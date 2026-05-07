---
name: obs-tempo-traceql-advanced
description: TraceQL’de ileri seviye sorgu yazmak gerektiğinde kullan: span attribute filtreleri, parent/child yapısı, “trace içinde belirli span kombinasyonu var mı?” gibi structural sorgular ve sorguyu daraltma/performans iyileştirme stratejileri. Basit trace araması için değil.
---

## Purpose
Bu skill’in çıktısı:
- “Yapısal koşul” içeren TraceQL örnekleri (tek span değil, trace içi ilişki)
- Attribute alanlarının nereden geldiğini netleştiren kısa kontrol (resource vs span attributes)
- Sorgu performansı için daraltma stratejisi (service/time + minimum koşul seti)

## Workflow
- Soruyu “trace yapısı”na çevir:
  - “Bu trace’de hem X hem Y var” mı? (ör. auth span + db span)
  - “Belirli span şu attribute ile var” mı? (örn. `http.status_code >= 500`)
- Attribute kaynağını doğrula:
  - Aradığın alan span attribute mu, resource attribute mu? (yanlış yerde arama boş sonuç üretir)
  - Eğer alan yoksa: instrumentation/collector tarafında eklenmeli.
- Structural sorgu yaz:
  - Önce service + zaman penceresi ile daralt.
  - Sonra “trace içinde” koşulu ekle: iki farklı span tipi/attribute kombinasyonu.
  - Gerekirse span name + attribute birlikte kullan (daha stabil).
- Performans:
  - Çok genel attribute regex’lerinden kaçın.
  - “Önce dar selector, sonra pahalı filtre” prensibi.
- Doğrulama:
  - Bulunan bir trace’i açıp koşulu gerçekten sağlıyor mu kontrol et (yanlış pozitif olabilir).

## Common mistakes
- Attribute’ı yanlış namespace’te aramak (resource vs span).
- “Her şeyi kapsayan” structural sorgu yazıp timeout olmak.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
