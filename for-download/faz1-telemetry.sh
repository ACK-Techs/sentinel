#!/usr/bin/env bash
# Faz 1 — Bölüm 2: OTLP gateway (Tempo + OpenTelemetry Collector) ve Grafana trace datasource.
# Sentinel / COS: Juju modelinde tempo-k8s ve opentelemetry-collector-k8s; Tempo için Traefik (traefik_route).
#
# OTLP dis erisim: Traefik HTTP yonlendirmesi kullanilmiyor; collector'a gelen veriler NodePort veya
# MetalLB ile K8s Service uzerinden (ic/dmz) erisilebilir. OTEL_CHANNEL icin stabil kanal (or. 2/stable)
# kullanilabilir — charm'da ingress ucu olmasi beklenmez.

set -euo pipefail

MODEL_NAME="${MODEL_NAME:-cos}"

TEMPO_APP="${TEMPO_APP:-tempo}"
TEMPO_CHARM="${TEMPO_CHARM:-tempo-k8s}"
TEMPO_CHANNEL="${TEMPO_CHANNEL:-latest/stable}"

OTEL_APP="${OTEL_APP:-otel-collector}"
OTEL_CHARM="${OTEL_CHARM:-opentelemetry-collector-k8s}"
OTEL_CHANNEL="${OTEL_CHANNEL:-2/stable}"

PROMETHEUS_APP="${PROMETHEUS_APP:-prometheus}"
LOKI_APP="${LOKI_APP:-loki}"
GRAFANA_APP="${GRAFANA_APP:-grafana}"
TRAEFIK_APP="${TRAEFIK_APP:-traefik}"

WAIT_ROUNDS="${WAIT_ROUNDS:-24}"
WAIT_SLEEP="${WAIT_SLEEP:-15}"

ok() { printf '[OK] %s\n' "$1"; }
warn() { printf '[WARN] %s\n' "$1" >&2; }
fail() { printf '[DUR] %s\n' "$1" >&2; exit 1; }

retry_twice() {
  local desc="$1"
  shift
  local attempt=1
  while (( attempt <= 2 )); do
    if "$@"; then
      ok "$desc"
      return 0
    fi
    warn "$desc basarisiz oldu (deneme ${attempt}/2)"
    (( attempt++ )) || true
    sleep 5
  done
  fail "$desc 2 denemede de basarisiz oldu. Protokol geregi dur ve bekle."
}

# juju status JSON'unu ortamda tasiyarak pipe/heredoc stdin carpismasini onler.
load_status_json() {
  JUJU_STATUS_JSON="$(juju status --model "$MODEL_NAME" --format=json)"
  export JUJU_STATUS_JSON
}

relation_exists_between_apps() {
  local left="$1"
  local right="$2"
  load_status_json
  python3 -c '
import json, os, sys
left, right = sys.argv[1], sys.argv[2]
data = json.loads(os.environ["JUJU_STATUS_JSON"])
for app_name in (left, right):
    app = data.get("applications", {}).get(app_name)
    if not app:
        sys.exit(1)
    rels = app.get("relations") or {}
    for items in rels.values():
        if isinstance(items, dict):
            items = [items]
        for it in items:
            if not isinstance(it, dict):
                continue
            ra = it.get("related-application")
            if ra == right or ra == left:
                sys.exit(0)
sys.exit(1)
' "$left" "$right"
}

deploy_if_missing() {
  local app="$1"
  local charm="$2"
  local channel="$3"

  if juju status --model "$MODEL_NAME" "$app" >/dev/null 2>&1; then
    ok "Uygulama zaten mevcut: $app"
    return 0
  fi

  retry_twice "juju deploy $charm as $app" \
    juju deploy "$charm" "$app" --channel "$channel"
}

integrate_if_missing() {
  local left="$1"
  local right="$2"
  # left veya sag uygulama adini cikar (or. otel-collector:send-traces -> otel-collector)
  local left_app="${left%%:*}"
  local right_app="${right%%:*}"

  if relation_exists_between_apps "$left_app" "$right_app"; then
    ok "Relation zaten var (uygulamalar): $left_app <-> $right_app"
    return 0
  fi

  retry_twice "juju integrate $left $right" \
    juju integrate --model "$MODEL_NAME" "$left" "$right"
}

has_relation_endpoint() {
  local charm="$1"
  local endpoint="$2"
  local channel="${3:-}"

  local out
  if [[ -n "$channel" ]]; then
    out="$(juju info "$charm" --channel "$channel" --format=yaml 2>/dev/null || true)"
  else
    out="$(juju info "$charm" --format=yaml 2>/dev/null || true)"
  fi
  grep -Eq "^[[:space:]]+${endpoint}:[[:space:]]*$" <<<"$out" \
    || grep -Eq "^[[:space:]]+${endpoint}:" <<<"$out"
}

declare -A RESOLVE_COUNT=()

