---
name: cos-relation-loki-grafana
description: loki-k8s ile grafana-k8s arasındaki log datasource ve Loki panoları için grafana-source/grafana-dashboard kurallarını tanımlar.
---

## Purpose
Loki loglarının Grafana’da **sorgulanabilir veri kaynağı** olarak bağlanması ve bundle ile gelen dashboard paketlerinin yüklenmesi.

## Rules
- Bundle içinde: `loki:grafana-source` → `grafana:grafana-source`; `loki:grafana-dashboard` → `grafana:grafana-dashboard`.
- Manuel: `juju integrate loki:grafana-source grafana:grafana-source` ve `juju integrate loki:grafana-dashboard grafana:grafana-dashboard` (`juju relate` = alias).
- Loki birim erişimi Traefik **ingress-per-unit** ile path tabanlıdır (ör. `/cos-loki-0`) — `cos-ingress-config` ile birlikte düşünün.
- Loki metrikleri Prometheus’a `loki:metrics-endpoint` → `prometheus:metrics-endpoint` ile gider.

## References
- `skills/cos-deploy-loki`, `skills/cos-deploy-grafana`
- `skills/cos-ingress-config`
