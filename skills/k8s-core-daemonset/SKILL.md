---
name: k8s-core-daemonset
description: DaemonSet ile her node’a agent/sidecar-servis deploy etmek (log/metrics/CSI gibi), taint/toleration ve node selector kurallarını uygulamak veya “bazı node’larda pod yok” sorununu çözmek gerektiğinde kullan. Odak: **node kapsama garantisi** ve scheduling kurallarıdır.
---

## Purpose
Bu skill’in çıktısı:
- DaemonSet yerleşim stratejisi (hangi node’lar dahil/haric, tolerations, selectors)
- Upgrade/rollback davranışı (maxUnavailable, surge yokluğu) ve risk notu
- Doğrulama: beklenen node sayısı kadar pod + taint’li node’larda kapsama kanıtı

## Workflow
- Kapsamı tanımla:
  - Tüm node’lar mı, sadece worker mı, GPU node’lar mı?
- Scheduling kuralları:
  - Node selector/affinity ile hedefle.
  - Control-plane node’lara gidecekse uygun tolerations’ı bilinçli ekle.
- Upgrade stratejisi:
  - RollingUpdate ve `maxUnavailable` ile kontrollü upgrade.
  - DaemonSet’te “surge” yok; kapasite etkisini yaz.
- Kaynaklar:
  - DaemonSet agent’ları node’da sürekli çalışır; requests/limits ayarla.
- Doğrulama:
  - `desiredNumberScheduled == currentNumberScheduled` mi?
  - Taint’li node’larda pod var mı? (isteniyorsa)

## Common mistakes
- Toleration’ı eksik bırakmak: bazı node’larda pod hiç oluşmaz.
- “Her node’a” deyip control-plane’de istemeden çalıştırmak: güvenlik/performans riski.

## References
- `skills/k8s-core-taints-tolerations`
