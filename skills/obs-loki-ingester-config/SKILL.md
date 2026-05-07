---
name: obs-loki-ingester-config
description: Loki ingester davranışını (chunk flush, WAL, chunk encoding) ayarlamak veya ingest sırasında bellek/disk baskısı ve veri kaybı risklerini yönetmek gerektiğinde kullan. “flush interval”, “WAL aç/kapat”, “chunk encoding seçimi” gibi ingester‑odaklı tuning sorularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Ingester için tuning kararları: flush/idle süreleri, WAL kullanımı, encoding seçimi
- “Hangi knob neyi etkiler?” kısa notu (RAM, disk, query latency, veri kaybı)
- Yanlış ayar semptomları ve düzeltme yönü (OOM, yüksek disk I/O, out-of-order)

## Workflow
- Önce sorunu sınıflandır:
  - Ingest sırasında RAM artıyor mu? (chunk’lar uzun süre memory’de kalıyor olabilir)
  - Disk I/O yüksek mi? (WAL/flush/compaction etkileşimi)
  - Veri kaybı/endişe var mı? (WAL kapalı/yanlış)
- Flush davranışı:
  - “Idle/age” bazlı flush: az trafik stream’lerinde chunk’ların asılı kalmasını önler.
  - Çok agresif flush → daha fazla küçük chunk → storage ve query maliyeti artar.
- WAL kararı:
  - WAL, crash/restart sonrası veri kaybı riskini azaltır; disk ve startup (replay) maliyeti getirir.
  - “Sık restart” veya node preemption varsa WAL genelde gereklidir.
- Chunk encoding seçimi:
  - Encoding seçimi, depolama maliyeti ve query CPU’sunu etkiler; değişikliği küçük bir pencereyle doğrula.
  - Encoding’i seçerken log yapısı (kısa/uzun satır, tekrar oranı) ve retention hedefini not et.
- Doğrulama:
  - Canary log gönder → query ile geri çek (write→read).
  - Ingester metrikleriyle bellek/flush/WAL davranışı beklenen yönde mi kontrol et.

## Common mistakes
- Flush’ı “çok seyrek” bırakıp bellek şişmesi yaratmak (az trafik stream’lerinde bile).
- WAL’i açıp disk kapasitesini planlamamak (replay + disk dolması).

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-storage-backend`
