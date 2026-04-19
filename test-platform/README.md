# Sentinel Test Platform

Phase 1 target application tree for Sentinel. It provides four FastAPI services, one Redis Streams worker, load generation, chaos profiles, Docker Compose, and Kubernetes manifests under `test-platform/`.

## Services

- `gateway`: public-ish API on `:8080`
- `orders`: orchestrates payments + inventory, writes Postgres, emits `orders.events`
- `payments`: payment simulation with Redis idempotency
- `inventory`: stock reads and reservations with cache-through Redis
- `worker`: Redis Streams consumer group processor

## Local Run

1. `docker compose up --build`
2. `export ORDERS_DB_URL=postgresql+asyncpg://sentinel:sentinel@localhost:5432/orders_db`
3. `export PAYMENTS_DB_URL=postgresql+asyncpg://sentinel:sentinel@localhost:5432/payments_db`
4. `export INVENTORY_DB_URL=postgresql+asyncpg://sentinel:sentinel@localhost:5432/inventory_db`
5. `export PAYMENTS_REDIS_URL=redis://localhost:6379/1`
6. `python scripts/seed_db.py`
7. `curl http://localhost:8080/health`
8. `curl http://localhost:8081/health`
9. `curl http://localhost:8082/health`
10. `curl http://localhost:8083/health`

## Chaos

Admin endpoints require `X-Chaos-Token`. `/admin/*` and `/health` are excluded from chaos middleware.

## Ground Truth

Use `python scripts/scenario_runner.py run <scenario.yaml>` to execute a run and append records to `ground-truth.jsonl`.
