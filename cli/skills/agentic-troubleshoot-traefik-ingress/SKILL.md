---
name: agentic-troubleshoot-traefik-ingress
description: Traefik ingress, proxied endpoint ve dış erişim sorunlarını teşhis ederken kullan.
---

## Amaç

Bu skill, COS bileşenlerine dış erişim sağlanamadığında Traefik, servis yayımı ve endpoint görünürlüğünü tutarlı biçimde incelemek için kullanılır.

## Kapsam

- Dahil:
- Traefik application sağlığı, proxied endpoint görünürlüğü ve Catalogue URL doğrulaması.
- MicroK8s servis görünürlüğü ve dış IP ataması için başlangıç kontrolleri.
- Hariç:
- Yeni ingress tasarımı, DNS mimarisi veya TLS terminasyon politikası üretme.

## Adımlar

1. Önce şunu doğrula: sorun tek bir uygulamada mı, tüm COS endpoint'lerinde mi.
2. Juju tarafında Traefik durumunu kontrol et:
   - `juju status --model cos traefik`
   - `juju show-unit traefik/0 --model cos`
3. Proxied endpoint bilgisini al:
   - `juju run traefik/0 show-proxied-endpoints --model cos`
4. Catalogue görünürlüğünü karşılaştır:
   - `juju show-unit catalogue/0 --model cos`
5. Kubernetes servis görünürlüğünü doğrula:
   - `microk8s kubectl get svc -A`
   - `microk8s kubectl describe svc -A`
6. Dış IP veya LoadBalancer görünmüyorsa önce MicroK8s ağı ve Faz 1 ingress kurulum adımlarını karşılaştır.
7. Yetki veya erişim hatasında Juju ve MicroK8s işletim referanslarına dön.

## Kontrol listesi

- [ ] Traefik application ve unit durumu doğrulandı mı?
- [ ] `show-proxied-endpoints` çıktısı alındı mı?
- [ ] Catalogue içindeki URL alanları karşılaştırıldı mı?
- [ ] Kubernetes servis ve dış IP durumu doğrulandı mı?
- [ ] Sorunun tek endpoint mi yoksa tüm ingress katmanı mı olduğu ayrıştırıldı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| 404 veya bağlantı yok | Proxied endpoints ve service görünürlüğü | `../../skills/cos-ingress-config/SKILL.md` |
| Dış IP yok | LoadBalancer veya servis yayımı | `../agentic-microk8s-ops-reference/SKILL.md` |
| Sadece bir uygulama açılmıyor | Catalogue URL ve ilgili app relation | İlgili bileşen troubleshoot skill'i |
| Traefik `blocked` | Juju status mesajı | `../../skills/cos-deploy-traefik/SKILL.md` |
| Juju veya K8s komutu yetki hatası veriyor | Kullanıcı erişimi, grup üyeliği, model bağlamı | İlgili ops reference skill |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-traefik/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-cos-catalogue-endpoints/SKILL.md`
- `../agentic-troubleshoot-grafana/SKILL.md`
