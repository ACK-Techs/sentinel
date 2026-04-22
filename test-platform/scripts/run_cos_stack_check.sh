#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
VENV_PY="$REPO_ROOT/.venv/bin/python"
VENV_PIP="$REPO_ROOT/.venv/bin/pip"
CLI_DIR="$REPO_ROOT/cli"
OBS_GATEWAY_DIR="$REPO_ROOT/observability-gateway"
OBS_GATEWAY_TOKEN="${OBS_GATEWAY_TOKEN:-sentinel-observability-gateway-token}"
RUN_DIR="$ROOT/runs/cos-smoke-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$RUN_DIR"

PORT_FORWARD_PIDS=()
SERVICE_PIDS=()

log() {
  printf '[cos-smoke] %s\n' "$1"
}

cleanup() {
  set +e
  for pid in "${SERVICE_PIDS[@]:-}"; do
    kill "$pid" >/dev/null 2>&1 || true
  done
  for pid in "${PORT_FORWARD_PIDS[@]:-}"; do
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
  echo "$name tcp did not become ready: $host:$port" >&2
  exit 1
}

start_pf() {
  local namespace="$1"
  local target="$2"
  local ports="$3"
  local logfile="$4"
  microk8s kubectl -n "$namespace" port-forward "$target" "$ports" >"$logfile" 2>&1 &
  PORT_FORWARD_PIDS+=("$!")
}

start_service() {
  local workdir="$1"
  local logfile="$2"
  shift 2
  (
    cd "$workdir"
    env "$@" >"$logfile" 2>&1
  ) &
  SERVICE_PIDS+=("$!")
}

query_window_start_ns() {
  "$VENV_PY" - <<'PY'
import time
print(int((time.time() - 1800) * 1e9))
PY
}

query_window_end_ns() {
  "$VENV_PY" - <<'PY'
import time
print(int(time.time() * 1e9))
PY
}

require_cmd microk8s
require_cmd juju
require_cmd curl
require_cmd pkill

if [[ ! -x "$VENV_PY" ]]; then
  echo "Missing virtualenv python: $VENV_PY" >&2
  exit 1
fi

log "Checking cluster and model health"
microk8s status --wait-ready >"$RUN_DIR/microk8s-status.txt"
if ! timeout 30 juju status >"$RUN_DIR/juju-status.txt"; then
  log "juju status timed out; continuing smoke with existing cluster state"
  printf 'juju status timed out after 30s\n' >>"$RUN_DIR/juju-status.txt"
fi

log "Installing editable packages into repo venv"
"$VENV_PIP" install -e "$REPO_ROOT/observability-gateway" \
  -e "$CLI_DIR" \
  >/dev/null
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

log "Stopping previous local test-platform processes if any"
pkill -f 'test-platform/services/.*/uvicorn app.main:app --host 127.0.0.1 --port 808' >/dev/null 2>&1 || true
pkill -f 'test-platform/services/worker.*-m app.main' >/dev/null 2>&1 || true
pkill -f 'uvicorn observability_gateway.main:app --host 127.0.0.1 --port 8091' >/dev/null 2>&1 || true
sleep 1

log "Starting port-forwards"
start_pf sentinel-target svc/postgres 5432:5432 "$RUN_DIR/pf-postgres.log"
start_pf sentinel-target svc/redis 6379:6379 "$RUN_DIR/pf-redis.log"
start_pf cos svc/otel-collector 4317:4317 "$RUN_DIR/pf-otel.log"
start_pf cos svc/prometheus 9090:9090 "$RUN_DIR/pf-prometheus.log"
start_pf cos svc/loki 3100:3100 "$RUN_DIR/pf-loki.log"
start_pf cos svc/tempo 3200:3200 "$RUN_DIR/pf-tempo.log"
wait_for_tcp 127.0.0.1 5432 postgres-port-forward
wait_for_tcp 127.0.0.1 6379 redis-port-forward
wait_for_tcp 127.0.0.1 4317 otel-port-forward
wait_for_tcp 127.0.0.1 9090 prometheus-port-forward
wait_for_tcp 127.0.0.1 3100 loki-port-forward
wait_for_tcp 127.0.0.1 3200 tempo-port-forward

