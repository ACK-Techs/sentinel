#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
VENV_PY="$REPO_ROOT/.venv/bin/python"
VENV_PIP="$REPO_ROOT/.venv/bin/pip"
HEAL_SCRIPT="$REPO_ROOT/scripts/cos-microk8s-heal.sh"
RUN_DIR="$ROOT/runs/local-smoke-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RUN_DIR"

SERVICE_PIDS=()

log() {
  printf '[smoke] %s\n' "$1"
}

cleanup() {
  set +e
  for pid in "${SERVICE_PIDS[@]:-}"; do
    kill "$pid" >/dev/null 2>&1 || true
  done
}
trap cleanup EXIT

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Required command not found: $1" >&2
    exit 1
  }
}

wait_for_http() {
  local url="$1"
  local name="$2"
  local retries=60
  while (( retries > 0 )); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      log "$name is ready"
      return 0
    fi
    retries=$((retries - 1))
    sleep 1
  done
  echo "$name did not become ready: $url" >&2
  exit 1
}

wait_for_tcp() {
  local host="$1"
  local port="$2"
  local name="$3"
  local retries=60
  while (( retries > 0 )); do
    if "$VENV_PY" - <<'PY' "$host" "$port" >/dev/null 2>&1
import socket
import sys
s = socket.socket()
s.settimeout(1)
try:
    s.connect((sys.argv[1], int(sys.argv[2])))
finally:
    s.close()
PY
    then
      log "$name tcp is ready"
      return 0
    fi
    retries=$((retries - 1))
    sleep 1
  done
  if [[ -f "$HEAL_SCRIPT" ]]; then
    echo "Hint: sudo $HEAL_SCRIPT" >&2
  fi
  echo "$name tcp did not become ready: $host:$port" >&2
  exit 1
}

start_service() {
  local name="$1"
  local workdir="$2"
  local logfile="$3"
  shift 3
  (
    cd "$workdir"
    env "$@" >"$logfile" 2>&1
  ) &
  SERVICE_PIDS+=("$!")
}

service_cluster_ip() {
  local namespace="$1"
  local service="$2"
  microk8s kubectl -n "$namespace" get svc "$service" -o jsonpath='{.spec.clusterIP}'
}

resolve_service_host() {
  local namespace="$1"
  local service="$2"
  local port="$3"
  local name="$4"
  local host

  host="$(service_cluster_ip "$namespace" "$service")"
  if [[ -z "$host" || "$host" == "None" ]]; then
    echo "ClusterIP not found for ${namespace}/${service}" >&2
    exit 1
  fi
  wait_for_tcp "$host" "$port" "$name" >&2
  printf '%s\n' "$host"
}

require_cmd microk8s
require_cmd curl
require_cmd ss
require_cmd pkill

if [[ ! -x "$VENV_PY" ]]; then
  echo "Missing virtualenv python: $VENV_PY" >&2
  exit 1
fi

log "Installing editable packages into repo venv"
"$VENV_PIP" install -e "$ROOT/libs/observability" \
  -e "$ROOT/services/gateway" \
  -e "$ROOT/services/orders" \
  -e "$ROOT/services/payments" \
  -e "$ROOT/services/inventory" \
  -e "$ROOT/services/worker" >/dev/null

log "Applying infra manifests"
microk8s kubectl apply -f "$ROOT/k8s/namespace.yaml" \
  -f "$ROOT/k8s/postgres.yaml" \
  -f "$ROOT/k8s/redis.yaml" >/dev/null
microk8s kubectl -n sentinel-target wait --for=condition=Ready pod/postgres-0 --timeout=300s >/dev/null
microk8s kubectl -n sentinel-target wait --for=condition=Ready pod/redis-0 --timeout=300s >/dev/null

POSTGRES_HOST="$(resolve_service_host sentinel-target postgres 5432 postgres-service)"
REDIS_HOST="$(resolve_service_host sentinel-target redis 6379 redis-service)"
OTEL_HOST="$(resolve_service_host cos otel-collector 4317 cos-otel-service)"

log "Seeding databases"
export ORDERS_DB_URL="postgresql+asyncpg://sentinel:sentinel@${POSTGRES_HOST}:5432/orders_db"
export PAYMENTS_DB_URL="postgresql+asyncpg://sentinel:sentinel@${POSTGRES_HOST}:5432/payments_db"
export INVENTORY_DB_URL="postgresql+asyncpg://sentinel:sentinel@${POSTGRES_HOST}:5432/inventory_db"
export PAYMENTS_REDIS_URL="redis://${REDIS_HOST}:6379/1"
"$VENV_PY" "$ROOT/scripts/seed_db.py"

