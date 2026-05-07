---
name: obs-tempo-resource-sizing
description: Tempo bileşenlerini (distributor/ingester/query) CPU/RAM ve storage açısından boyutlandırmak veya “trace volumü artıyor, ne kadar kaynak gerekir?” sorusunu yanıtlamak gerektiğinde kullan. Ölçüm‑tabanlı sizing ve büyüme tahmini odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Sizing için ölçüm listesi (ingest rate, spans/s, block yazımı, query concurrency)
- Hangi bileşen hangi yükten etkilenir (ingest vs query vs compaction)
- Kapasite planı: “önce ölç → sonra knob değiştir/ölçekle” kısa aksiyon listesi

## Workflow
- Önce workload’ı tanımla:
  - Ingest: spans/s, trace boyutu, sampling oranı
  - Query: kaç kullanıcı, hangi zaman aralıkları, TraceQL karmaşıklığı
  - Retention: kaç gün/saat
- Ölç (tahminin tabanı):
  - Ingest throughput ve reject/dropped sinyalleri
  - Query latency p95/p99 ve concurrent query
  - Storage büyüme trendi (object store bytes/day)
- Bileşen bazlı kaldıraçlar:
  - Distributor: protokol/ingress, burst kontrolü
  - Ingester: bellek baskısı, WAL/replay, block flush davranışı
  - Querier/query-frontend: shard/caching, tail latency
  - Compactor: retention iş yükü ve storage I/O
- Çıktı üret:
  - “Şimdi” durum özeti (3 satır) + risk (OOM, throttle, storage) + öneri (scale up/out).

## Common mistakes
- Query darboğazını ingest ölçekleyerek çözmeye çalışmak (katmanı ayır).
- Sampling/attribute patlaması varken sadece kaynak büyütmek (maliyeti katlar).

## References
- `skills/obs-tempo-sampling-strategy`
- `skills/obs-tempo-storage-backend`
