---
name: k8s-core-kustomize
description: "Kubernetes manifest’lerini base/overlay yapısıyla ortam bazlı yönetmek veya “aynı YAML’ın kopyaları drift olmuş” problemini çözmek gerektiğinde kullan. Amaç: **declarative farkları patch ile yönetmek**, şablon kopyası çoğaltmamaktır."
---

## Purpose
Bu skill’in çıktısı:
- Base ve overlay ayrımı
- Patch stratejisi (`patches`, image override, namePrefix/labels)
- Doğrulama: render edilen manifest’in beklenen farkları içerdiği kanıt

## Workflow
- Ortam farklarını sınıflandır:
  - Image tag, replica, ingress host, resource limit, secret referansı.
- Base’i sade tut:
  - Ortak kaynaklar base’te; ortam farkları overlay’de.
- Patch yöntemini seç:
  - Küçük alan farkı için patch.
  - Liste/alan override’larında stratejik merge veya JSON patch davranışını dikkatle seç.
- Adlandırma ve label:
  - Ortam etiketi ve ortak ownership label’ları tutarlı olsun.
- Doğrulama:
  - `kustomize build` veya `kubectl kustomize` çıktısını incele.
  - Overlay yanlışlıkla base’i aşırı değiştirmiş mi?

## Common mistakes
- Her ortam için tam kopya klasör: drift üretir.
- Çok fazla patch katmanı: okunabilirliği bozar.

## References
- `skills/k8s-core-helm-chart`
- `skills/gitops-monorepo-strategy`
