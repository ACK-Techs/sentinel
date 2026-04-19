---
name: target-app-repo-layout
description: Sentinel Faz-1 test platformu monorepo alt-ağacı (test-platform/) ve per-service iskelet kuralları.
---

## Purpose
Sentinel'in gözlemleyeceği çok-servisli test platformunun **repo-içi konumu ve iskeletini** standartlaştırmak. Tüm servisler aynı layout'u takip etmeli ki observability, chaos ve k8s manifestleri tek şablondan türetilebilsin.

## When to Use
- Yeni bir test servisi eklerken (ör. `notifications`).
- Mevcut servise route/client dosyası koyarken.
- CI/CD, Dockerfile veya k8s manifestleri yazmadan önce yolları doğrulamak için.

## Contract / Interface
Kök dizin: `test-platform/`
```
test-platform/
  services/
    gateway/        orders/         payments/
    inventory/      worker/
  libs/observability/    # shared OTEL setup (see target-app-observability-lib)
  load/                   # locust scenarios (see target-app-load-generator)
  chaos/                  # chaos profile yaml + ConfigMap source
  k8s/                    # kustomize base + overlays (sentinel-target ns)
  scripts/                # scenario_runner.py, ground-truth tooling
```
Her servis için zorunlu dosyalar:
```
services/<name>/
  app/
    main.py              # FastAPI entrypoint; first line: setup_observability(...)
    routes/              # business endpoints + /admin/chaos
    clients/             # httpx clients with timeouts (otel auto-instrumented)
    config.py            # pydantic-settings, reads OTEL_* and DB_URL env
  Dockerfile             # python:3.12-slim base, non-root UID 10001
  pyproject.toml         # OR requirements.txt — pick one and stick to it
  README.md              # service contract summary (routes, deps)
```

## Implementation Notes
- `libs/observability` **pip-installable** olarak tüketilir (`pip install -e ../../libs/observability`) veya `PYTHONPATH` üzerinden mount; tek kaynak.
- `worker` servisinde `app/main.py` yerine `app/worker.py` kabul edilir ama `main.py` giriş noktası olarak da bir `__main__` export eder.
- Her Dockerfile **multi-stage** (builder + runtime), `USER 10001`, `EXPOSE 8000`.
- `pyproject.toml` tercih ediliyorsa Python sürümü `>=3.11`, bağımlılıklar `[project.dependencies]`.
- Servisler arası import yasak — sadece `libs/observability` paylaşılır. İletişim HTTP üzerinden.

## Anti-patterns
1. Servisler arası doğrudan Python import (`from services.orders import ...`) — topoloji HTTP olmalı.
2. Her servisin kendi OTEL setup'ını yazması — `libs/observability` dışına çıkılmaz.
3. `requirements.txt` ve `pyproject.toml`'u aynı serviste birlikte bulundurmak (çakışan bağımlılıklar).
4. Chaos veya load kodunu `services/` altına koymak — ayrı `chaos/` / `load/` klasörlerine ait.
5. Dockerfile'da root user — k8s PodSecurity 'restricted' ile çakışır.

## Example Snippet
```
test-platform/services/orders/
├── Dockerfile
├── pyproject.toml
└── app/
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── routes/
    │   ├── orders.py
    │   └── admin_chaos.py
    └── clients/
        ├── payments.py
        └── inventory.py
```
```dockerfile
# services/orders/Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml ./
RUN pip wheel --wheel-dir /wheels .

FROM python:3.12-slim
RUN useradd -u 10001 -m app
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels orders
USER 10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
