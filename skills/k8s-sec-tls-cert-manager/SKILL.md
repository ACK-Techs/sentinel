---
name: k8s-sec-tls-cert-manager
description: "cert-manager ile sertifika yaşam döngüsü otomasyonu kurmak, issuer/clusterissuer seçmek veya “certificate pending / renew olmuyor” sorunlarını çözmek gerektiğinde kullan. Amaç: **TLS’i manuel secret kopyalamaktan çıkarmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Issuer/ClusterIssuer ve challenge akışı
- Certificate kaynağı ve yenileme davranışı
- Doğrulama: secret oluşumu ve başarılı renew kanıtı

## Workflow
- Sertifika kaynağını belirle:
  - Let’s Encrypt, internal CA, self-signed?
- Scope:
  - Namespace issuer yeterli mi, cluster-wide issuer mı?
- Challenge türü:
  - HTTP-01 mi DNS-01 mi? ingress/DNS erişimi uygun mu?
- Yenileme:
  - Secret rotation uygulamayı nasıl etkileyecek?
- Doğrulama:
  - Certificate resource durumu, secret oluşumu, gerçek TLS testi.

## Common mistakes
- Wildcard gereksinimi varken HTTP-01 düşünmek.
- Renew’ü test etmeden sadece ilk issuance’a bakmak.

## References
- `skills/k8s-net-traefik-tls`
- `skills/cos-ingress-config`
