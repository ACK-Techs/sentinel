#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SMOKE_VENV="${ROOT_DIR}/.venv-smoke"

cd "${ROOT_DIR}"
rm -rf dist "${SMOKE_VENV}"
./.venv/bin/python -m build
python3 -m venv "${SMOKE_VENV}"
"${SMOKE_VENV}/bin/python" -m pip install --upgrade pip
"${SMOKE_VENV}/bin/python" -m pip install dist/sentinel_cli-*.whl
"${SMOKE_VENV}/bin/sentinel-cli" --help
"${SMOKE_VENV}/bin/sentinel-cli" version
