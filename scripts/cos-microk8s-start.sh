#!/usr/bin/env bash
# COS + Juju icin MicroK8s guvenli baslatma.
# Kullanim: sudo ./scripts/cos-microk8s-start.sh
#            COS_HEAL_TEMPO=1 sudo ./scripts/cos-microk8s-start.sh   # Tempo waiting ise edge refresh
#
# Amac: "microk8s start" sonrasi API/node hazir olmadan Juju uniter'in hook calistirmasini
# azaltmak; Tempo'daki tempo-ready / Pebble yarisi icin asil cozum charm (latest/edge)
# — bkz. cli/documantations/error-descriptions/TEMPO_K8S_JUJU_COS.md

set -euo pipefail

if [[ "${EUID:-}" -ne 0 ]]; then
  echo "Root gerekli: sudo $0" >&2
  exit 1
fi

if ! command -v microk8s >/dev/null 2>&1; then
  echo "microk8s bulunamadi (snap kurulu mu?)." >&2
  exit 1
fi

echo "==> microk8s start"
microk8s start

if [[ -x "$(dirname "$0")/cos-microk8s-heal.sh" ]]; then
  echo "==> IP drift / Juju kubeconfig / kubelet cert onarimi"
  "$(dirname "$0")/cos-microk8s-heal.sh"
fi

echo "==> Kubernetes API / servisler hazir (bekleniyor)"
# --wait-ready yoksa veya --timeout desteklenmiyorsa yedek dongu
if microk8s status --help 2>&1 | grep -q -- '--wait-ready'; then
  if microk8s status --help 2>&1 | grep -q -- '--timeout'; then
    microk8s status --wait-ready --timeout 600
  else
    microk8s status --wait-ready
  fi
else
  end=$(( $(date +%s) + 600 ))
  until microk8s kubectl get --raw=/readyz >/dev/null 2>&1; do
    if (( $(date +%s) > end )); then
      echo "Zaman asimi: API ayaga kalkmadi." >&2
      exit 1
    fi
    sleep 2
  done
fi

echo "==> Tum node'lar Ready"
microk8s kubectl wait --for=condition=Ready nodes --all --timeout=300s

echo "==> cos namespace pod'lari (varsa) Running/Ready bekleniyor"
if microk8s kubectl get ns cos >/dev/null 2>&1; then
  # Best-effort: COS podlari icin kisa bekleme (hook yarisi azaltmaya yardim eder)
  microk8s kubectl wait --for=condition=Ready pod --all -n cos --timeout=300s 2>/dev/null || true
fi

echo "==> Juju ajanlari ve Pebble icin sakinlesme (~45 sn)"
sleep 45

_heal_tempo() {
  command -v juju >/dev/null 2>&1 || return 0
  juju switch cos >/dev/null 2>&1 || return 0
  local out
  out=$(juju status tempo --no-color 2>/dev/null || true)
  if echo "$out" | grep -qi waiting && echo "$out" | grep -qiE 'tempo|API not ready'; then
    echo "==> Tempo waiting goruldu -> latest/edge + --force-units (tempo-ready duzeltmesi)"
    juju refresh tempo --channel=latest/edge --force-units
  fi
}

if [[ "${COS_HEAL_TEMPO:-}" == "1" ]]; then
  _heal_tempo
fi

echo ""
echo "MicroK8s hazir. Son kontrol: juju switch cos && juju status"
echo "Tempo yine waiting ise: COS_HEAL_TEMPO=1 sudo $0 veya:"
echo "  juju refresh tempo --channel=latest/edge --force-units"
echo "(Kalici: tempo-k8s'i edge'de tut veya stable'a duzeltme gelince stable'a sabitle.)"
