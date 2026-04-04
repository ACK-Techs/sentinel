---
name: cos-deploy-traefik
description: traefik-k8s ingress charm’ı; COS HTTP girişi, metrics scrape ve peers için kuralları tanımlar.
---

## Purpose
COS Lite’ın **tek HTTP giriş noktası** olarak `traefik-k8s` üzerinden Grafana, Catalogue, Alertmanager, Prometheus ve Loki birimlerine yönlendirilmiş erişim sağlamak.

## Rules
- Charm adı: **`traefik-k8s`** ([Charmhub](https://charmhub.io/traefik-k8s)).
- MicroK8s önkoşulu: **MetalLB** etkin; Traefik Service tipi LoadBalancer için IP ataması yapılabilmeli.
- Bundle: `juju deploy cos-lite --trust` — Traefik `ingress`, `ingress-per-unit`, `traefik-route`, `metrics-endpoint`, `peers` ilişkileriyle gelir.
- Aksiyon: **`show-proxied-endpoints`** — proxied URL’leri YAML olarak döner; `yq`/`jq` ile parse (tutorial örneği).
- Kanal: tutorial örneği `latest/edge` rev kullanır; üretimde **sabit kanal/rev** seçin.

## References
- `skills/microk8s-addons-dns-storage`
- `skills/cos-ingress-config`
- [traefik-k8s actions — show-proxied-endpoints](https://charmhub.io/traefik-k8s/actions#show-proxied-endpoints)
