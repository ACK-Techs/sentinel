---
name: cos-deploy-otel-collector
description: "Juju ile OTEL Collector charm'ını COS modeline dağıtmak, Prometheus/Loki/Tempo relation'larını kurmak ve telemetri yönlendirme yapılandırmasını uygulamak gerektiğinde kullan."
---

## Purpose
OTEL Collector Juju charm'ı, uygulama tarafından gönderilen OTLP telemetri verisini alıp COS bileşenlerine yönlendirir. Tüm sinyal türleri (metric, log, trace) için merkezi giriş noktasıdır.

## Deploy
```bash
juju switch cos
juju deploy opentelemetry-collector-k8s --channel=latest/stable
```

## Temel relation'lar
```bash
# Prometheus → metrik çekme:
juju integrate opentelemetry-collector-k8s:metrics-endpoint prometheus-k8s:metrics-endpoint

# Loki → log gönderme:
juju integrate opentelemetry-collector-k8s:log-forwarding loki-k8s:log-proxy

# Tempo → trace gönderme:
juju integrate opentelemetry-collector-k8s:tempo-endpoint tempo-k8s:tempo-source

# Ingress (opsiyonel):
juju integrate opentelemetry-collector-k8s:ingress traefik-k8s:ingress-per-unit
```

## Uygulama modelinden veri gönderme
```bash
# cos modelinde offer oluştur:
juju switch cos
juju offer opentelemetry-collector-k8s:receiver otlp-receiver

# uygulama modelinde:
juju switch myapp
juju integrate myapp:otlp-endpoint admin/cos.otlp-receiver
```

## Yapılandırma
```bash
# OTLP gRPC port varsayılan: 4317, HTTP: 4318
juju config opentelemetry-collector-k8s
```

## Doğrulama
```bash
juju status opentelemetry-collector-k8s
# Test trace gönder:
curl -X POST http://<collector-url>/v1/traces \
  -H "Content-Type: application/json" \
  -d '{"resourceSpans":[]}'
```

## Common mistakes
- Tempo deploy etmeden trace relation oluşturmaya çalışmak.
- Uygulama OTLP endpoint'ini doğrudan Tempo'ya yönlendirmek yerine Collector'dan geçirmemek — sampling/batching kaybedilir.

## References
- `skills/cos-bundle-overview`
- `skills/cos-deploy-tempo`
- `skills/cos-relation-otel-prometheus`
- `skills/obs-otel-collector-pipeline`