log "Seeding databases"
export ORDERS_DB_URL='postgresql+asyncpg://sentinel:sentinel@127.0.0.1:5432/orders_db'
export PAYMENTS_DB_URL='postgresql+asyncpg://sentinel:sentinel@127.0.0.1:5432/payments_db'
export INVENTORY_DB_URL='postgresql+asyncpg://sentinel:sentinel@127.0.0.1:5432/inventory_db'
export PAYMENTS_REDIS_URL='redis://127.0.0.1:6379/1'
"$VENV_PY" "$ROOT/scripts/seed_db.py"

log "Starting local services against COS"
start_service "$ROOT/services/payments" "$RUN_DIR/payments.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4317 \
  DB_URL=postgresql+asyncpg://sentinel:sentinel@127.0.0.1:5432/payments_db \
  REDIS_URL=redis://127.0.0.1:6379/1 \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8082

start_service "$ROOT/services/inventory" "$RUN_DIR/inventory.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4317 \
  DB_URL=postgresql+asyncpg://sentinel:sentinel@127.0.0.1:5432/inventory_db \
  REDIS_URL=redis://127.0.0.1:6379/2 \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8083

start_service "$ROOT/services/orders" "$RUN_DIR/orders.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4317 \
  DB_URL=postgresql+asyncpg://sentinel:sentinel@127.0.0.1:5432/orders_db \
  REDIS_URL=redis://127.0.0.1:6379/0 \
  PAYMENTS_URL=http://127.0.0.1:8082 \
  INVENTORY_URL=http://127.0.0.1:8083 \
  ORDERS_STREAM=orders.events \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8081

start_service "$ROOT/services/gateway" "$RUN_DIR/gateway.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4317 \
  ORDERS_URL=http://127.0.0.1:8081 \
  INVENTORY_URL=http://127.0.0.1:8083 \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8080

start_service "$ROOT/services/worker" "$RUN_DIR/worker.log" \
  OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4317 \
  REDIS_URL=redis://127.0.0.1:6379/0 \
  ORDERS_STREAM=orders.events \
  CHAOS_TOKEN=sentinel-chaos-token \
  "$VENV_PY" -m app.main

wait_for_http http://127.0.0.1:8082/health payments
wait_for_http http://127.0.0.1:8083/health inventory
wait_for_http http://127.0.0.1:8081/health orders
wait_for_http http://127.0.0.1:8080/health gateway

log "Starting observability gateway"
start_service "$OBS_GATEWAY_DIR" "$RUN_DIR/observability-gateway.log" \
  SENTINEL_OBSERVABILITY_GATEWAY_TOKEN="$OBS_GATEWAY_TOKEN" \
  SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL=http://127.0.0.1:9090 \
  SENTINEL_OBSERVABILITY_LOKI__BASE_URL=http://127.0.0.1:3100 \
  SENTINEL_OBSERVABILITY_TEMPO__BASE_URL=http://127.0.0.1:3200 \
  SENTINEL_OBSERVABILITY_HTTP__TIMEOUT_SEC=10 \
  "$VENV_PY" -m uvicorn observability_gateway.main:app --host 127.0.0.1 --port 8091
local_gateway_health_retries=60
while (( local_gateway_health_retries > 0 )); do
  if curl -fsS http://127.0.0.1:8091/health \
    -H "Authorization: Bearer $OBS_GATEWAY_TOKEN" >/dev/null 2>&1; then
    log "observability-gateway is ready"
    break
  fi
  local_gateway_health_retries=$((local_gateway_health_retries - 1))
  sleep 1
done
if (( local_gateway_health_retries == 0 )); then
  echo "observability-gateway did not become ready: http://127.0.0.1:8091/health" >&2
  exit 1
fi

