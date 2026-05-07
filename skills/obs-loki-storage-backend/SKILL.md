---
name: obs-loki-storage-backend
description: Loki için storage backend seçmek (filesystem vs object storage) ve bunun operasyonel sonuçlarını (retention, compactor, dayanıklılık) tasarlamak gerektiğinde kullan. “Hangi storage?”, “prod vs lab”, “index/chunk nerede”, “disk doluyor” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı:
- Seçim kararı: **deneme** (filesystem) mi, **prod** (object storage) mı?
- Operasyonel trade-off notu: durability, maliyet, compactor/retention bağımlılığı
- Storage katmanlarının nerede tutulacağına dair netlik (chunk vs index)

## Workflow
- Önce hedefi belirle:
  - Retention kaç gün? Sorgu yükü ne kadar? HA gerekir mi?
- Basit karar:
  - **Filesystem**: hızlı kurulur; tek node/lab için uygun; node kaybında veri riski yüksek.
  - **Object storage (S3/GCS/MinIO)**: prod için daha doğru; compactor/retention ile birlikte düşün.
- “Index maliyeti” ve label stratejisi:
  - Label set’i kötü ise backend ne olursa olsun ölçeklenmez (önce label stratejisini düzelt).
- Operasyonel riskleri yaz:
  - Disk tabanlı: disk dolması ve inode baskısı.
  - Object storage: latency + erişim hatası; retry ve cache ihtiyacı.
- Retention/compactor ilişkisi:
  - Retention istiyorsan compactor planı gerekir (aksi halde eski veri kalır veya silinemez).
- Doğrulama:
  - Küçük bir canary log gönder, query ile geri çek; “write→read” zinciri çalışıyor mu?

## Common mistakes
- Prod’da filesystem ile başlamak: ilk node sorunu “tüm geçmiş gitti”ye dönüşür.
- Label cardinality’i düzeltmeden storage’ı büyütmek: sadece daha pahalı hale getirir.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-label-strategy`
- `skills/obs-loki-compactor`
