---
name: k8s-sec-image-scanning
description: "Container image güvenlik taraması kurmak, CI kapısı eklemek veya “bu image prod’a girmeden önce hangi CVE eşiğinden geçmeli?” kararını vermek gerektiğinde kullan. Amaç: **scan sonucunu uygulanabilir policy’ye çevirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Image scanning akışı ve eşik kararı
- Build pipeline’da scan konumu
- Doğrulama: riskli image’in gerçekten engellendiği kanıt

## Workflow
- Tarama noktasını seç:
  - Build sonrası mı, registry’de mi, deploy öncesi mi?
- Eşik:
  - Critical/high CVE, fix available filtresi, ignore listesi.
- SBOM ilişkisi:
  - Paket kökeni ve bağımlılık görünürlüğü gerekir mi?
- Operasyon:
  - False positive ve exception süreci tanımla.
- Doğrulama:
  - Bilinçli zafiyetli image ile pipeline davranışını test et.

## Common mistakes
- Tarama açıp sonuçları policy’ye bağlamamak.
- Fix olmayan CVE’lerle pipeline’ı kullanılamaz hale getirmek.

## References
- `cli/skills/agentic-dependency-licensing`
- `skills/k8s-sec-supply-chain`
