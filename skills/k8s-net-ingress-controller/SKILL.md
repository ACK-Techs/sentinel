---
name: k8s-net-ingress-controller
description: HTTP(S) trafiğini Kubernetes Ingress ile yönlendirmek, uygun controller seçmek veya “host/path routing neden çalışmıyor?” sorunlarını çözmek gerektiğinde kullan. Amaç: **L7 giriş katmanını doğru controller mantığıyla kurmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Ingress resource + controller sorumluluk ayrımı
- Host/path routing, TLS ve class seçimi
- Doğrulama: istek gerçekten doğru backend’e gidiyor mu?

## Workflow
- Controller bağlamını sabitle:
  - NGINX mi, Traefik mi, MicroK8s addon mu?
- Kural tasarla:
  - Host bazlı mı, path bazlı mı, rewrite gerekiyor mu?
- IngressClass:
  - Cluster’da birden fazla controller varsa class açık yaz.
- TLS:
  - Termination nerede? secret var mı? redirect gerekir mi?
- Debug:
  - Ingress oluşmuş ama address gelmiş mi?
  - Controller log’u ve backend service endpoint’leri sağlıklı mı?
- Doğrulama:
  - `curl -H "Host: ..."` ile test.

## Common mistakes
- Ingress tanımlayıp controller kurulu varsaymak.
- Service/port yanlışken suçu Ingress’e yazmak.

## References
- `skills/k8s-net-traefik-tls`
- `skills/microk8s-addon-ingress`
