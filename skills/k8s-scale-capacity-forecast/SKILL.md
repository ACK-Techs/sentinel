---
name: k8s-scale-capacity-forecast
description: "Gelecek 30-90 gün içinde cluster kapasite yetersizliği yaşanıp yaşanmayacağını, mevcut Prometheus metriklerinden lineer/mevsimsel projeksiyon yaparak tahmin etmek gerektiğinde kullan."
---

## Purpose
Reaktif ölçekleme yerine proaktif planlama: hangi namespace'in, hangi zaman diliminde, hangi kaynak (CPU/memory/storage/pod sayısı) için sınırı zorlayacağını önceden bilerek node ekleme veya kota artırma kararı almak.

## Workflow

### Temel metrikler ve PromQL sorguları

**CPU kullanım trendi (son 30 gün)**
```promql
predict_linear(
  sum(rate(container_cpu_usage_seconds_total{namespace!="kube-system"}[5m]))[30d:1h],
  86400 * 30
)
```

**Memory baskısı riski**
```promql
predict_linear(
  sum(container_memory_working_set_bytes{namespace!="kube-system"})[14d:1h],
  86400 * 14
)
```

**Pod sayısı büyüme tahmini**
```promql
predict_linear(count(kube_pod_info)[7d:1h], 86400 * 30)
```

### Kapasite eşik hesabı
- Node allocatable CPU/memory: `kube_node_status_allocatable{resource="cpu"}`
- Toplam request vs allocatable oranı %70'i geçince yeni node planla.
- Storage için PVC kullanım büyümesi: `kubelet_volume_stats_used_bytes`.

### Grafana dashboard önerisi
Forecast panellerinde `predict_linear` sonuçlarını mevcut kapasite çizgisiyle birleştir; kesişim tarihi = planlama son tarihi.

## Common mistakes
- `predict_linear` ile mevsimsel (hafta sonu/tatil) trendi düz çizgi tahmin etmek.
- Sadece CPU'ya bakmak; memory OOM veya PVC dolması çok daha sık kapasiteyi tüketir.
- Namespace kotalarını hesaba katmamak; cluster genelinde yer olsa da namespace kotası engel çıkarabilir.

## References
- `skills/k8s-scale-cluster-autoscaler`
- `skills/obs-prometheus-query-range`
- `skills/k8s-core-resource-requests-limits`
- `skills/k8s-core-namespace`
