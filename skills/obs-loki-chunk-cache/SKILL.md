---
name: obs-loki-chunk-cache
description: Loki query path’inde chunk cache eklemek (memcached/redis) ve bunun hangi sorgularda fayda sağlayacağını değerlendirmek gerektiğinde kullan. “query yavaş”, “cache hit rate”, “memcached/redis ile hızlanır mı?” gibi performans odaklı konular için.
---

## Purpose
Bu skill’in çıktısı:
- Cache’in **nerede** devreye girdiği ve hangi workload’da kazanç beklenmesi gerektiği
- Cache boyutu/TTL için başlangıç önerisi + gözlem metrikleri (hit/miss)
- Yanlış cache’in maliyeti (stampede, memory pressure) için guardrail

## Workflow
- Önce darboğazı doğrula:
  - Yavaşlık index mi, chunk fetch mi, query parse mı? (rastgele cache ekleme)
- Cache’in uygun olduğu senaryolar:
  - Aynı zaman aralığına tekrarlı sorgular (dashboard refresh, explore tekrarları)
  - Büyük arşiv sorguları (object storage’dan sık okuma)
- Cache backend seç:
  - Memcached: basit, hızlı; eviction davranışını izle.
  - Redis: daha esnek; ama latency ve persistence ayarları dikkat ister.
- Başlangıç ayarı:
  - TTL’i “dashboard refresh” ile uyumlu seç (çok kısa → fayda yok, çok uzun → memory).
  - Boyutu hit rate’e göre büyüt; ilk gün “küçük başla”.
- Doğrulama:
  - Cache hit/miss metriklerini izle ve sorgu latency (p95) düşüyor mu bak.
  - Cache ekledikten sonra query_frontend ve querier load dağılımı değişti mi?

## Common mistakes
- Cache’i darboğaz ölçmeden eklemek: sadece yeni bir bağımlılık yaratır.
- Cache stampede: aynı sorgu aynı anda patlayıp cache’i boğar (rate limit / query sharding düşün).

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-query-frontend`
