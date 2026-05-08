---
name: cos-relation-otel-prometheus
description: "OTEL Collector charm'ını Prometheus'a scrape hedefi olarak bağlamak, OTLP üzerinden gelen metriklerin Prometheus'ta görünmesini sağlamak ve metric akışını doğrulamak gerektiğinde kullan."
---

## Purpose
OTEL Collector, OTLP metrikleri alır ve Prometheus uyumlu `/metrics` endpoint'i sunar. Bu relation, Prometheus'un OTEL Collector'ı otomatik scrape hedefi olarak tanımasını sağlar.

## Relation kurulumu
```bash
juju switch cos
juju integrate opentelemetry-collector-k8s:metrics-endpoint prometheus-k8s:metrics-endpoint
```

## Doğrulama
```bash
# Prometheus hedefler:
curl http://<prometheus-url>/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job | contains("opentelemetry"))'

# OTEL Collector kendi metrikleri geliyor mu:
curl http://<prometheus-url>/api/v1/query?query=otelcol_receiver_accepted_metric_points
```

## Uygulama metriklerinin akışı
```
Uygulama (OTLP/gRPC 4317) → OTEL Collector (Prometheus exporter) → Prometheus scrape
```

OTEL Collector Prometheus exporter config (charm'ın yönettiği):
- endpoint: `0.0.0.0:8889` (varsayılan)
- Juju relation üzerinden Prometheus'a otomatik duyurulur

## Metrik adı dönüşümü
OTLP metrik adları Prometheus için normalize edilir:
- `myapp.request.duration` → `myapp_request_duration_seconds`
- Nokta → alt çizgi; birim suffix eklenir

## Common mistakes
- OTEL SDK'nın metric SDK'sını başlatmadan OTLP metrik göndermeye çalışmak.
- Prometheus scrape interval (varsayılan 60s) ile metriğin hemen görünmesini beklemek.
- Label adlarında OTLP semantic conventions ile Prometheus label kuralları arasındaki farkı göz ardı etmek.

## References
- `skills/cos-deploy-otel-collector`
- `skills/cos-bundle-overview`
- `skills/obs-otel-collector-exporters`
- `skills/obs-prometheus-scrape-config`
