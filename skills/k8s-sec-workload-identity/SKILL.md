---
name: k8s-sec-workload-identity
description: "Kubernetes workload’larının cloud veya harici platform kimliği almasını sağlamak, statik cloud credential’dan çıkmak veya “pod hangi kimlikle erişiyor?” sorusunu çözmek gerektiğinde kullan. Amaç: **workload kimliğini pod identity ile güvenli eşlemektir**."
---

## Purpose
Bu skill’in çıktısı:
- Workload identity akışı ve trust ilişkisi
- ServiceAccount ↔ cloud role eşlemesi
- Doğrulama: pod beklenen kimlikle erişiyor mu?

## Workflow
- Hedef sistemi belirle:
  - AWS/GCP/Azure veya başka federated kimlik?
- Eşleme:
  - Hangi ServiceAccount hangi role/principal’a bağlanacak?
- Scope:
  - Namespace/app bazında en küçük izin seti.
- Migration:
  - Statik secret credential’lardan nasıl çıkılacak?
- Doğrulama:
  - Pod içinden token/identity test ve hedef kaynağa erişim denemesi.

## Common mistakes
- Birden çok workload’a aynı geniş rolü vermek.
- Federated trust policy’yi fazla geniş bırakmak.

## References
- `skills/k8s-core-service-account`
- `cli/skills/agentic-secrets-handling`
