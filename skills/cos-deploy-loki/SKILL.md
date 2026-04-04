---
name: cos-deploy-loki
description: loki-k8s charm’ı veya cos-lite içindeki Loki için kanal, trust ve ingress-per-unit kurallarını tanımlar.
---

## Purpose
**Log aggregation** için `loki-k8s` bileşenini COS mimarisine uygun şekilde konuşlandırmak.

## Rules
- Charm adı: **`loki-k8s`** ([Charmhub](https://charmhub.io/loki-k8s)).
- Bundle ile: `juju deploy cos-lite --trust` — Loki PVC ve Traefik **ingress-per-unit** ile birlikte gelir.
- Ayrı deploy: `juju deploy loki-k8s --channel ... --trust` — depolama sınıfı ve retention için charm config’e bakın.
- İlişkiler: `grafana-dashboard`, `grafana-source` → Grafana; `metrics-endpoint` → Prometheus; `alertmanager` → Alertmanager; `ingress` uçları Traefik **ingress-per-unit** üzerinden.
- `loki:replicas` peer ile çoğaltma (HA) senaryosu charm sürümüne göre değişir; dokümantasyon/changelog doğrulanmalıdır.

## References
- `skills/juju-model-cos`
- `skills/cos-relation-loki-grafana`, `skills/cos-deploy-grafana`, `skills/cos-deploy-traefik`
- [Integration Matrix](https://documentation.ubuntu.com/observability/reference/integration-matrix/)
