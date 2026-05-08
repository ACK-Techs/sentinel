---
name: cos-custom-charm-relation
description: "Kendi yazdığın FastAPI veya benzeri bir uygulamayı COS observability stack'ine bağlamak için Juju observability relation endpoint'leri eklemek; metrik, log ve trace akışını Charm kodu yazmadan sağlamak gerektiğinde kullan."
---

## Purpose
Özel uygulama charm'larını COS'a bağlamanın en temiz yolu, standart Juju observability library interface'lerini kullanmaktır: `grafana-dashboard`, `metrics-endpoint`, `log-proxy`.

## Mevcut charm'a interface ekleme (charm geliştirme)

### charmcraft.yaml
```yaml
provides:
  metrics-endpoint:
    interface: prometheus_scrape
  grafana-dashboard:
    interface: grafana_dashboard
  logging:
    interface: loki_push_api
  tracing:
    interface: tracing
```

### charm.py (Python Ops)
```python
from charms.prometheus_k8s.v0.prometheus_scrape import MetricsEndpointProvider
from charms.loki_k8s.v1.loki_push_api import LokiPushApiConsumer
from charms.grafana_k8s.v0.grafana_dashboard import GrafanaDashboardProvider

class MyAppCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self._metrics = MetricsEndpointProvider(
            self, jobs=[{"static_configs": [{"targets": ["*:8000"]}]}]
        )
        self._logging = LokiPushApiConsumer(self)
        self._dashboards = GrafanaDashboardProvider(self)
```

## Charm olmayan uygulama (doğrudan Kubernetes pod)
```bash
# ServiceMonitor ile scrape:
kubectl apply -f servicemonitor.yaml  # Prometheus Operator varsa
# OTEL SDK ile OTLP gönder → OTEL Collector charm'ına

# COS offer'a bağlan:
juju integrate myapp:metrics-endpoint admin/cos.prometheus-remote-write
```

## Grafana dashboard ekleme
```python
# Charm'ın src/grafana_dashboards/ dizininde JSON dosyası bırak
# GrafanaDashboardProvider otomatik iletir
```

## Common mistakes
- Interface library versiyonunu (v0, v1) yanlış seçmek — provider ve consumer versiyonu eşleşmelidir.
- `logging` endpoint'ini ekleyip uygulamanın OTLP log SDK'sını yapılandırmamak.

## References
- `skills/cos-bundle-overview`
- `skills/cos-relation-otel-prometheus`
- `skills/juju-relation-add-remove`
- `skills/obs-otel-sdk-python`
