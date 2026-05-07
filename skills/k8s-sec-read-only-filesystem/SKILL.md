---
name: k8s-sec-read-only-filesystem
description: Container root filesystem’ini read-only yapmak, yazılabilir path’leri ayırmak veya “uygulama neden dosya yazamıyor?” sorusunu çözmek gerektiğinde kullan. Amaç: **runtime saldırı yüzeyini dosya sistemi seviyesinde küçültmektir**.
---

## Purpose
Bu skill’in çıktısı:
- readOnlyRootFilesystem uygulanabilirlik kararı
- Yazılabilir path/volume ihtiyacı listesi
- Doğrulama: uygulama çalışırken beklenmeyen yazma yolları kapanıyor mu?

## Workflow
- Yazma ihtiyaçlarını çıkar:
  - Temp file, cache, pid/socket, upload path var mı?
- Root FS’i kapat:
  - Gerekli yazma alanlarını `emptyDir` veya özel volume ile aç.
- Security context:
  - Non-root, dropped capabilities ile birlikte düşün.
- Test:
  - Uygulama startup ve normal trafik altında hata veriyor mu?
- Doğrulama:
  - Beklenmeyen write denemeleri engelleniyor mu?

## Common mistakes
- `/tmp` ihtiyacını unutup app’i kırmak.
- Sadece flag ekleyip volume düzenini yapmamak.

## References
- `skills/k8s-sec-pod-security-standards`
- `skills/sec-container-hardening`
