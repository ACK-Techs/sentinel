#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="${MODEL_NAME:-cos}"
# Juju uygulama adi; K8s Service adi genelde bununla aynidir (bundle'daki otel-collector).
OTEL_APP="${OTEL_APP:-otel-collector}"
TRAEFIK_UNIT="traefik/0"
GRAFANA_UNIT="grafana/0"

ok() { printf '[OK] %s\n' "$1"; }
warn() { printf '[WARN] %s\n' "$1" >&2; }
fail() { printf '[DUR] %s\n' "$1" >&2; exit 1; }

echo "== Faz 4 + Faz 5 | Sentinel Telemetry Gateway Entegrasyon ve Dogrulama =="

echo "[CHECK] Model durumu"
juju status --model "$MODEL_NAME" >/dev/null
ok "Juju modeli erisilebilir: $MODEL_NAME"

echo
echo "[CHECK] Traefik proxied endpoint'leri"
PROXIED_OUTPUT="$(juju run "$TRAEFIK_UNIT" show-proxied-endpoints --model "$MODEL_NAME" --format=yaml)" \
  || fail "show-proxied-endpoints basarisiz. Protokol geregi dur ve bekle."

printf '%s\n' "$PROXIED_OUTPUT"
ok "Traefik proxied endpoint'leri alindi (Tempo dahil)"

echo
echo "[CHECK] Grafana admin parolasi"
GRAFANA_PASSWORD="$(
  juju run "$GRAFANA_UNIT" get-admin-password --model "$MODEL_NAME" --format=yaml \
  | awk -F': ' '/admin-password:/ {print $2; exit}'
)"
[ -n "${GRAFANA_PASSWORD:-}" ] || fail "Grafana admin parolasi alinamadi. Protokol geregi dur ve bekle."

echo "Grafana kullanici: admin"
echo "Grafana parola  : ${GRAFANA_PASSWORD}"
ok "Grafana admin parolasi alindi"

echo
echo "[CHECK] OTLP Gateway IP Adresi (OpenTelemetry) [OTEL_APP=${OTEL_APP}]"
OTEL_EXT_IP="$(
  sudo microk8s kubectl get svc -n "$MODEL_NAME" --no-headers \
    | awk -v app="$OTEL_APP" '$1 == app { print $4; exit }'
)"
if [ -n "${OTEL_EXT_IP:-}" ] && [ "$OTEL_EXT_IP" != "<none>" ]; then
  OTEL_SVC="$OTEL_EXT_IP"
else
  OTEL_SVC="Bulunamadi"
fi
if [ "$OTEL_SVC" != "Bulunamadi" ] && [ -n "$OTEL_SVC" ]; then
    ok "OTLP Gateway (MetalLB IP): $OTEL_SVC (Port: 4317/4318)"
else
    warn "OTLP IP adresi dogrudan bulunamadi, K8s NodePort kullaniliyor olabilir."
fi

echo
echo "== Tarayicida acilacak URL'ler =="
echo "Asagidaki URL'leri Traefik cikisindan kullan:"
echo "$PROXIED_OUTPUT" | sed 's/^/  /'
echo "Grafana icin gereken kullanici: admin"
echo "Grafana icin gereken parola   : ${GRAFANA_PASSWORD}"

echo
echo "== Son durum =="
juju status --model "$MODEL_NAME"