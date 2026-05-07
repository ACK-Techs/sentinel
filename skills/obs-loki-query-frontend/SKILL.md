---
name: obs-loki-query-frontend
description: Loki sorguları yavaş/timeout oluyor, çok kullanıcı aynı anda Explore açıyor veya “querier overload” yaşıyorsan query-frontend ile shard/caching/fairness tasarlamak için kullan. Query-frontend’in neyi hızlandırdığı ve hangi ayarların riskli olduğu üzerine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Query-frontend’in rolü: request splitting/sharding, sonuç cache, query queue
- Hedeflenen semptoma göre ayar önerisi (timeout, tail latency, concurrency)
- Doğrulama planı: latency p95/p99, cache hit rate, querier yükü

## Workflow
- Semptomu seç:
  - Timeout mı? (uzun zaman aralığı + geniş selector)
  - Tail latency mi? (p99 sıçrıyor)
  - Concurrency mi? (çok kullanıcı aynı anda query)
- Query-frontend’in ne yaptığına göre karar ver:
  - Zaman aralığını parçalayıp querier’a dağıtma (shard/split) → büyük aralık sorgularında fayda.
  - Sonuç cache → tekrarlı dashboard/Explore sorgularında fayda.
  - Queue/fairness → “bir kullanıcı herkesi boğmasın” senaryosu.
- Cache stratejisi:
  - Cache’in fayda sağlaması için sorguların tekrar etmesi gerekir; yoksa sadece maliyet.
  - TTL’i dashboard refresh ile uyumlu seç.
- Sharding riskleri:
  - Çok agresif shard → aşırı fan-out, querier üzerinde daha fazla iş.
  - Çok az shard → timeout devam eder.
- Doğrulama:
  - Aynı sorguyu önce/sonra karşılaştır: wall time düşüyor mu?
  - Cache hit ve querier CPU/memory trendi beklenen yönde mi?

## Common mistakes
- Query-frontend’i “her derde deva” sanmak: label stratejisi kötü ise frontend sadece daha çok iş üretir.
- Cache’i ölçmeden büyütmek: memory pressure ve eviction churn yaratır.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-chunk-cache`
- `skills/obs-loki-label-strategy`
