---
name: k8s-core-service-account
description: ServiceAccount ile workload identity kurmak, token projection (bound service account token) kullanmak veya “pod içinden API’ye erişemiyor / yanlış SA kullanıyor” sorunlarını çözmek gerektiğinde kullan. Odak: **identity bağlama + token ömrü/güvenlik**.
---

## Purpose
Bu skill’in çıktısı:
- SA + RBAC binding taslağı (workload’a doğru SA bağlama)
- Token projection stratejisi (kısa ömürlü token, audience) ve güvenlik notu
- Doğrulama: pod içinden `kubectl`/API çağrısı ile erişim kanıtı

## Workflow
- Identity ihtiyacını yaz:
  - Workload hangi API’ye erişecek? sadece read mi, write mı?
- SA bağla:
  - Pod spec’te `serviceAccountName` ile bağla; default SA’yı kullanma.
- Token yönetimi:
  - Bound token projection kullan (kısa TTL, audience).
  - Token’ı dosya olarak mount et; log’a basma.
- RBAC:
  - SA için minimum Role/ClusterRole ve binding.
- Doğrulama:
  - Pod içinde SA token var mı?
  - `kubectl auth can-i` ve/veya API call ile izin çalışıyor mu?

## Common mistakes
- Default ServiceAccount ile prod workload çalıştırmak: görünmez yetki sızıntıları.
- Uzun ömürlü token’ı “secret” olarak dağıtmak: rotasyon ve sızıntı riski.

## References
- `skills/k8s-core-rbac`
- `skills/k8s-sec-workload-identity`
