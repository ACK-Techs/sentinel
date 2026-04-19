#!/usr/bin/env bash
# MicroK8s/Juju IP drift oldugunda kubelet cert ve Juju kubeconfig'lerini onarir.
# Kullanim:
#   sudo ./scripts/cos-microk8s-heal.sh

set -euo pipefail

if [[ "${EUID:-}" -ne 0 ]]; then
  echo "Root gerekli: sudo $0" >&2
  exit 1
fi

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Gerekli komut bulunamadi: $1" >&2
    exit 1
  }
}

log() {
  printf '[heal] %s\n' "$1"
}

detect_primary_ip() {
  local ip
  ip="$(ip -4 route get 1.1.1.1 2>/dev/null | awk '/src/ {for (i=1; i<=NF; i++) if ($i=="src") {print $(i+1); exit}}')"
  [[ -n "$ip" ]] || {
    echo "Ana IPv4 adresi tespit edilemedi." >&2
    exit 1
  }
  printf '%s\n' "$ip"
}

detect_invoking_user() {
  if [[ -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    printf '%s\n' "${SUDO_USER}"
    return 0
  fi
  log "SUDO_USER yok; sadece sistem tarafi fix uygulanacak."
  printf '%s\n' "root"
}

patch_juju_client_files() {
  local owner="$1"
  local endpoint="$2"
  local juju_dir controllers bootstrap

  [[ "$owner" == "root" ]] && return 0

  juju_dir="$(eval echo "~${owner}")/.local/share/juju"
  controllers="${juju_dir}/controllers.yaml"
  bootstrap="${juju_dir}/bootstrap-config.yaml"

  if [[ -f "$controllers" ]]; then
    perl -0pi -e 's#https://[0-9.]+:16443#'"${endpoint}"'#g' "$controllers"
    log "Juju controllers.yaml guncellendi"
  fi

  if [[ -f "$bootstrap" ]]; then
    perl -0pi -e 's#https://[0-9.]+:16443#'"${endpoint}"'#g' "$bootstrap"
    log "Juju bootstrap-config.yaml guncellendi"
  fi
}

write_juju_microk8s_kubeconfigs() {
  local cfg tmp_cfg

  tmp_cfg="$(mktemp)"
  microk8s config > "$tmp_cfg"

  while IFS= read -r -d '' cfg; do
    install -m 0644 "$tmp_cfg" "$cfg"
    log "Juju kubeconfig yenilendi: $cfg"
  done < <(find /var/snap/juju -path '*/microk8s/credentials/client.config' -print0 2>/dev/null)

  rm -f "$tmp_cfg"
}

cert_has_ip() {
  local cert_path="$1"
  local ip="$2"

  [[ -s "$cert_path" ]] || return 1
  openssl x509 -in "$cert_path" -noout -ext subjectAltName 2>/dev/null | grep -Fq "IP Address:${ip}"
}

regenerate_kubelet_material() {
  log "kubelet/client cert ve kubeconfig'leri yeniden uretiliyor"
  snap run --shell microk8s -c '. $SNAP/actions/common/utils.sh; create_user_certificates; create_user_kubeconfigs'
}

restart_microk8s() {
  log "microk8s yeniden baslatiliyor"
  microk8s stop
  microk8s start
  microk8s status --wait-ready
  microk8s kubectl wait --for=condition=Ready nodes --all --timeout=300s
}

verify_live_kubelet_cert() {
  local ip="$1"
  echo | openssl s_client -connect "${ip}:10250" -servername "${ip}" 2>/dev/null | openssl x509 -noout -ext subjectAltName 2>/dev/null | grep -Fq "IP Address:${ip}"
}

maybe_update_client_cloud() {
  local owner="$1"

  [[ "$owner" == "root" ]] && return 0

  if runuser -u "$owner" -- juju update-k8s --client microk8s >/dev/null 2>&1; then
    log "juju update-k8s --client microk8s basarili"
  else
    log "juju update-k8s best-effort olarak denendi; hata varsa lokal fix'ler yine uygulandi"
  fi
}

main() {
  local current_ip current_endpoint owner needs_restart=0

  require_cmd microk8s
  require_cmd openssl
  require_cmd perl
  require_cmd runuser
  require_cmd snap
  require_cmd ip

  current_ip="$(detect_primary_ip)"
  current_endpoint="https://${current_ip}:16443"
  owner="$(detect_invoking_user)"

  log "Aktif host IP: ${current_ip}"
  patch_juju_client_files "$owner" "$current_endpoint"
  write_juju_microk8s_kubeconfigs
  maybe_update_client_cloud "$owner"

  if ! cert_has_ip /var/snap/microk8s/current/certs/kubelet.crt "$current_ip"; then
    regenerate_kubelet_material
    needs_restart=1
  fi

  if (( needs_restart == 1 )); then
    restart_microk8s
  fi

  if verify_live_kubelet_cert "$current_ip"; then
    log "Canli kubelet sertifikasi dogru IP ile eslesiyor"
  else
    echo "Canli kubelet sertifikasi dogrulanamadi. manual kontrol gerekli." >&2
    exit 1
  fi

  if [[ "$owner" != "root" ]]; then
    runuser -u "$owner" -- juju status >/dev/null 2>&1 \
      && log "juju status erisimi dogrulandi" \
      || log "juju status best-effort kontrolu basarisiz; controller tarafini ayrica kontrol et"
  fi
}

main "$@"
