---
name: k8s-storage-projected-volume
description: ConfigMap, Secret, DownwardAPI veya ServiceAccount token kaynaklarını tek mount altında birleştirmek gerektiğinde kullan. Amaç: **çoklu metadata/config kaynağını düzenli ve okunabilir biçimde sunmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Projected volume tasarımı ve kaynak birleşimi
- Token/config dosya yerleşimi
- Doğrulama: pod içindeki dosya yapısı ve rotation davranışı

## Workflow
- Kaynakları listele:
  - Hangi ConfigMap/Secret/token aynı mount altında olmalı?
- Dosya düzeni:
  - Çakışan isimler veya path mapping ihtiyacı var mı?
- Güvenlik:
  - Secret ve SA token’ı aynı yere koyarken erişim sınırını düşün.
- Rotation:
  - Token/secret güncellemesi uygulama tarafından yeniden okunuyor mu?
- Doğrulama:
  - Pod içinde beklenen dosyalar ve izinler mevcut mu?

## Common mistakes
- Birleştirmeyi kolaylık sanıp gereksiz karmaşık mount ağacı kurmak.
- Secret rotation’ı uygulamanın görmediğini fark etmemek.

## References
- `skills/k8s-core-configmap-secret`
- `skills/k8s-core-service-account`
