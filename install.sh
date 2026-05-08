#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTPYPI_PACKAGE="${SENTINEL_TESTPYPI_PACKAGE:-sentinel-cli}"
GIT_FALLBACK_URL="${SENTINEL_GIT_URL:-}"
INSTALL_MODE="${SENTINEL_INSTALL_MODE:-}"
export PATH="$HOME/.local/bin:$PATH"

log() {
  printf '[sentinel-install] %s\n' "$*"
}

fail() {
  printf '[sentinel-install] %s\n' "$*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Gerekli komut bulunamadi: $1"
}

detect_platform() {
  local os arch
  os="$(uname -s | tr '[:upper:]' '[:lower:]')"
  arch="$(uname -m)"
  case "$arch" in
    x86_64|amd64) arch="amd64" ;;
    aarch64|arm64) arch="arm64" ;;
    armv7l) arch="armv7" ;;
  esac
  log "platform: ${os}/${arch}"
}

ensure_python() {
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
    return 0
  fi
  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
    return 0
  fi
  fail "Python bulunamadi. Python 3.11+ kurup tekrar deneyin."
}

ensure_pipx() {
  if command -v pipx >/dev/null 2>&1; then
    return 0
  fi

  log "pipx bulunamadi; kuruluyor"
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y pipx
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y pipx
  elif command -v yum >/dev/null 2>&1; then
    sudo yum install -y pipx
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm pipx
  elif command -v brew >/dev/null 2>&1; then
    brew install pipx
  else
    "$PYTHON_BIN" -m pip install --user pipx
    export PATH="$HOME/.local/bin:$PATH"
  fi

  command -v pipx >/dev/null 2>&1 || fail "pipx kurulumu tamamlanamadi."
  pipx ensurepath >/dev/null 2>&1 || true
}

install_sentinel_cli() {
  log "sentinel-cli TestPyPI uzerinden kuruluyor"
  if pipx install --force \
    "$TESTPYPI_PACKAGE" \
    --pip-args="--index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/"; then
    return 0
  fi

  log "TestPyPI kurulumu basarisiz; git+https fallback deneniyor"
  if [[ -z "$GIT_FALLBACK_URL" ]] && command -v git >/dev/null 2>&1; then
    GIT_FALLBACK_URL="$(git -C "$SCRIPT_DIR" remote get-url origin 2>/dev/null || true)"
  fi
  if [[ -z "$GIT_FALLBACK_URL" ]]; then
    GIT_FALLBACK_URL="https://github.com/<user>/sentinel-coming.git"
  fi
  pipx install --force "git+${GIT_FALLBACK_URL}#subdirectory=cli"
}

run_sentinel_install() {
  if [[ -n "$INSTALL_MODE" ]]; then
    sentinel install --mode "$INSTALL_MODE"
    return 0
  fi

  if [[ -t 0 ]]; then
    sentinel install
    return 0
  fi

  log "TTY yok; varsayilan compose modu kullaniliyor"
  sentinel install --mode compose
}

main() {
  detect_platform
  ensure_python
  ensure_pipx
  install_sentinel_cli
  require_cmd sentinel
  run_sentinel_install
}

main "$@"
