---
name: k8s-scale-custom-metrics-api
description: "HPA'yı CPU/memory dışında Prometheus metriğine (RPS, kuyruk derinliği, hata oranı) göre ölçeklendirmek için custom.metrics.k8s.io API'sini ve Prometheus Adapter'ı kurmak ya da sorunlarını gidermek gerektiğinde kullan."
---

## Purpose
Standart Metrics Server yalnızca cpu/memory sunar. Uygulama tanımlı sinyaller (örn. `http_requests_total` oranı) için `custom.metrics.k8s.io` API'sini Prometheus Adapter aracılığıyla açmak ve HPA'ya bu metriği göstermek gerekir.

## Workflow

### 1. Prometheus Adapter kurulumu
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus-adapter prometheus-community/prometheus-adapter \
  --set prometheus.url=http://prometheus.monitoring.svc \
  --set prometheus.port=9090
```

### 2. Kural tanımlama (values.yaml)
```yaml
rules:
  custom:
    - seriesQuery: 'http_requests_total{namespace!="",pod!=""}'
      resources:
        overrides:
          namespace: {resource: "namespace"}
          pod: {resource: "pod"}
      name:
        matches: "^(.*)_total$"
        as: "${1}_per_second"
      metricsQuery: 'rate(<<.Series>>{<<.LabelMatchers>>}[2m])'
```
Kural değiştikten sonra adapter pod'u yeniden başlat.

### 3. HPA tanımı
```yaml
metrics:
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: 100
```

### Doğrulama
```bash
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq '.resources[].name'
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1/namespaces/default/pods/*/http_requests_per_second"
```

## Common mistakes
- PromQL ifadesinde pod/namespace label eşleşmesini atlayıp "no metrics" hatası almak.
- `averageValue` yerine `averageUtilization` kullanmaya çalışmak (Pods tipi metrikte geçersiz).
- Prometheus scrape aralığı ile `rate()` penceresini uyumsuz seçmek.

## References
- `skills/k8s-scale-hpa`
- `skills/k8s-scale-load-testing`
- `skills/obs-prometheus-recording-rules`
