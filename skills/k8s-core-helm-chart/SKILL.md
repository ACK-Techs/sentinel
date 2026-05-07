---
name: k8s-core-helm-chart
description: "Helm chart yazmak, values yapısını tasarlamak veya “aynı uygulamayı farklı ortamlara parameterize ederek dağıtmak” gerektiğinde kullan. Amaç: **tekrar kullanılabilir chart üretmek**, sadece template doldurmak değildir."
---

## Purpose
Bu skill’in çıktısı:
- Chart yapısı ve values ayrımı
- Template’te hangi alanların parameterize edileceği kararı
- Doğrulama: `helm template/lint` ile render ve hata kontrolü

## Workflow
- Chart sınırını çiz:
  - Tek servis mi, bağımlı chart’lar da mı? subchart gerekli mi?
- Values tasarla:
  - Sık değişen alanları values’a çıkar; sabit altyapı detaylarını gereksiz parametreleştirme.
  - Secret değeri değil, secret referansı taşımayı tercih et.
- Template prensibi:
  - İsim/label helper’ları oluştur.
  - Koşullu kaynaklar (`ingress.enabled`, `autoscaling.enabled`) sade kalsın.
- Sürüm ve uyumluluk:
  - Image tag, chart version, appVersion farkını net tut.
- Doğrulama:
  - `helm lint`
  - `helm template` çıktısında namespace, selector ve values bağlamı doğru mu?

## Common mistakes
- Her alanı values yapmak: chart kullanımı zorlaşır.
- Selector label ile pod label’ın drift olması: rollout bozulur.

## References
- `skills/k8s-core-kustomize`
- `skills/gitops-helm-release`
