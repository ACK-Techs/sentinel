---
name: k8s-net-traefik-tls
description: "Traefik ile TLS termination kurmak, sertifika secret veya cert-manager entegrasyonu yapmak ya da “HTTPS geliyor ama certificate/redirect bozuk” problemini çözmek gerektiğinde kullan. Amaç: **sertifika yaşam döngüsü ile routing’i birlikte doğrulamaktır**."
---

## Purpose
Bu skill’in çıktısı:
- TLS entrypoint, secret/certificate kaynağı ve redirect kararı
- Sertifika yenileme/rotation akışı
- Doğrulama: sertifika zinciri, host eşleşmesi ve HTTPS yönlendirmesi

## Workflow
- Sertifika kaynağını seç:
  - Manuel secret mı, cert-manager mı, wildcard mı?
- Termination noktası:
  - TLS Traefik’te mi bitiyor, passthrough mu?
- Host ve SAN uyumu:
  - Sertifika tam hangi domain’leri kapsıyor?
- Redirect:
  - HTTP → HTTPS zorunlu mu?
- Doğrulama:
  - `curl -vk` veya tarayıcı ile cert subject/issuer/expiry kontrolü.
  - Yanlış certificate fallback var mı?

## Common mistakes
- Default certificate düşmesini fark etmemek.
- Secret namespace/attachment yanlışken route’u suçlamak.

## References
- `skills/k8s-sec-tls-cert-manager`
- `skills/k8s-net-traefik-dashboard`
