---
name: cos-ingress-config
description: Traefik üzerinden COS web uçlarına erişim; show-proxied-endpoints, path kuralları ve MetalLB önkoşullarını tanımlar.
---

## Purpose
**MetalLB + Traefik** ile COS bileşenlerine HTTP üzerinden güvenli ve tutarlı erişim; pod IP ile doğrudan erişimde port/path birleşiminin bilinmesi.

## Rules
- Önkoşul: MicroK8s **metallb** etkin; Traefik LoadBalancer IP’si `show-proxied-endpoints` çıktısındaki host IP ile uyumlu olmalıdır.
- Aksiyon: `juju run traefik/0 show-proxied-endpoints --format=yaml` — Prometheus, Loki, Catalogue, Alertmanager URL’leri; Grafana için çoğu zaman **Catalogue** veya `show-unit catalogue/0` içindeki `url` listesi (tutorial).
- Path kuralları: app ingress → `http://<LB>/cos-<app>`; per-unit → `.../cos-<app>-<unit>` örnek yapısı tutorial’da verilmiştir.
- Pod IP ile test: örn. Alertmanager `/-/ready` yolu ingress path ile birlikte: `curl <pod-ip>:9093/cos-alertmanager/-/ready` (tutorial örneği).
- Sorun: [Gateway Address Unavailable (Traefik)](https://documentation.ubuntu.com/observability/how-to/troubleshooting/troubleshoot-gateway-address-unavailable/).

## References
- `skills/cos-deploy-traefik`, `skills/microk8s-addons-dns-storage`
- [Browse dashboards — COS Lite MicroK8s](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/#browse-dashboards)
