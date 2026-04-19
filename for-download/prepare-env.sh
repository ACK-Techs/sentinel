#!/usr/bin/env bash
set -euo pipefail

CONTROLLER_NAME="${CONTROLLER_NAME:-microk8s-controller}"
MODEL_NAME="${MODEL_NAME:-cos}"
JUJU_CHANNEL="${JUJU_CHANNEL:-3.6/stable}"
METALLB_SPAN="${METALLB_SPAN:-5}"
SCRIPT_PATH="$(readlink -f "$0")"

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
    (( attempt++ ))
    sleep 5
  done
  fail "$desc 2 denemede de basarisiz oldu. Protokol geregi dur ve bekle."
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "'$1' komutu bulunamadi."
}

detect_primary_ip() {
  local ip
  ip="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '/src/ {for (i=1; i<=NF; i++) if ($i=="src") {print $(i+1); exit}}')"
  [ -n "$ip" ] || fail "Makinenin ana IPv4 adresi tespit edilemedi."
  printf '%s\n' "$ip"
}

build_metallb_range() {
  local host_ip="$1"
  local prefix last_octet start_octet end_octet

  prefix="${host_ip%.*}"
  last_octet="${host_ip##*.}"

  [[ "$last_octet" =~ ^[0-9]+$ ]] || fail "Gecersiz IPv4 adresi: $host_ip"

  start_octet="$last_octet"
  end_octet=$(( last_octet + METALLB_SPAN ))
  (( end_octet <= 254 )) || fail "MetalLB IP araligi 254 ustune cikiyor. Manuel mudahale gerekli."

  printf '%s-%s\n' "${prefix}.${start_octet}" "${prefix}.${end_octet}"
}

ensure_microk8s_group_and_reexec() {
  if ! getent group microk8s >/dev/null; then
    retry_twice "groupadd microk8s" sudo groupadd microk8s
  fi

  if id -nG "$USER" | tr ' ' '\n' | grep -qx microk8s; then
    ok "Kullanici microk8s grubunda"
    return 0
  fi

  retry_twice "usermod -aG microk8s $USER" sudo usermod -aG microk8s "$USER"
  ok "Kullanici microk8s grubuna eklendi"
  exec sg microk8s -c "CONTROLLER_NAME='$CONTROLLER_NAME' MODEL_NAME='$MODEL_NAME' JUJU_CHANNEL='$JUJU_CHANNEL' METALLB_SPAN='$METALLB_SPAN' bash '$SCRIPT_PATH'"
}

ensure_juju_kubeconfig_fix() {
  local juju_current juju_target_dir juju_target_cfg tmp_cfg

  juju_current="$(readlink -f /var/snap/juju/current)"
  [ -n "$juju_current" ] || fail "Juju current revision yolu bulunamadi."

  juju_target_dir="${juju_current}/microk8s/credentials"
  juju_target_cfg="${juju_target_dir}/client.config"
  tmp_cfg="$(mktemp)"

  retry_twice "mkdir juju microk8s credentials dizini" sudo mkdir -p "$juju_target_dir"
  retry_twice "chown juju microk8s credentials dizini" sudo chown -R "$USER:$USER" "${juju_current}/microk8s"
  retry_twice "microk8s kubeconfig gecici dosya yaz" bash -lc "microk8s config > '$tmp_cfg'"
  retry_twice "microk8s kubeconfig yaz" install -m 0644 "$tmp_cfg" "$juju_target_cfg"
  while IFS= read -r -d '' cfg; do
    retry_twice "ek juju kubeconfig yaz: $cfg" install -m 0644 "$tmp_cfg" "$cfg"
  done < <(find /var/snap/juju -path '*/microk8s/credentials/client.config' -print0 2>/dev/null)
  rm -f "$tmp_cfg"
  ok "Juju classic kubeconfig fix uygulandi: $juju_target_cfg"
}

echo "== Prepare Environment =="
require_cmd snap
require_cmd sudo
require_cmd ip

ensure_microk8s_group_and_reexec

echo
echo "== MicroK8s =="
if snap list microk8s >/dev/null 2>&1; then
  ok "microk8s zaten kurulu"
else
  retry_twice "snap install microk8s --classic" sudo snap install microk8s --classic
fi
retry_twice "microk8s hazirlik kontrolu" microk8s status --wait-ready

echo
echo "== Addons =="
retry_twice "microk8s enable dns" microk8s enable dns
retry_twice "microk8s enable hostpath-storage" microk8s enable hostpath-storage

PRIMARY_IP="$(detect_primary_ip)"
METALLB_RANGE="$(build_metallb_range "$PRIMARY_IP")"
echo "[CHECK] Primary IP      : $PRIMARY_IP"
echo "[CHECK] MetalLB araligi : $METALLB_RANGE"
retry_twice "microk8s enable metallb:$METALLB_RANGE" microk8s enable "metallb:${METALLB_RANGE}"

retry_twice "coredns rollout" microk8s kubectl rollout status deployment/coredns -n kube-system --timeout=180s
retry_twice "hostpath-provisioner rollout" microk8s kubectl rollout status deployment/hostpath-provisioner -n kube-system --timeout=180s
retry_twice "metallb speaker rollout" microk8s kubectl rollout status daemonset/speaker -n metallb-system --timeout=180s

echo
echo "== Juju =="
if snap list juju >/dev/null 2>&1; then
  retry_twice "snap refresh juju --classic --channel=$JUJU_CHANNEL" sudo snap refresh juju --classic --channel="$JUJU_CHANNEL"
else
  retry_twice "snap install juju --classic --channel=$JUJU_CHANNEL" sudo snap install juju --classic --channel="$JUJU_CHANNEL"
fi
retry_twice "juju version" juju version
ensure_juju_kubeconfig_fix

echo
echo "== Bootstrap =="
if juju controllers 2>/dev/null | awk 'NR>1 {gsub(/^[* ]+/,"",$1); print $1}' | grep -Fxq "$CONTROLLER_NAME"; then
  ok "Controller zaten mevcut: $CONTROLLER_NAME"
else
  retry_twice "juju bootstrap microk8s $CONTROLLER_NAME" juju bootstrap microk8s "$CONTROLLER_NAME"
fi

if juju models 2>/dev/null | awk 'NR>1 {gsub(/^[* ]+/,"",$1); print $1}' | grep -Fxq "$MODEL_NAME"; then
  ok "Model zaten mevcut: $MODEL_NAME"
else
  retry_twice "juju add-model $MODEL_NAME" juju add-model "$MODEL_NAME"
fi

retry_twice "juju switch $MODEL_NAME" juju switch "$MODEL_NAME"

echo
echo "== Son Durum =="
juju controllers
juju models
echo "Artik juju deploy ./cos-bundle.yaml yazarak kurulumu baslatabilirsiniz"
