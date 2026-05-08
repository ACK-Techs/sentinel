---
name: cos-deploy-tempo
description: "Juju ile Tempo charm'ını COS modeline dağıtmak, OTEL Collector relation'ını kurmak, Grafana datasource ilişkisini eklemek ve ingress üzerinden trace UI erişimini sağlamak gerektiğinde kullan."
---

## Purpose
Tempo, COS Lite'ın dağıtık iz (distributed tracing) bileşenidir. Temel bundle'a dahil değildir; ayrıca deploy edilmesi gerekir.

## Deploy
```bash
juju switch cos
juju deploy tempo-k8s --channel=latest/stable
juju deploy tempo-worker-k8s --channel=latest/stable  # opsiyonel HA
```

## Temel relation'lar
```bash
# Grafana datasource:
juju integrate tempo-k8s:grafana-source grafana-k8s:grafana-source

# Traefik ingress:
juju integrate tempo-k8s:ingress traefik-k8s:ingress-per-unit

# OTEL Collector → Tempo:
juju integrate otel-collector-k8s:tempo-endpoint tempo-k8s:tempo-source

# Prometheus metrics:
juju integrate tempo-k8s:metrics-endpoint prometheus-k8s:metrics-endpoint
```

## Storage
```bash
juju deploy tempo-k8s --storage data=10G
```

## Doğrulama
```bash
juju status tempo-k8s
# Ingress URL:
juju run traefik-k8s/0 show-proxied-endpoints | grep tempo
# Test trace gönder:
curl -X POST http://<tempo-url>/api/traces
```

## Uygulama modelinden tüketim
```bash
# cos modelinden offer:
juju switch cos
juju offer tempo-k8s:tempo-endpoint tempo-endpoint

# uygulama modelinde:
juju switch myapp
juju integrate myapp:tracing admin/cos.tempo-endpoint
```

## Common mistakes
- OTEL Collector deploy etmeden Tempo'ya trace göndermeye çalışmak.
- Grafana relation eklemeden Tempo datasource'unun otomatik görünmesini beklemek.
- S3 backend yapılandırmadan 10GB'dan büyük trace verisi depolamaya çalışmak.

## References
- `skills/cos-bundle-overview`
- `skills/cos-deploy-otel-collector`
- `skills/cos-relation-tempo-grafana`
- `skills/obs-tempo-pipeline-e2e`
