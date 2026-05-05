#!/usr/bin/env bash

set -euo pipefail

DEBOUNCE_SEC="${AUTO_PUSH_DEBOUNCE_SEC:-2}"
COMMIT_PREFIX="${AUTO_PUSH_COMMIT_PREFIX:-chore: auto-push snapshot}"
WATCH_EVENTS="${AUTO_PUSH_EVENTS:-modify,create,delete,move,attrib}"
EXCLUDE_REGEX="${AUTO_PUSH_EXCLUDE_REGEX:-(^|/)\.git(/|$)|(^|/)node_modules(/|$)|(^|/)\.venv(/|$)|(^|/)\.pytest_cache(/|$)|(^|/)__pycache__(/|$)}"

log() {
  printf '[auto-push] %s\n' "$*"
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    log "missing command: $1"
    exit 1
  fi
}

require_command git
require_command inotifywait

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "${REPO_ROOT}" ]]; then
  log "current directory is not inside a git repository"
  exit 1
fi

cd "${REPO_ROOT}"

BRANCH="${AUTO_PUSH_BRANCH:-$(git branch --show-current)}"
if [[ -z "${BRANCH}" ]]; then
  log "detached HEAD is not supported"
  exit 1
fi

UPSTREAM="${AUTO_PUSH_UPSTREAM:-$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)}"
if [[ -z "${UPSTREAM}" ]]; then
  log "no upstream configured for branch ${BRANCH}"
  exit 1
fi

REMOTE="${AUTO_PUSH_REMOTE:-${UPSTREAM%%/*}}"
REMOTE_BRANCH="${AUTO_PUSH_REMOTE_BRANCH:-${UPSTREAM#*/}}"

commit_and_push() {
  if [[ -z "$(git status --porcelain)" ]]; then
    return 0
  fi

  git add -A

  if git diff --cached --quiet; then
    return 0
  fi

  local timestamp
  timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  if ! git commit -m "${COMMIT_PREFIX} ${timestamp}" --no-verify; then
    log "commit failed"
    return 1
  fi

  if ! git push "${REMOTE}" "HEAD:${REMOTE_BRANCH}"; then
    log "push failed; resolve remote divergence/auth and restart if needed"
    return 1
  fi

  log "pushed ${BRANCH} at ${timestamp}"
}

log "watching ${REPO_ROOT}"
log "upstream ${REMOTE}/${REMOTE_BRANCH}"
log "debounce ${DEBOUNCE_SEC}s"

while true; do
  inotifywait \
    --quiet \
    --recursive \
    --event "${WATCH_EVENTS}" \
    --exclude "${EXCLUDE_REGEX}" \
    "${REPO_ROOT}" >/dev/null

  sleep "${DEBOUNCE_SEC}"
  commit_and_push || sleep "${DEBOUNCE_SEC}"
done
