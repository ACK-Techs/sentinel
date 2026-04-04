---
name: cos-deploy-alertmanager
description: alertmanager-k8s charm’ı için dağıtım; Prometheus/Loki uyarıları ve Traefik ingress kurallarını kapsar.
---

## Purpose
**Uyarı yönlendirme** ve COS içi uyarı entegrasyonu için `alertmanager-k8s` bileşenini doğru ilişkilerle çalıştırmak.

## Rules
- Charm adı: **`alertmanager-k8s`** ([Charmhub](https://charmhub.io/alertmanager-k8s)).
- Bundle: `juju deploy cos-lite --trust` — `alertmanager:alerting` hem `loki` hem `prometheus` ile `alertmanager_dispatch` benzeri uçlarda bağlanır (çıktıda `alertmanager_dispatch`).
- Traefik: `traefik:ingress` → `alertmanager:ingress` (app ingress).
- Grafana: `grafana-dashboard`, `grafana-source` ile pano/kaynak sağlanır.
- Prometheus self-scrape: `alertmanager:self-metrics-endpoint` → `prometheus:metrics-endpoint`.
- Alıcı yapılandırması: upstream [Alertmanager config](https://prometheus.io/docs/alerting/latest/configuration/) ve charm config anahtarları (sürüme göre `juju config alertmanager`).

## References
- `skills/cos-deploy-prometheus`, `skills/cos-deploy-loki`, `skills/cos-deploy-grafana`
- `skills/cos-ingress-config`
