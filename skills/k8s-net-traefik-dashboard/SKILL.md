---
name: k8s-net-traefik-dashboard
description: Traefik dashboard erişimini açmak, güvenli hale getirmek veya router/service görünürlüğüyle ingress sorunlarını teşhis etmek gerektiğinde kullan. Amaç: **dashboard’u debug aracı olarak kullanmak**, herkese açık bırakmak değildir.
---

## Purpose
Bu skill’in çıktısı:
- Dashboard erişim modeli (internal only, auth-protected, temporary)
- Dashboard üzerinden router/service/middleware inceleme akışı
- Doğrulama: dashboard görülebiliyor ve yanlış expose edilmiyor

## Workflow
- Erişim modelini seç:
  - Sadece cluster içi mi, VPN arkasında mı, basic auth mı?
- Publish et:
  - IngressRoute veya port-forward ile erişim yolunu belirle.
- Güvenlik:
  - Public internete çıplak dashboard açma.
  - Gerekirse IP allow-list veya auth ekle.
- Debug kullanımı:
  - Route attach olmuş mu, middleware var mı, backend healthy mi?
- Doğrulama:
  - Dashboard açılıyor mu?
  - Dışarıdan yetkisiz erişim yok mu?

## Common mistakes
- Prod dashboard’u auth’suz yayınlamak.
- Dashboard açık ama asıl controller log’una hiç bakmamak.

## References
- `skills/k8s-net-traefik-middleware`
- `skills/k8s-net-ingress-controller`