resolve_error_units_if_needed() {
  load_status_json
  local units
  mapfile -t units < <(
    python3 -c '
import json, os
data = json.loads(os.environ["JUJU_STATUS_JSON"])
for app in data.get("applications", {}).values():
    for unit_name, unit in (app.get("units") or {}).items():
        wl = (unit.get("workload-status") or {}).get("current", "")
        ag = (unit.get("juju-status") or {}).get("current", "")
        if wl == "error" or ag == "error":
            print(unit_name)
'
  )

  if (( ${#units[@]} == 0 )); then
    return 0
  fi

  local unit count
  for unit in "${units[@]}"; do
    count="${RESOLVE_COUNT[$unit]:-0}"
    if (( count >= 2 )); then
      fail "$unit icin 2 resolve denemesi tukendi. Protokol geregi dur ve bekle."
    fi
    retry_twice "juju resolve $unit" juju resolve "$unit" --model "$MODEL_NAME"
    RESOLVE_COUNT["$unit"]=$(( count + 1 ))
  done
}

wait_for_active_idle() {
  local desc="$1"
  shift
  local apps=("$@")
  local round

  for round in $(seq 1 "$WAIT_ROUNDS"); do
    load_status_json
    if python3 -c '
import json, os, sys
data = json.loads(os.environ["JUJU_STATUS_JSON"])
apps = sys.argv[1:]
for app_name in apps:
    app = data.get("applications", {}).get(app_name)
    if not app:
        sys.exit(1)
    ast = (app.get("application-status") or {}).get("current")
    if ast and ast != "active":
        sys.exit(1)
    units = app.get("units") or {}
    if not units:
        sys.exit(1)
    for unit in units.values():
        wl = (unit.get("workload-status") or {}).get("current", "")
        ag = (unit.get("juju-status") or {}).get("current", "")
        if wl != "active" or ag != "idle":
            sys.exit(1)
sys.exit(0)
' "${apps[@]}"; then
      ok "$desc"
      return 0
    fi

    resolve_error_units_if_needed
    sleep "$WAIT_SLEEP"
  done

  juju status --model "$MODEL_NAME"
  fail "$desc zaman asimina ugradi. Protokol geregi dur ve bekle."
}

echo "== Faz 1 — Telemetry (Tempo + OTel Collector + Grafana; Tempo-Traefik) =="

echo "[CHECK] Model erisimi"
juju status --model "$MODEL_NAME" >/dev/null
ok "Model erisilebilir: $MODEL_NAME"

echo
echo "== Preflight (charm uclari) =="
has_relation_endpoint "prometheus-k8s" "receive-remote-write" || fail "prometheus-k8s receive-remote-write ucu bulunamadi."
has_relation_endpoint "loki-k8s" "logging" || fail "loki-k8s logging ucu bulunamadi."
has_relation_endpoint "$OTEL_CHARM" "send-remote-write" "$OTEL_CHANNEL" || fail "$OTEL_CHARM ($OTEL_CHANNEL) send-remote-write ucu bulunamadi."
has_relation_endpoint "$OTEL_CHARM" "send-loki-logs" "$OTEL_CHANNEL" || fail "$OTEL_CHARM send-loki-logs ucu bulunamadi."
has_relation_endpoint "$OTEL_CHARM" "send-traces" "$OTEL_CHANNEL" || fail "$OTEL_CHARM send-traces ucu bulunamadi."
has_relation_endpoint "$TEMPO_CHARM" "tracing" "$TEMPO_CHANNEL" || fail "$TEMPO_CHARM tracing ucu bulunamadi."
has_relation_endpoint "grafana-k8s" "grafana-source" || fail "grafana-k8s grafana-source (requirer) bulunamadi."
has_relation_endpoint "$TEMPO_CHARM" "grafana-source" "$TEMPO_CHANNEL" || fail "$TEMPO_CHARM grafana-source (provider) bulunamadi."

ok "Temel relation endpoint'leri dogrulandi (OTel Traefik ingress kontrolu atlandi — OTLP NodePort/MetalLB)"

echo
echo "== Deploy =="
deploy_if_missing "$TEMPO_APP" "$TEMPO_CHARM" "$TEMPO_CHANNEL"
deploy_if_missing "$OTEL_APP" "$OTEL_CHARM" "$OTEL_CHANNEL"

wait_for_active_idle "Yeni uygulamalar active/idle oldu" "$TEMPO_APP" "$OTEL_APP"

echo
echo "== Telemetry baglantilari (COS) =="
# Metrikler: OTLP -> collector -> Prometheus (remote write), scrape degil.
integrate_if_missing "$OTEL_APP:send-remote-write" "$PROMETHEUS_APP:receive-remote-write"
integrate_if_missing "$OTEL_APP:send-loki-logs" "$LOKI_APP:logging"
integrate_if_missing "$OTEL_APP:send-traces" "$TEMPO_APP:tracing"

echo
echo "== Grafana datasource (trace UI) =="
integrate_if_missing "$GRAFANA_APP:grafana-source" "$TEMPO_APP:grafana-source"

wait_for_active_idle "Telemetry + Grafana datasource sonrasi active/idle" \
  alertmanager catalogue "$GRAFANA_APP" "$LOKI_APP" prometheus traefik "$TEMPO_APP" "$OTEL_APP"

echo
echo "== Traefik (Tempo dis erisim) =="
# COS: traefik_route <-> tempo ingress. OTel collector Traefik'e baglanmaz (OTLP Service/NodePort/MetalLB).
integrate_if_missing "$TRAEFIK_APP:traefik-route" "$TEMPO_APP:ingress"

wait_for_active_idle "Tempo-Traefik route sonrasi ilgili uygulamalar active/idle" \
  alertmanager catalogue "$GRAFANA_APP" "$LOKI_APP" prometheus traefik "$TEMPO_APP"

echo
echo "== Son durum =="
juju status --model "$MODEL_NAME" --relations

echo
echo "== Dogrulama ipucu =="
echo "Traefik (Tempo): juju run ${TRAEFIK_APP}/0 show-proxied-endpoints --model $MODEL_NAME --format=yaml"
echo "OTLP (collector): K8s Service / NodePort veya MetalLB IP — ornek: microk8s kubectl get svc -A | grep -i otel"
echo "Grafana: Explore icinde Tempo datasource secildi mi kontrol edin (grafana-source relation)."
