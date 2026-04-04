---
name: cos-relation-prometheus-grafana
description: prometheus-k8s ile grafana-k8s arasındaki grafana-source ve grafana-dashboard entegrasyon uçlarını ve kurallarını tanımlar.
---

## Purpose
Prometheus metriklerinin Grafana’da **veri kaynağı** ve **hazır panolar** olarak görünmesini sağlayan Juju integration’larını doğru uç adlarıyla kullanmak.

## Rules
- Bundle içinde otomatik: `prometheus:grafana-source` → `grafana:grafana-source`; `prometheus:grafana-dashboard` → `grafana:grafana-dashboard` (arayüz adları dokümana göre `grafana_datasource` / `grafana_dashboard`).
- Manuel entegrasyon (Juju 3.6): `juju integrate prometheus:grafana-source grafana:grafana-source` ve `juju integrate prometheus:grafana-dashboard grafana:grafana-dashboard` — `relate` bu komutun takma adıdır; uygulama adları `juju status` ile aynı olmalıdır.
- Prometheus ayrıca `metrics-endpoint` ile Grafana’nın kendisini scrape edebilir (stack içi metrikler).
- Sorun giderme: [Troubleshoot no data in Grafana panels](https://documentation.ubuntu.com/observability/how-to/troubleshooting/troubleshoot-no-data-in-grafana-panels/).

## References
- `skills/cos-deploy-prometheus`, `skills/cos-deploy-grafana`
- `documantations/ARCHITECTURE_COS.md`
