---
name: cos-observability-self-monitoring
description: "COS bileşenlerinin kendi sağlığını izlemek için self-monitoring dashboard ve alert kurmak, 'observability stack kendisi çöktüğünde' durumunu tespit etmek gerektiğinde kullan."
---

## Purpose
COS'un izlediği şeyler kadar COS'un kendisini izlemek de önemlidir. Prometheus'un scrape health'i, Loki'nin ingestion durumu ve Alertmanager pipeline sağlığı izlenmezse sessiz hatalar oluşur.

## Prometheus self-monitoring metrikleri
```promql
# Scrape başarısızlıkları:
sum by(job) (up == 0)

# Query gecikme p99:
histogram_quantile(0.99, prometheus_http_request_duration_seconds_bucket{handler="/api/v1/query"})

# TSDB head chunk boyutu (bellek baskısı):
prometheus_tsdb_head_chunks

# Kural değerlendirme süresi:
rate(prometheus_rule_evaluation_duration_seconds_sum[5m]) / rate(prometheus_rule_evaluation_duration_seconds_count[5m])
```

## Loki self-monitoring
```promql
# Ingestion hızı:
sum(rate(loki_distributor_bytes_received_total[5m]))

# Hata oranı:
sum(rate(loki_distributor_ingester_appends_failures_total[5m]))
```

## Alertmanager pipeline sağlığı
```promql
# İşlenmiş alert sayısı (sıfır = problem):
rate(alertmanager_alerts_received_total[5m])

# Bildirim hataları:
rate(alertmanager_notifications_failed_total[5m])
```

## Grafana dashboard önerisi
COS self-monitoring için ayrı bir Grafana folder oluştur: "COS Health". Her bileşen için 1 stat paneli (UP/DOWN) + temel latency/error grafiği.

## Alert örnekleri
```yaml
- alert: PrometheusDown
  expr: up{job="prometheus"} == 0
  for: 1m
  annotations:
    summary: "Prometheus erişilemiyor"

- alert: LokiHighIngestErrors
  expr: rate(loki_distributor_ingester_appends_failures_total[5m]) > 0.01
  for: 5m
```

## Common mistakes
- COS metrikleri için Prometheus'un kendisini scrape ettiğini varsaymak — açık yapılandırma gerekir.
- Self-monitoring alert'leri Alertmanager'a göndermek; Alertmanager çökünceki alert teslim edilemez. Harici webhook veya ayrı monitoring channel kullan.

## References
- `skills/cos-bundle-overview`
- `skills/obs-prometheus-alerting-rules`
- `skills/obs-grafana-alerting-unified`
