---
name: k8s-core-namespace
description: Namespace oluşturup izolasyon kurmak (ResourceQuota, LimitRange, default policy) veya “bir ekip diğerinin kaynaklarını tüketiyor / prod ile staging karışıyor” sorunlarını çözmek gerektiğinde kullan. Odak: **multi-tenant cluster hijyeni**.
---

## Purpose
Bu skill’in çıktısı:
- Namespace standardı: isimlendirme, label set’i, owner/team metadata
- ResourceQuota + LimitRange taslağı (kapsam ve gerekçe)
- Doğrulama: quota/limit’in gerçekten uygulandığını kanıtlayan örnek test

## Workflow
- Sınırı tanımla:
  - Takım/ortam bazlı namespace mi? (örn. `team-a-prod`)
- Metadata standardı:
  - `team`, `env`, `cost-center` gibi label/annotation’ları sabitle.
- Quota tasarımı:
  - CPU/memory/pod sayısı gibi limitler; “burst” ihtiyacı varsa not et.
- LimitRange:
  - Default requests/limits ile “requests yok” workloads’u disipline et.
- Politikalar:
  - NetworkPolicy, Pod Security Standard gibi “namespace default”larını bağla.
- Doğrulama:
  - Quota’yı aşan örnek deployment dene → beklenen hata mesajı.

## Common mistakes
- Namespace açıp quota koymamak: noisy neighbor devam eder.
- Prod/staging aynı namespace: yanlış config ve erişim riski.

## References
- `skills/k8s-scale-resource-quotas`
- `skills/k8s-sec-pod-security-standards`