log "Generating traffic"
ORDER_RESPONSE="$(curl -fsS -X POST http://127.0.0.1:8080/api/orders -H 'content-type: application/json' -d '{"sku":"SKU-001","qty":1,"amount":25}')"
ORDER_ID="$("$VENV_PY" - <<'PY' "$ORDER_RESPONSE"
import json
import sys
print(json.loads(sys.argv[1])["order_id"])
PY
)"
curl -fsS "http://127.0.0.1:8080/api/orders/${ORDER_ID}" >"$RUN_DIR/order.json"
curl -fsS http://127.0.0.1:8080/api/inventory/SKU-001 >"$RUN_DIR/inventory.json"
for _ in $(seq 1 5); do
  curl -fsS -X POST http://127.0.0.1:8080/api/orders -H 'content-type: application/json' -d '{"sku":"SKU-001","qty":1,"amount":25}' >/dev/null
  curl -fsS http://127.0.0.1:8080/api/inventory/SKU-001 >/dev/null
done

log "Checking worker stream state"
PENDING_JSON="$("$VENV_PY" - <<'PY'
import asyncio
import json
from redis.asyncio import Redis

async def main():
    r = Redis.from_url('redis://127.0.0.1:6379/0', decode_responses=True)
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
payload = json.loads(sys.argv[1])
assert int(payload["pending"]) == 0, payload
PY

log "Waiting for metric export"
sleep 20

log "Checking Prometheus"
curl -fsS 'http://127.0.0.1:9090/api/v1/query?query=target_info' >"$RUN_DIR/prom-target-info.json"
curl -fsS 'http://127.0.0.1:9090/api/v1/query?query=app_orders_created_total' >"$RUN_DIR/prom-orders-created.json"
grep -q '"job":"gateway"' "$RUN_DIR/prom-target-info.json"
grep -q '"job":"orders"' "$RUN_DIR/prom-target-info.json"
grep -q '"job":"payments"' "$RUN_DIR/prom-target-info.json"
grep -q '"job":"inventory"' "$RUN_DIR/prom-target-info.json"
grep -q '"job":"worker"' "$RUN_DIR/prom-target-info.json"
grep -q '"app_orders_created_total"' "$RUN_DIR/prom-orders-created.json"

log "Checking Loki"
curl -fsS 'http://127.0.0.1:3100/loki/api/v1/label/job/values' >"$RUN_DIR/loki-job-values.json"
curl -G -fsS \
  --data-urlencode 'query={job="gateway"}' \
  --data-urlencode 'limit=5' \
  --data-urlencode "start=$(query_window_start_ns)" \
  --data-urlencode "end=$(query_window_end_ns)" \
  http://127.0.0.1:3100/loki/api/v1/query_range >"$RUN_DIR/loki-gateway.json"
grep -q '"gateway"' "$RUN_DIR/loki-job-values.json"
grep -q 'HTTP Request:' "$RUN_DIR/loki-gateway.json"

log "Checking Tempo"
curl -fsS 'http://127.0.0.1:3200/api/search/tags' >"$RUN_DIR/tempo-tags.json"
curl -fsS 'http://127.0.0.1:3200/api/search?limit=5&tags=service.name%3Dorders' >"$RUN_DIR/tempo-orders.json"
grep -q '"service.name"' "$RUN_DIR/tempo-tags.json"
grep -q '"traceID"' "$RUN_DIR/tempo-orders.json"

log "Checking observability gateway"
curl -fsS http://127.0.0.1:8091/health \
  -H "Authorization: Bearer $OBS_GATEWAY_TOKEN" >"$RUN_DIR/observability-gateway-health.json"
curl -fsS http://127.0.0.1:8091/api/v1/status \
  -H "Authorization: Bearer $OBS_GATEWAY_TOKEN" >"$RUN_DIR/observability-gateway-status.json"
grep -q '"status":"ok"' "$RUN_DIR/observability-gateway-health.json"
grep -q '"prometheus"' "$RUN_DIR/observability-gateway-status.json"
grep -q '"loki"' "$RUN_DIR/observability-gateway-status.json"
grep -q '"tempo"' "$RUN_DIR/observability-gateway-status.json"

