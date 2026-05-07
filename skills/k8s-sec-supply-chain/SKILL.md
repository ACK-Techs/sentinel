---
name: k8s-sec-supply-chain
description: "Container image imzalama, doğrulama, SBOM ve provenance akışını kurmak veya “deploy ettiğimiz image gerçekten build ettiğimiz image mi?” sorusunu yönetmek gerektiğinde kullan. Amaç: **tedarik zinciri güvenini doğrulanabilir hale getirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Sign/verify ve SBOM akışı
- Cluster admission veya CI doğrulama noktası
- Doğrulama: imzasız/uygunsuz image engelleniyor mu?

## Workflow
- Güven modelini belirle:
  - Kim imzalıyor? build sistemi mi, insan mı?
- Artifact zinciri:
  - Image digest, SBOM, provenance birlikte mi tutulacak?
- Doğrulama noktası:
  - CI’da mı, registry policy’de mi, cluster admission’da mı?
- Exception:
  - Üçüncü parti image’ler nasıl yönetilecek?
- Doğrulama:
  - İmzasız veya yanlış imzalı image ile kapıyı test et.

## Common mistakes
- Tag’e güvenip digest ve imzayı ikinci plana atmak.
- SBOM üretip hiç kullanmamak.

## References
- `skills/k8s-sec-image-scanning`
- `cli/skills/agentic-dependency-licensing`
