---
name: obs-tempo-hot-cold-storage
description: Tempo’da “yakın dönem hızlı, eski dönem ucuz” hedefiyle hot/cold storage katmanlaması tasarlamak veya local→object storage gibi bir storage migration planlamak gerektiğinde kullan. Query latency ve operasyonel riskleri birlikte ele alır.
---

## Purpose
Bu skill’in çıktısı:
- Hot vs cold dönem tanımı (örn. son 24–72 saat hot, sonrası cold)
- Katmanlama/migration planı (kesinti riski, geri dönüş, doğrulama)
- Beklenen etkiler: maliyet düşer, eski trace sorguları yavaşlayabilir

## Workflow
- İhtiyacı netleştir:
  - “Sık sorgulanan aralık” kaç saat/gün? (hot pencere)
  - Retention toplam kaç gün? (cold kapsam)
- Katmanlama kararını yaz:
  - Hot: hızlı disk / düşük latency erişim
  - Cold: object storage (ucuz) + kabul edilebilir arama gecikmesi
- Migration planı:
  - Yeni storage’a yazmaya geçiş sırası (dual-write mümkün mü?)
  - Eski verinin taşınması vs “eski kaldığı yerde kalsın” kararı
  - Credential/izin ve lifecycle politikaları
- Riskler:
  - Cold sorgularında timeout: kullanıcı beklentisini yönet (UI uyarısı/limit)
  - Yanlış permission: ingest var gibi görünür ama data kalıcı olmaz
- Doğrulama:
  - Yeni yazılan trace’ler hot’ta hızlı bulunuyor mu?
  - Eski trace’ler cold’da bulunabiliyor mu? (beklenen latency ile)

## Common mistakes
- Hot pencereyi gerçek kullanım verisi olmadan seçmek (gereksiz maliyet).
- Cold sorgularını sınırlamamak: herkes “tüm ay” arayıp sistemi boğar.

## References
- `skills/obs-tempo-storage-backend`
- `skills/obs-tempo-resource-sizing`