log "Stopping previous local test-platform processes if any"
pkill -f 'test-platform/services/.*/uvicorn app.main:app --host 127.0.0.1 --port 808' >/dev/null 2>&1 || true
pkill -f 'test-platform/services/worker.*-m app.main' >/dev/null 2>&1 || true
sleep 1

log "Starting local services"
start_service payments "$ROOT/services/payments" "$RUN_DIR/payments.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_HOST}:4317" \
  DB_URL="postgresql+asyncpg://sentinel:sentinel@${POSTGRES_HOST}:5432/payments_db" \
  REDIS_URL="redis://${REDIS_HOST}:6379/1" \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8082

start_service inventory "$ROOT/services/inventory" "$RUN_DIR/inventory.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_HOST}:4317" \
  DB_URL="postgresql+asyncpg://sentinel:sentinel@${POSTGRES_HOST}:5432/inventory_db" \
  REDIS_URL="redis://${REDIS_HOST}:6379/2" \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8083

start_service orders "$ROOT/services/orders" "$RUN_DIR/orders.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_HOST}:4317" \
  DB_URL="postgresql+asyncpg://sentinel:sentinel@${POSTGRES_HOST}:5432/orders_db" \
  REDIS_URL="redis://${REDIS_HOST}:6379/0" \
  PAYMENTS_URL=http://127.0.0.1:8082 \
  INVENTORY_URL=http://127.0.0.1:8083 \
  ORDERS_STREAM=orders.events \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8081

start_service gateway "$ROOT/services/gateway" "$RUN_DIR/gateway.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_HOST}:4317" \
  ORDERS_URL=http://127.0.0.1:8081 \
  INVENTORY_URL=http://127.0.0.1:8083 \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8080

start_service worker "$ROOT/services/worker" "$RUN_DIR/worker.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT="${OTEL_HOST}:4317" \
  REDIS_URL="redis://${REDIS_HOST}:6379/0" \
  ORDERS_STREAM=orders.events \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m app.main

wait_for_http http://127.0.0.1:8082/health payments
wait_for_http http://127.0.0.1:8083/health inventory
wait_for_http http://127.0.0.1:8081/health orders
wait_for_http http://127.0.0.1:8080/health gateway

log "Running smoke flow"
ORDER_RESPONSE="$(curl -fsS -X POST http://127.0.0.1:8080/api/orders -H 'content-type: application/json' -d '{"sku":"SKU-001","qty":1,"amount":25}')"
ORDER_ID="$("$VENV_PY" - <<'PY' "$ORDER_RESPONSE"
import json
import sys
print(json.loads(sys.argv[1])["order_id"])
PY
)"
curl -fsS "http://127.0.0.1:8080/api/orders/${ORDER_ID}" >"$RUN_DIR/order.json"
curl -fsS http://127.0.0.1:8080/api/inventory/SKU-001 >"$RUN_DIR/inventory.json"

log "Checking worker stream state"
PENDING_JSON="$("$VENV_PY" - <<'PY' "$REDIS_HOST"
import asyncio
import json
import sys
from redis.asyncio import Redis

async def main():
    r = Redis.from_url(f'redis://{sys.argv[1]}:6379/0', decode_responses=True)
    result = None
    for _ in range(20):
        result = await r.xpending('orders.events', 'orders-workers')
        if int(result["pending"]) == 0:
            break
        await asyncio.sleep(1)
    await r.aclose()
    print(json.dumps(result))

asyncio.run(main())
PY
)"
printf '%s\n' "$PENDING_JSON" >"$RUN_DIR/worker-pending.json"
"$VENV_PY" - <<'PY' "$PENDING_JSON"
import json
import sys
payload=json.loads(sys.argv[1])
assert int(payload["pending"]) == 0, payload
PY

log "Checking collector telemetry"
sleep 3
microk8s kubectl -n cos logs pod/otel-collector-0 --tail=500 >"$RUN_DIR/collector.log"
grep -Eq 'ResourceSpans #|ResourceLog #' "$RUN_DIR/collector.log"
grep -q 'service.name: Str(gateway)' "$RUN_DIR/collector.log"
grep -q 'service.name: Str(orders)' "$RUN_DIR/collector.log"

log "Smoke test passed"
printf 'order_id=%s\n' "$ORDER_ID"
printf 'logs=%s\n' "$RUN_DIR"