log "Checking Sentinel CLI through observability gateway"
(
  cd "$CLI_DIR"
  SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091 \
  SENTINEL_OBSERVABILITY_GATEWAY_TOKEN="$OBS_GATEWAY_TOKEN" \
  "$VENV_PY" -m sentinel_cli doctor --profile local
) >"$RUN_DIR/cli-doctor.json"
(
  cd "$CLI_DIR"
  SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091 \
  SENTINEL_OBSERVABILITY_GATEWAY_TOKEN="$OBS_GATEWAY_TOKEN" \
  "$VENV_PY" -m sentinel_cli obs metric 'app_orders_created_total'
) >"$RUN_DIR/cli-obs-metric.json"
(
  cd "$CLI_DIR"
  SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091 \
  SENTINEL_OBSERVABILITY_GATEWAY_TOKEN="$OBS_GATEWAY_TOKEN" \
  "$VENV_PY" -m sentinel_cli obs logs --service gateway
) >"$RUN_DIR/cli-obs-logs.json"
(
  cd "$CLI_DIR"
  SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091 \
  SENTINEL_OBSERVABILITY_GATEWAY_TOKEN="$OBS_GATEWAY_TOKEN" \
  "$VENV_PY" -m sentinel_cli obs traces --service orders
) >"$RUN_DIR/cli-obs-traces.json"
(
  cd "$CLI_DIR"
  SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL=http://127.0.0.1:8091 \
  SENTINEL_OBSERVABILITY_GATEWAY_TOKEN="$OBS_GATEWAY_TOKEN" \
  SENTINEL_TRAJECTORY_ENABLED=1 \
  SENTINEL_TRAJECTORY_DIR="$RUN_DIR/agent-trajectories" \
  "$VENV_PY" - <<'PY'
import contextlib
import io
import json
from pathlib import Path

import sentinel_cli.cli.app as app
from sentinel_cli.llm.types import CompletionResult, ToolCall


class ScriptedProvider:
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, request):
        self.calls += 1
        if self.calls == 1:
            return CompletionResult(
                text="Gateway araciyla log sorgusu baslatiliyor.",
                tool_calls=[
                    ToolCall(
                        id="obs-smoke-1",
                        name="obs_logs_query",
                        arguments_json=json.dumps({"service": "gateway", "limit": 5}),
                    )
                ],
                provider_name="smoke-scripted",
            )
        return CompletionResult(
            text="Gateway loglari icin agentik smoke tamamlandi.",
            provider_name="smoke-scripted",
        )

    def stream(self, request):
        raise NotImplementedError


def fake_build_provider(config, resolved_profile):
    del config, resolved_profile
    return ScriptedProvider()


trajectory_dir = Path("agent-trajectories")
before = set(trajectory_dir.glob("*.jsonl"))
app.build_provider = fake_build_provider

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    exit_code = app.main(
        ["run", "--profile", "local", "gateway loglarinda son 5 dakikayi ozetle"]
    )

after = set(trajectory_dir.glob("*.jsonl"))
new_files = sorted(str(path.name) for path in (after - before))
trajectory_content = ""
if new_files:
    trajectory_content = (trajectory_dir / new_files[0]).read_text(encoding="utf-8")

print(
    json.dumps(
        {
            "exit_code": exit_code,
            "stdout": buffer.getvalue(),
            "trajectory_files": new_files,
            "trajectory": trajectory_content,
        },
        ensure_ascii=True,
    )
)
PY
) >"$RUN_DIR/cli-agent-run.json"
grep -q '"observability_gateway"' "$RUN_DIR/cli-doctor.json"
grep -q '"backend": "prometheus"' "$RUN_DIR/cli-obs-metric.json"
grep -q '"backend": "loki"' "$RUN_DIR/cli-obs-logs.json"
grep -q '"backend": "tempo"' "$RUN_DIR/cli-obs-traces.json"
grep -q '"exit_code": 0' "$RUN_DIR/cli-agent-run.json"
grep -q '"tool_name": "obs_logs_query"' "$RUN_DIR/cli-agent-run.json"
grep -q 'Gateway loglari icin agentik smoke tamamlandi.' "$RUN_DIR/cli-agent-run.json"

log "COS smoke test passed"
printf 'order_id=%s\n' "$ORDER_ID"
printf 'logs=%s\n' "$RUN_DIR"
