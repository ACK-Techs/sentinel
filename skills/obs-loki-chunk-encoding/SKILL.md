---
name: obs-loki-chunk-encoding
description: Loki’de chunk compression/encoding seçimi yapmak veya “disk maliyeti vs query CPU” dengesini ayarlamak gerektiğinde kullan. gzip/snappy/lz4/zstd gibi seçeneklerde hangi workload’a hangi tercihin daha uygun olacağını dar kapsamda değerlendirir.
---

## Purpose
Bu skill’in çıktısı:
- Encoding seçimi için karar (CPU mı disk mi öncelik?)
- Değişiklik yapmadan önce/sonra ölçüm planı (query latency, CPU, storage büyümesi)
- “Ne zaman değiştirmemeli?” uyarısı (prod’da ani format değişimi riskleri)

## Workflow
- Önce darboğazı belirle:
  - Disk/obj storage maliyeti mi yüksek?
  - Query CPU mu yüksek? (decompress maliyeti)
  - Ingest CPU mu yüksek? (compress maliyeti)
- Encoding seçimini hedefe göre yap:
  - Disk kazanımı öncelikse daha agresif sıkıştırma (CPU pahasına).
  - Hız öncelikse daha hızlı codec (daha büyük veri pahasına).
- Değişiklik stratejisi:
  - Prod’da aniden tüm cluster’da değiştirme; küçük kapsamda dene ve ölç.
  - Retention/compactor davranışıyla birlikte düşün (eski chunk’lar ne olacak?).
- Ölç ve doğrula:
  - Aynı dashboard sorgularında p95/p99 latency.
  - Ingester/querier CPU.
  - Storage büyüme hızı.

## Common mistakes
- “Daha iyi sıkıştırma”yı kör seçmek: query CPU’yu patlatabilir.
- Ölçmeden değiştirmek: kazanç mı zarar mı anlaşılmaz.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-ingester-config`
- `skills/obs-loki-storage-backend`
