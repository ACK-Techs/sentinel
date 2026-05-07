---
name: obs-tempo-storage-backend
description: Tempo için trace storage backend seçmek (local vs object storage) ve bunun retention, dayanıklılık, maliyet ve query latency etkilerini değerlendirmek gerektiğinde kullan. “Prod’da hangi storage?”, “local ile olur mu?”, “object storage latency” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı:
- Storage seçimi kararı (lab vs prod) ve gerekçesi
- Operasyonel risk notu: durability, kapasite planı, restore/DR
- Doğrulama planı: canary trace + Grafana/Tempo’da trace geri çekme

## Workflow
- Önce hedefi belirle:
  - Retention kaç gün/saat? (trace volumüne göre)
  - HA/DR beklentisi var mı?
- Basit karar:
  - **Local storage**: hızlı kurulum; tek node/lab için; node kaybında veri riski yüksek.
  - **Object storage (S3/GCS/MinIO)**: prod için daha uygun; latency ve izin yönetimi plan ister.
- Maliyet/latency trade-off:
  - Arama ve trace get performansı storage latency’den etkilenebilir; cache/compactor bileşenleriyle birlikte düşün.
- Güvenlik:
  - Credential’ları config’e düz metin yazma; secret referansı kullan.
- Doğrulama:
  - Uygulamadan canary trace üret.
  - Tempo’dan trace’i bul/get yap; aynı trace’i birkaç dakika sonra tekrar çek (persist ediyor mu?).

## Common mistakes
- Prod’da local storage ile başlamak: ilk node olayında trace geçmişi kaybolur.
- Object storage izinlerini eksik bırakmak: ingest var gibi görünür ama blok yazılamaz.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
