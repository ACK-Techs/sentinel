---
name: obs-prometheus-capacity-planning
description: Prometheus’un CPU/RAM/disk ihtiyacını hedef sayısı, seri sayısı ve scrape aralığına göre planlamak gerektiğinde kullan. “kaç target kaldırır?”, “15s → 30s yapsam ne kazanırım?”, “head memory büyüyor”, “remote_write eklersem ne olur?” gibi kapasite sorularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Kapasite tahmini için ölçüm listesi (seri/örnek/saniye, head chunks, WAL, query yükü)
- Basit “knob → etki” özeti: `scrape_interval`, target sayısı, label kardinalitesi, recording rule
- Kısa aksiyon planı: önce ölç, sonra en yüksek kaldıraçlı ayarı değiştir

## Workflow
- Önce hangi limitin sorun olduğunu belirle:
  - CPU mu? (scrape + ingestion + compaction)
  - RAM mı? (head series/chunks, query cache)
  - Disk mi? (TSDB blocks + WAL + retention)
- Ölç (tahminin tabanı):
  - Seri sayısı: `prometheus_tsdb_head_series`
  - Ingestion hızı: `rate(prometheus_tsdb_head_samples_appended_total[5m])`
  - Head chunk: `prometheus_tsdb_head_chunks`
  - Query yükü: `prometheus_engine_query_duration_seconds` (p95/p99) ve concurrent sorgular
- Kaldıraçları sırala (en çok etkileyenden başla):
  - **Kardinalite** (label patlaması) → seri sayısını çarpar; çoğu zaman en büyük etki.
  - **Scrape interval**: daha seyrek scrape → samples/s düşer; ama çözünürlük düşer.
  - **Target sayısı**: keşfi daralt (opt-in), gereksiz exporter’ları çıkar.
  - **Recording rules**: query maliyetini düşürür; ingestion’ı arttırabilir (trade-off’u yaz).
  - **remote_write**: egress + queue + retry maliyeti ekler; fail mode planı gerekir.
- Çıktı üret:
  - Mevcut metriklere göre “şimdi” durumunu 3 satırda özetle.
  - Değişiklik önerisini “beklenen etki” ile yaz (örn. samples/s % kaç düşer).
  - Risk: çok agresif interval/retention kesintisi gözlem kalitesini düşürür.

## References
- `skills/obs-prometheus-storage-tsdb`
- `skills/obs-prometheus-labels-strategy`
- `skills/obs-prometheus-remote-write`
