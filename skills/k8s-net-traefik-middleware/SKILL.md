---
name: k8s-net-traefik-middleware
description: "Traefik üzerinde strip-prefix, headers, redirect, rate-limit gibi middleware zinciri kurmak veya “route çalışıyor ama request davranışı yanlış” sorunlarını çözmek gerektiğinde kullan. Amaç: **router ile middleware sorumluluğunu ayırmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- Gerekli middleware zinciri ve sıralaması
- Traefik CRD/Ingress bağlama yaklaşımı
- Doğrulama: request/response header ve path davranış kanıtı

## Workflow
- İhtiyacı netleştir:
  - Path rewrite mı, security header mı, rate limit mi, auth proxy mi?
- Middleware seç ve sırala:
  - Rewrite önce mi, auth önce mi, header ekleme sonra mı?
- Bağlama noktası:
  - Router/IngressRoute üzerinde nasıl attach edilecek?
- Etkiyi test et:
  - Özellikle `stripPrefix` sonrası backend path beklentisini doğrula.
- Doğrulama:
  - `curl -I` ve örnek request ile header/path sonucu.

## Common mistakes
- Middleware sırasını rastgele vermek: rewrite sonrası auth veya CORS bozulabilir.
- Rate limit’i yanlış scope’ta uygulamak.

## References
- `skills/k8s-net-traefik-tls`
- `skills/cos-ingress-config`
