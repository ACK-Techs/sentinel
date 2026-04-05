#!/usr/bin/env bash
# Bireysel kapanis: Grafana snapshot + REPL/run dogrulama adimlari (sirayla).
# Kullanim: cli kokunden: ./scripts/verify_grafana_context_repl.sh
# Adimlar arasinda duraklatmak icin: STEP_PAUSE=1 ./scripts/verify_grafana_context_repl.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

PYTHON="${ROOT_DIR}/.venv/bin/python"
CLI="${ROOT_DIR}/.venv/bin/sentinel-cli"

_pause() {
  if [[ "${STEP_PAUSE:-0}" == "1" ]]; then
    read -r -p "Devam icin Enter... " _
  fi
}

_banner() {
  echo ""
  echo "================================================================================"
  echo "  $1"
  echo "================================================================================"
}

if [[ ! -x "${PYTHON}" ]]; then
  echo "Hata: ${PYTHON} yok. Once: python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'" >&2
  exit 1
fi

_banner "1/7 — Calisma dizini"
echo "${ROOT_DIR}"

_banner "2/7 — grafana_context bayraklari (sentinel.yaml / .env)"
grep -E "grafana_context|SENTINEL_GRAFANA_CONTEXT" config/sentinel.yaml .env 2>/dev/null || echo "(eslesme yok veya dosya eksik — kontrol edin)"
_pause

_banner "3/7 — pytest: agent_loop Grafana testleri"
"${PYTHON}" -m pytest -q tests/unit/test_agent_loop.py -k grafana
_pause

_banner "4/7 — sentinel-cli run (ilk oturum, snapshot + system_prompt)"
"${CLI}" run "Sentinel operasyonel Grafana ozetinde ne yaziyor, kisa tekrarla."
_pause

_banner "5/7 — Ayni oturumda ikinci mesaj (snapshot tekrar HTTP ile cekilmez)"
SESSION_FILE="$(ls -t "${ROOT_DIR}/.sentinel/sessions/"*.json 2>/dev/null | head -1 || true)"
if [[ -z "${SESSION_FILE}" ]]; then
  echo "Uyari: Oturum dosyasi bulunamadi; 4. adim atlanmis olabilir." >&2
  exit 1
fi
SESSION_ID="$(basename "${SESSION_FILE}" .json)"
echo "session_id=${SESSION_ID}"
"${CLI}" run --session-id "${SESSION_ID}" --resume "Operasyonel ozette http_status kac yaziyor? Sadece sayi veya kisa cevap."
_pause

_banner "6/7 — Yeni oturum, grafana_context kapali (ozet beklenmez)"
SENTINEL_GRAFANA_CONTEXT_IN_REPL=false "${CLI}" run "Bana Grafana baglanti ozeti sistem tarafindan verildi mi? Tek cumle."
_pause

_banner "7/7 — Tum pytest"
"${PYTHON}" -m pytest -q

echo ""
echo "Tamamlandi."
