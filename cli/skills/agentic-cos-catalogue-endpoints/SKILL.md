---
name: agentic-cos-catalogue-endpoints
description: COS Catalogue ve proxied endpoint görünürlüğünü doğrularken kullan.
---

## Amaç

Bu skill, COS bileşenlerinin kullanıcıya sunulan URL'lerini Catalogue ve Traefik bilgileri üzerinden doğrulamak için kullanılır. Amaç, “hangi endpoint doğru” belirsizliğini azaltmak ve yanlış URL nedeniyle açılmayan servisleri ayırmaktır.

## Kapsam

- Dahil:
- Catalogue içindeki URL alanları ve Traefik proxied endpoint çıktıları.
- Bileşenlerin beklenen erişim adreslerini karşılaştırma.
- Hariç:
- DNS, sertifika veya dış load balancer mimarisi tasarımı.

## Adımlar

1. Önce şunu doğrula: kullanıcı hangi bileşene erişmeye çalışıyor ve mevcut kullandığı URL nedir.
2. Catalogue görünürlüğünü incele:
   - `juju show-unit catalogue/0 --model cos`
3. Traefik tarafından yayımlanan endpoint'leri incele:
   - `juju run traefik/0 show-proxied-endpoints --model cos`
4. Gerekirse uygulama durumunu karşılaştır:
   - `juju status --model cos`
5. Catalogue ile Traefik çıktısı uyuşmuyorsa önce relation ve ingress tarafını doğrula; rastgele URL verme.
6. Bir URL görünmüyor ama uygulama `active` ise ilgili bileşenin ingress veya relation gereksinimini Faz 1 skill ile karşılaştır.

## Kontrol listesi

- [ ] Hangi bileşen için endpoint arandığı net mi?
- [ ] Catalogue çıktısı alındı mı?
- [ ] Traefik proxied endpoint çıktısı alındı mı?
- [ ] Uygulama durumu `juju status` ile karşılaştırıldı mı?
- [ ] Son önerilen URL Faz 1 deploy veya ingress akışıyla çelişmiyor mu?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| URL hiç görünmüyor | Traefik proxied endpoints ve app durumu | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Catalogue boş veya eksik | `catalogue/0` unit durumu | İlgili deploy ve Juju ops skill |
| Yanlış URL ile erişim denenmiş | Kullanıcının kullandığı adres ile gerçek endpoint'i karşılaştır | Doğru endpoint'i paylaş, gerekirse ingress skill'e dön |
| Tek bileşen eksik | İlgili app relation veya deploy durumu | İlgili troubleshoot skill |

## İlgili belgeler ve skill'ler

- `../../skills/cos-ingress-config/SKILL.md`
- `../../skills/cos-deploy-grafana/SKILL.md`
- `../../skills/cos-deploy-prometheus/SKILL.md`
- `../../skills/cos-deploy-loki/SKILL.md`
- `../../skills/cos-deploy-alertmanager/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
