#!/usr/bin/env bash
set -euo pipefail

MODEL_NAME="cos"
TRAEFIK_UNIT="traefik/0"
GRAFANA_UNIT="grafana/0"

ok() { printf '[OK] %s\n' "$1"; }
fail() { printf '[DUR] %s\n' "$1" >&2; exit 1; }

echo "== Faz 4 + Faz 5 | Entegrasyon ve dogrulama =="

echo "[CHECK] Model durumu"
juju status --model "$MODEL_NAME" >/dev/null
ok "Juju modeli erisilebilir"

echo
echo "[CHECK] Traefik proxied endpoint'leri"
PROXIED_OUTPUT="$(juju run "$TRAEFIK_UNIT" show-proxied-endpoints --model "$MODEL_NAME" --format=yaml)" \
  || fail "show-proxied-endpoints basarisiz. Protokol geregi dur ve bekle."

printf '%s\n' "$PROXIED_OUTPUT"
ok "Traefik proxied endpoint'leri alindi"

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
echo "== Tarayicida acilacak URL'ler =="
echo "Asagidaki URL'leri Traefik cikisindan kullan:"
echo "$PROXIED_OUTPUT" | sed 's/^/  /'
echo "Grafana icin gereken kullanici: admin"
echo "Grafana icin gereken parola   : ${GRAFANA_PASSWORD}"

echo
echo "== Son durum =="
juju status --model "$MODEL_NAME" --relations
