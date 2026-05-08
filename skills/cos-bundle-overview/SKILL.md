---
name: cos-bundle-overview
description: "Canonical Observability Stack (COS) Lite bundle'ının bileşenlerini, aralarındaki relation ağını ve hangi sırayla ne yapılması gerektiğini anlayarak COS deploy sürecini yönetmek gerektiğinde kullan."
---

## Purpose
COS Lite, Juju bundle olarak dağıtılan tam bir observability stack'tir: Prometheus, Loki, Grafana, Alertmanager ve Traefik (ingress). Her bileşen bağımsız Kubernetes charm'ı olarak çalışır.

## COS Lite bileşenleri

| Charm | Rol |
|---|---|
| `prometheus-k8s` | Metrik toplama ve depolama |
| `loki-k8s` | Log toplama ve sorgu |
| `grafana-k8s` | Dashboard ve görselleştirme |
| `alertmanager-k8s` | Alert yönlendirme ve bildirim |
| `traefik-k8s` | Ingress ve URL yönetimi |
| `catalogue-k8s` | Servis dizini ve URL paylaşımı |

## Standart relation ağı
```
prometheus → grafana     (grafana-source)
loki → grafana           (grafana-source)
alertmanager → grafana   (grafana-source)
prometheus → alertmanager (alerting)
traefik → grafana        (ingress)
traefik → prometheus     (ingress)
traefik → alertmanager   (ingress)
catalogue → grafana      (catalogue)
```

## Deploy
```bash
juju switch cos-model
juju deploy cos-lite
# veya kaynak koda doğrudan:
juju deploy ./cos-lite.yaml
```

## Durum doğrulama
```bash
juju status --watch 5s
# Tüm birimler active/idle olduğunda URL'leri al:
juju run traefik-k8s/0 show-proxied-endpoints --format=json
```

## Common mistakes
- Traefik ingress IP'si hazır olmadan dashboard URL'lerini almaya çalışmak.
- `catalogue-k8s` deploy etmeyi atlamak — servis keşif URL'leri eksik kalır.
- DNS veya /etc/hosts olmadan Traefik hostname'lerine bağlanmaya çalışmak.

## References
- `skills/juju-bundle-deploy`
- `skills/cos-deploy-tempo`
- `skills/cos-multi-model`
- `documantations/ARCHITECTURE_COS.md`
