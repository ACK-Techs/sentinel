---
name: k8s-sec-admission-webhooks
description: "Validating veya Mutating admission webhook tasarlamak, cluster politikasını API girişinde uygulamak veya “resource create olurken neden mutate/reject oluyor?” sorunlarını çözmek gerektiğinde kullan. Amaç: **admission zincirini güvenli ve öngörülebilir kurmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Mutating vs Validating webhook kararı
- Failure policy, scope ve timeout yaklaşımı
- Doğrulama: örnek resource ile webhook etkisinin kanıtı

## Workflow
- Webhook rolünü seç:
  - Default ekleme/mutate mi, kural denetimi/reject mi?
- Scope:
  - Hangi resource, namespace, operation’lara uygulanacak?
- Güvenlik ve dayanıklılık:
  - `failurePolicy=Fail` mi `Ignore` mu?
  - Timeout kısa mı, HA gerekliliği var mı?
- Yan etki:
  - Sonsuz mutate döngüsü veya beklenmeyen patch riski var mı?
- Doğrulama:
  - Örnek create/update çağrısında beklenen mutate veya reject gerçekleşiyor mu?

## Common mistakes
- Kritik webhook’u tek replica ve uzun timeout ile çalıştırmak.
- Kapsamı çok geniş verip cluster API’sini yavaşlatmak.

## References
- `skills/k8s-sec-opa-gatekeeper`
- `skills/k8s-sec-pod-security-standards`
