---
name: fastapi-deployment
description: "FastAPI üretim deployment (gunicorn+uvicorn, Docker, K8s) — Sentinel gateway servisinin production hazırlanması"
---

## Purpose
FastAPI'yi production'da çalıştırmak; single worker uvicorn'dan gunicorn+uvicorn worker pool'a, Docker image optimizasyonuna ve Kubernetes deployment konfigürasyonuna kadar birden fazla katman gerektirir. Sentinel'in gateway servisi bu adımların tümünü uygular.

## Workflow

### 1. gunicorn + uvicorn worker

```python
# gunicorn.conf.py
import multiprocessing

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

```bash
gunicorn app.main:app -c gunicorn.conf.py
```

### 2. Dockerfile (multi-stage, minimal)

```dockerfile
# Builder
FROM python:3.11-slim AS builder
WORKDIR /build
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Runtime
FROM python:3.11-slim AS runtime
RUN useradd --uid 1001 --no-create-home sentinel
WORKDIR /app

COPY --from=builder /build/.venv /app/.venv
COPY src/ /app/src/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER sentinel
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health').raise_for_status()"

CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
```

### 3. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinel-gateway
  labels:
    app: sentinel-gateway
    version: "1.0.0"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentinel-gateway
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    spec:
      containers:
      - name: gateway
        image: registry.internal/sentinel-gateway:1.0.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "1000m"
            memory: "512Mi"
        env:
        - name: SENTINEL_ENVIRONMENT
          value: "production"
        envFrom:
        - secretRef:
            name: sentinel-gateway-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 15
      terminationGracePeriodSeconds: 30
```

### 4. Graceful shutdown

```python
# main.py
import signal
import asyncio

async def graceful_shutdown():
    """SIGTERM alındığında aktif isteklerin bitmesini bekle."""
    await asyncio.sleep(5)  # Load balancer'ın deregister etmesini bekle

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Shutdown
    await graceful_shutdown()
    await cleanup_resources()
```

### 5. HPA (Horizontal Pod Autoscaler)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sentinel-gateway-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sentinel-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## Common mistakes

- `uvicorn app.main:app` ile tek worker production'da çalıştırmak — HPA pod çoğaltsa da her pod tek CPU core kullanır
- Docker image'a `.venv` yerine sistem Python paketleri kurmak — image boyutu gereksiz büyür
- `preload_app = True` ile gunicorn'da async lifespan olmadan çalışmak — fork sonrası event loop sorunları çıkabilir
- `terminationGracePeriodSeconds` < gunicorn timeout — pod kapanmadan önce istekler kesilir

## References
- `skills/fastapi-health-checks`
- `skills/fastapi-lifespan`
- `skills/fastapi-observability`
