---
name: obs-prometheus-storage-tsdb
description: Prometheus TSDB disk kullanımı büyüyor, retention belirlemek gerekiyor veya “kaç gün saklayabilirim?” sorusu yanıtlanacaksa kullan. “retention.time/size”, “WAL”, “compaction”, “blocks”, “disk doluyor” gibi TSDB-odaklı konularda dar kapsamlı karar ve hesap üretir.
---

## Purpose
Bu skill’in çıktısı:
- Retention kararı: `--storage.tsdb.retention.time` ve/veya `retention.size` için öneri
- Büyüme tahmini: hangi metrikler üzerinden yaklaşık GB/gün hesabı yapıldığı
- Operasyonel risk notu: disk dolması, restart sonrası WAL replay, compaction etkisi

## Workflow
- Önce soruyu sınıflandır:
  - “Disk doluyor” (acil) mi, yoksa “retention planla” (tasarım) mı?
  - Tek Prometheus mu, HA/replica var mı? (kopya sayısı disk çarpanı)
- Ölçümle başla (tahmin yerine metrik kullan):
  - Şu metriklerle mevcut kullanım ve eğilimi çıkar:
    - `prometheus_tsdb_storage_blocks_bytes`
    - `prometheus_tsdb_wal_size_bytes`
    - `rate(prometheus_tsdb_compactions_total[...])` (aktivite sinyali)
  - Günlük büyüme (yaklaşık): `delta(prometheus_tsdb_storage_blocks_bytes[24h])`
- Retention kararını üret:
  - Önce “iş ihtiyacı” (kaç gün sorgulanacak?) → sonra disk kapasitesi.
  - `retention.time` (gün) ve gerekiyorsa `retention.size` (hard cap) birlikte düşün.
  - Uyarı: size cap, bazı eski blokların beklenenden hızlı silinmesine sebep olabilir; raporla.
- Kök neden ipucu (disk büyümesi anormalse):
  - Yeni label patlaması mı? (kardinalite) → ayrı skill: labels-strategy.
  - Scrape hedef sayısı/interval değişti mi? → scrape-config.
- Operasyonel kontroller:
  - Disk dolmadan önce alarm: free space / TSDB bytes threshold.
  - Restart sonrası WAL replay süresi: büyük WAL → uzun açılış; WAL büyümesini takip et.

## Common mistakes
- Retention’ı “beklenen gün”e göre değil, “disk dolana kadar” bırakmak.
- Kardinalite artışını retention ile saklamaya çalışmak (kök nedeni çözmez).

## References
- `skills/cos-deploy-prometheus`
- `skills/obs-prometheus-labels-strategy`
- `skills/obs-prometheus-scrape-config`
