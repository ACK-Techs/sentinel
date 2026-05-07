---
name: k8s-sec-secrets-management
description: "Kubernetes secret yönetimini güvenli hale getirmek, External Secrets/Vault entegrasyonu düşünmek veya “secret’lar nasıl dönecek/yenilenecek?” sorusunu cevaplamak gerektiğinde kullan. Amaç: **secret yaşam döngüsünü YAML’dan ayırmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Native Secret vs external secret store kararı
- Secret dağıtım/rotation modeli
- Doğrulama: workload secret’ı alıyor mu, yenilenme davranışı nasıl?

## Workflow
- Secret tipini ayır:
  - Statik kısa ömürlü mü, sık dönen credential mı?
- Saklama modeli:
  - Native Secret sadece referans mı olacak, değer dış sistemden mi gelecek?
- Dağıtım:
  - Env var mı, volume mount mı, sidecar/helper mı?
- Rotation:
  - Secret değişince app yeniden başlatılmalı mı, hot reload var mı?
- Doğrulama:
  - Secret erişimi sınırlı mı, log’a sızmıyor mu?

## Common mistakes
- Git’e base64 secret koyup “şifreli” sanmak.
- Rotation ihtiyacı olan credential’ı statik Secret’a gömmek.

## References
- `cli/skills/agentic-secrets-handling`
- `skills/k8s-core-configmap-secret`
