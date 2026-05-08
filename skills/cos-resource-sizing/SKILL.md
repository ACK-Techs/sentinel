---
name: cos-resource-sizing
description: "COS bileşenleri (Prometheus, Loki, Grafana, Alertmanager, Tempo) için CPU/memory/disk kaynak talebini iş yükü büyüklüğüne göre tahmin etmek ve Juju constraints ile uygulamak gerektiğinde kullan."
---

## Purpose
Yetersiz resource = OOM kill veya scrape gecikmesi. Fazla resource = gereksiz maliyet. Başlangıç değerleri ve büyüme formülleri:

## Prometheus

| Metrik sayısı | CPU | Memory | Disk/ay |
|---|---|---|---|
| <10K | 100m | 512Mi | 5GB |
| 10K–100K | 500m | 2Gi | 20GB |
| >100K | 1–2 | 4–8Gi | 50+GB |

Disk = `samples_per_second × bytes_per_sample(1.5) × retention_seconds`

## Loki

| Log hacmi | Memory | Disk/gün |
|---|---|---|
| <1 GB/gün | 256Mi | 1GB |
| 1–10 GB/gün | 1–2Gi | 10GB |
| >10 GB/gün | 4Gi+ | 10+GB |

## Grafana
- Genellikle 200m CPU / 256Mi yeterli
- Yoğun dashboard sorgusu: 500m / 512Mi

## Alertmanager
- Düşük yük: 50m / 64Mi; HA cluster: 100m / 128Mi × 3

## Tempo
- Trace hacmine göre: 10M trace/gün ≈ 1 GB/gün storage

## Juju ile uygulama
```bash
juju deploy prometheus-k8s --constraints "mem=2G cores=1"
# veya charm config ile resource request:
juju config prometheus-k8s cpu=500m memory=2Gi
```

## Kaynak izleme
```promql
container_memory_working_set_bytes{namespace="cos"}
rate(container_cpu_usage_seconds_total{namespace="cos"}[5m])
```

## Common mistakes
- Grafana dashboard sorgularının Prometheus'a yük bindirdiğini hesaba katmamak.
- Loki için retention ayarlamadan disk'in dolmasını beklemek.

## References
- `skills/cos-bundle-overview`
- `skills/k8s-core-resource-requests-limits`
- `skills/obs-prometheus-capacity-planning`
