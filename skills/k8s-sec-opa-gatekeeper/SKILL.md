---
name: k8s-sec-opa-gatekeeper
description: OPA Gatekeeper ile policy-as-code kurmak, constraint template yazmak veya “hangi kural hangi resource’u blokladı?” sorusunu çözmek gerektiğinde kullan. Amaç: **yeniden kullanılabilir admission politikalarını şeffaf şekilde işletmektir**.
---

## Purpose
Bu skill’in çıktısı:
- ConstraintTemplate + Constraint ayrımı
- Kuralın hangi metadata/spec alanlarını denetlediği
- Doğrulama: audit ve admission sonuçları

## Workflow
- Politikayı modelle:
  - Tekrar kullanılabilir mantık mı, tek namespace’e özel istisna mı?
- Template yaz:
  - Input alanlarını açık ve dar tut.
- Constraint uygula:
  - Match kapsamı ve istisnaları belirt.
- Audit vs deny:
  - Önce audit modunda gözlemleyip sonra enforce düşün.
- Doğrulama:
  - İhlalli ve uyumlu örnek resource ile sonucu test et.

## Common mistakes
- Çok genel match ile sistem bileşenlerini istemeden bloklamak.
- Gatekeeper audit sonuçlarını hiç incelememek.

## References
- `skills/k8s-sec-admission-webhooks`
- `skills/k8s-sec-rbac-least-privilege`
