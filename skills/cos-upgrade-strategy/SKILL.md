---
name: cos-upgrade-strategy
description: "COS bileşenlerini (Prometheus, Loki, Grafana, Alertmanager, Traefik) kesintisiz veya minimum downtime ile yükseltmek için sıralı güncelleme stratejisini uygulamak gerektiğinde kullan."
---

## Purpose
COS charm yükseltmesi bileşen bağımlılıklarını göz önünde bulundurmalıdır. Özellikle Loki→Alertmanager ve Prometheus→Grafana bağlantıları yükseltme sırasında geçici kopabilir.

## Önerilen yükseltme sırası
1. **Traefik** — ingress değişikliği en az etki
2. **Alertmanager** — alert susturma penceresini aç
3. **Prometheus** — metrik toplama kısa süre durabilir
4. **Loki** — log ingestion toleranslı
5. **Grafana** — UI erişimi son yükseltilir
6. **Tempo** (varsa) — trace pipeline
7. **OTEL Collector** (varsa)

## Charm yükseltme komutu
```bash
juju switch cos
juju refresh traefik-k8s --channel=latest/stable
juju status traefik-k8s --watch 5s  # active/idle bekle
juju refresh alertmanager-k8s --channel=latest/stable
# ...sırayla devam
```

## Alertmanager silence (yükseltme penceresi)
```bash
amtool silence add --alertmanager.url=http://<am-url> \
  --duration=30m --comment="COS upgrade window" severity=warning
```

## Yükseltme öncesi snapshot
```bash
juju run grafana-k8s/0 get-admin-password  # Grafana admin şifresini kaydet
# Prometheus TSDB snapshot (veri kaybı önleme):
curl -X POST http://<prom-url>/api/v1/admin/tsdb/snapshot
```

## Geri alma
```bash
juju refresh grafana-k8s --revision=<önceki-rev>
```

## Common mistakes
- Tüm bileşenleri eş zamanlı yükseltmek — bağımlı relation hook'ları çakışır.
- Grafana'yı ilk yükseltmek; Prometheus datasource kaybolabilir.
- Revision belirtmeden yükseltmek ve hangi sürüme geçildiğini bilmemek.

## References
- `skills/juju-upgrade-charm`
- `skills/cos-bundle-overview`
- `skills/cos-backup-strategy`
