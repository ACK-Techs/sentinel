---
name: agentic-troubleshoot-traefik-ingress
description: LoadBalancer IP yok, proxied endpoints boş ve TLS sorunlarında MetalLB ve Traefik kontrolleri verirken kullan.
---

## Amaç

**MetalLB önkoşulu**: MicroK8s `metallb` addon — Faz 1 `../../skills/cos-ingress-config/SKILL.md` ve `../../skills/microk8s-addons-dns-storage/SKILL.md`. **Proxied endpoints**: `juju run traefik/0 show-proxied-endpoints --format=yaml`. **Catalogue URL**: `juju show-unit catalogue/0`. **TLS**: sertifika ve path sorunlarında resmi “Gateway Address Unavailable” troubleshooting bağlantısı.

## Kapsam

### Dahil

- Traefik `LoadBalancer` servis IP’si yok senaryosu.
- Boş endpoint listesi — Catalogue alternatifi.

### Hariç

- Özel PKI tasarımı.

## Kurallar

- Faz 1 tutorial path yapısı ile çelişen kısa yol önerme.
- `curl` testlerinde kullanıcı ortamına göre `-k` kullanımı güvenlik uyarısı ile.
- Sorun devam ederse: [Troubleshoot gateway](https://documentation.ubuntu.com/observability/how-to/troubleshooting/troubleshoot-gateway-address-unavailable/).

## Kontrol listesi

- [ ] metallb atanmış IP aralığı doğru mu?
- [ ] Traefik charm `active` mı?
- [ ] DNS / hosts girişi test için uygun mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Pending external IP | metallb | Addon skill |
| Endpoints boş | İlişkiler | `cos-deploy-traefik`, ingress skill |

## İlgili belgeler ve skill'ler

- `../../skills/cos-ingress-config/SKILL.md`
- `../../skills/cos-deploy-traefik/SKILL.md`
- `../../skills/microk8s-addons-dns-storage/SKILL.md`
- `../agentic-cos-catalogue-endpoints/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
