---
name: cos-deploy-prometheus
description: prometheus-k8s charm’ını veya cos-lite bundle içindeki Prometheus bileşenini hedefleyen kanal ve güven (trust) kurallarını tanımlar.
---

## Purpose
**Metrik toplama** için `prometheus-k8s` charm’ının doğru kanalda ve gerekli entegrasyonlarla (Alertmanager, Grafana, Traefik) çalışmasını sağlamak.

## Rules
- Charm adı: **`prometheus-k8s`** (Charmhub: [prometheus-k8s](https://charmhub.io/prometheus-k8s)).
- **Tercih edilen yol**: tam yığın için `juju deploy cos-lite --trust` — Prometheus bundle içinde gelir; `--trust` Kubernetes Service/limits düzeltmeleri için gereklidir.
- Ayrı deploy: `juju deploy prometheus-k8s --channel <stable|latest/edge>` — tutorial örnekleri `latest/edge` rev gösterebilir; üretimde **stable/track** sabitleyin (ör. Terraform modülü `2/stable` bundle kanalı referansı).
- İlişkiler (bundle dışı manuel): `metrics-endpoint` sağlayıcı/tüketici, `alertmanager`, `grafana-dashboard`, `grafana-source`, `ingress` (Traefik), `catalogue` — tam tablo için `juju status --relations`.
- Ölçek: `prometheus-peers` peer ilişkisi HA senaryolarında kullanılır.

## References
- `skills/juju-model-cos`
- `skills/cos-relation-prometheus-grafana`, `skills/cos-deploy-alertmanager`, `skills/cos-deploy-traefik`
- [COS Lite on MicroK8s — bundle deploy](https://documentation.ubuntu.com/observability/track-2/tutorial/installation/cos-lite-microk8s-sandbox/#deploy-the-cos-lite-bundle)
