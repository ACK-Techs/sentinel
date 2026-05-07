---
name: k8s-core-labels-annotations
description: Kubernetes’te label/annotation stratejisi tasarlamak (selector tutarlılığı, metadata standardı, governance) veya “Service selector yanlış, pod’ları seçmiyor” gibi hataları çözmek gerektiğinde kullan. Odak: **etiket sözleşmesi** ve arama/otomasyon uyumudur.
---

## Purpose
Bu skill’in çıktısı:
- Label kontratı: zorunlu anahtarlar (`app.kubernetes.io/*`, `team`, `env`) ve değer kuralları
- Selector güvenliği: Deployment/Service/Ingress selector’larının drift olmamasını sağlayan pratikler
- Doğrulama: label query’leriyle doğru kaynakların seçildiğini kanıtlayan kontrol listesi

## Workflow
- Kontrat belirle:
  - Ownership: team, owner.
  - Ortam: env.
  - Uygulama kimliği: name/instance/version (k8s recommended keys).
- Label vs annotation:
  - Label: selector ve indexing (küçük, stabil).
  - Annotation: büyük/serbest metadata (build info, link, checksum).
- Selector tasarımı:
  - Service selector sadece stabil label’lara bağlansın (version ekleme).
  - Canary’de selector ayrımı nasıl yapılacak? (instance/track gibi).
- Drift önleme:
  - Kustomize/Helm template’lerinde label’ları tek kaynaktan üret.
  - PR review checklist: selector’lar değişti mi?
- Doğrulama:
  - `kubectl get pod -l <selector>` ile beklenen pod sayısı.
  - Service endpoints beklenen mi?

## Common mistakes
- Version/build id’yi Service selector’a koymak: rollout’ta trafik kesilir.
- Label’ları “her şeyi anlatacak” kadar çoğaltmak: yönetim ve hata riski artar.

## References
- `skills/k8s-core-kustomize`
- `skills/k8s-core-helm-chart`
