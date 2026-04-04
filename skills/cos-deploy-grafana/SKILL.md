---
name: cos-deploy-grafana
description: grafana-k8s charm’ı için dağıtım, admin parolası ve Traefik traefik-route entegrasyon kurallarını içerir.
---

## Purpose
**Dashboard ve veri kaynağı** tüketimi için `grafana-k8s` uygulamasını COS ile uyumlu şekilde çalıştırmak.

## Rules
- Charm adı: **`grafana-k8s`** ([Charmhub](https://charmhub.io/grafana-k8s)).
- Bundle: `juju deploy cos-lite --trust` — Grafana, Prometheus/Loki/Alertmanager’dan `grafana-source` ve `grafana-dashboard` alır; Traefik ile **`traefik-route`** (`grafana:ingress`) üzerinden yayınlanır.
- Varsayılan kullanıcı: **`admin`** — parola: `juju run grafana/leader get-admin-password --model <model>` (tutorial ile aynı).
- Ayrı deploy: `juju deploy grafana-k8s --channel ... --trust` — peer `grafana:grafana`, `grafana:replicas` HA için.
- Catalogue, Grafana URL’lerini listeleyebilir; Traefik `show-proxied-endpoints` çıktısında Grafana her zaman görünmeyebilir — `juju show-unit catalogue/0` içindeki `url` alanlarına bakın (tutorial notu).

## References
- `skills/cos-relation-prometheus-grafana`, `skills/cos-relation-loki-grafana`
- `skills/cos-ingress-config`
- [Grafana-k8s actions — get-admin-password](https://charmhub.io/grafana-k8s/actions)
