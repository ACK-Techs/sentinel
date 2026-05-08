---
name: platform-paved-road
description: "Sentinel platform ekibi için paved road (altın yol) tasarımı; servis geliştirme standartları ve golden path oluşturma"
---

## Purpose
Paved road, geliştiricilerin en iyi pratiklere uymaları için en kolay yolu seçmelerine olanak tanıyan önceden inşa edilmiş altyapı ve araçlar bütünüdür. Sentinel bağlamında bu; OTEL bootstrap, chaos middleware, health endpoint ve Kubernetes manifest şablonlarının hazır paket halinde sunulmasıdır.

## Workflow

### 1. Sentinel golden path bileşenleri

```
Platform Paved Road
├── libs/observability/     ← OTEL setup library (tek satır import)
├── libs/chaos/             ← Chaos middleware (plug-and-play)
├── libs/health/            ← /health, /ready, /metrics endpoints
├── libs/auth/              ← JWT validation middleware
├── templates/service/      ← Cookiecutter service skeleton
└── helm/base-service/      ← Ortak Helm chart değerleri
```

### 2. Observability kütüphanesi
```python
# libs/observability/__init__.py
from .setup import setup_observability, get_meter, get_tracer

# Servis main.py'de tek satır:
from libs.observability import setup_observability
setup_observability("my-service")
# → OTEL exporter, resource attributes, auto-instrumentation hazır
```

### 3. Servis skeleton oluşturma
```bash
# Cookiecutter ile yeni servis iskeleti
cookiecutter templates/service/ \
  --no-input \
  service_name=notifications \
  port=8005 \
  with_postgres=true \
  with_redis=false

# Üretilen yapı:
# services/notifications/
# ├── app/main.py          ← OTEL + chaos + health dahil
# ├── app/routes/
# ├── Dockerfile
# ├── helm/
# ├── catalog-info.yaml
# └── tests/
```

### 4. Base Helm chart değerleri
```yaml
# helm/base-service/values.yaml
# Tüm servisler bu değerleri miras alır
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"

livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5

podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

### 5. Platform contract (kaçınılamaz kurallar)
```markdown
Her Sentinel target servisi:
1. `libs.observability.setup_observability()` import eder
2. `/health`, `/ready`, `/metrics` endpoint'leri sunar
3. `libs.chaos` middleware'ini içerir
4. `catalog-info.yaml` ile Backstage'e kayıtlıdır
5. Helm `base-service` chart'ını miras alır

Bu kurallar `make lint` ile otomatik kontrol edilir.
```

### 6. Paved road uyumluluk kontrolü
```bash
# scripts/check_paved_road.py
for svc_dir in services/*/; do
  svc=$(basename $svc_dir)
  echo "=== $svc ==="
  
  # OTEL import kontrolü
  grep -q "setup_observability" $svc_dir/app/main.py && \
    echo "  ✓ OTEL" || echo "  ✗ OTEL MISSING"
  
  # Health endpoint kontrolü
  grep -q "/health" $svc_dir/app/main.py && \
    echo "  ✓ health" || echo "  ✗ health MISSING"
  
  # catalog-info.yaml
  [ -f "$svc_dir/catalog-info.yaml" ] && \
    echo "  ✓ catalog" || echo "  ✗ catalog MISSING"
done
```

## Common mistakes
1. Paved road'u zorlama politikası olmadan "öneri" olarak bırakmak — servislerin yarısı uymaz.
2. Kütüphaneyi güncellemeyi duyurmadan servisleri kırmak — semver + deprecation notice gerekli.
3. Golden path'i tek platformcu bilirse — onboarding'e dahil et, dokümante et.
4. Kütüphane API'sini çok sık değiştirmek — servis ekipleri her sürümde uyum sağlamak zorunda kalır.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/platform-idp-backstage`
- `skills/platform-service-catalog`
