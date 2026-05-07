---
name: obs-prometheus-histogram-summary
description: Latency gibi dağılım ölçümlerinde Histogram mı Summary mi seçileceğine karar vermek, histogram bucket’larını tasarlamak veya PromQL’de `histogram_quantile()` kullanımını doğru yapmak gerektiğinde kullan. “p95/p99 nasıl hesaplanır?”, “bucket yanlış mı?”, “summary neden aggregate olmuyor?” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı:
- Histogram vs Summary seçimi için kısa karar (distributed aggregation ihtiyacı, cardinality, client-side quantile)
- Histogram kullanılıyorsa **bucket seti** önerisi (ölçek + hedef SLO bandı)
- PromQL şablonu: `histogram_quantile(q, sum by (...) (rate(<metric>_bucket[...])) )`

## Workflow
- İhtiyacı sor:
  - Quantile’ı **global** (çok instance/service üzerinde) aggregate etmek istiyor musun?
  - Hedef: p50/p95/p99 mı, yoksa sadece ortalama/ratio mu?
- Seçim kuralı:
  - **Histogram**: Prometheus tarafında aggregate edilebilir (cluster/service düzeyi p95/p99 için genelde doğru tercih).
  - **Summary**: quantile client-side hesaplanır; instance dışına aggregate etmek genelde anlamlı değildir.
- Histogram ölçümü doğru mu kontrol et:
  - `_bucket`, `_sum`, `_count` üçlüsü var mı?
  - Bucket’lar monotonic mi? (le etiketleri)
- Bucket tasarımı:
  - SLO bandını kapsa: ör. 50ms–5s arası ise bu aralığa daha yoğun bucket koy.
  - Çok fazla bucket → daha fazla seri ve maliyet; çok az bucket → quantile hassasiyeti düşer.
- PromQL kalıbı (hata yapma noktalarıyla):
  - `rate(..._bucket[window])` kullan; raw bucket sayımı değil.
  - `sum by (le, <dim...>)` ile aggregate et; `le`’yi düşürürsen quantile bozulur.
  - `window` seçimi: çok kısa pencere “zıplar”, çok uzun pencere “gecikir”.
- Doğrulama:
  - p95/p99 grafiği ile `_count` (trafik) grafiğini birlikte gör: low-traffic’te quantile gürültülüdür.

## Anti-patterns
- Summary quantile’ını service geneline “toplamak”: matematiksel olarak yanıltıcı.
- `histogram_quantile()` içinde `sum without(le)` gibi `le`’yi düşürmek.

## References
- `skills/obs-grafana-heatmap-panel`
- `skills/obs-prometheus-recording-rules`
