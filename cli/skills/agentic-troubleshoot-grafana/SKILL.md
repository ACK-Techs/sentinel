---
name: agentic-troubleshoot-grafana
description: Grafana erişim, parola, datasource ve boş pano sorunlarını teşhis ederken kullan.
---

## Amaç

Bu skill, Grafana tarafındaki erişim, giriş, datasource ve no data semptomlarını Faz 1 akışıyla uyumlu şekilde incelemeyi standartlaştırır. Belirsizlikte operatörü relation, ingress veya deploy skill'ine geri yönlendirir.

## Kapsam

- Dahil:
- Admin parola alma, endpoint doğrulama, datasource ve relation kontrolü.
- Boş pano veya datasource görünmeme semptomlarını ayırma.
- Hariç:
- Grafana plugin kurulumu, özel dashboard geliştirme veya Faz 1 dışı entegrasyonlar.

## Adımlar

1. Önce şunu doğrula: sorun login mi, URL erişimi mi, datasource mu, yoksa no data mı.
2. Uygulama durumunu kontrol et:
   - `juju status --model cos grafana`
   - `juju show-unit grafana/0 --model cos`
3. Giriş sorunu varsa Faz 1 action ile hizalı admin parola akışını kullan:
   - `juju run grafana/leader get-admin-password --model cos`
4. Endpoint görünürlüğünü doğrula:
   - `juju run traefik/0 show-proxied-endpoints --model cos`
   - Gerekirse `juju show-unit catalogue/0 --model cos` içindeki URL alanlarını kontrol et.
5. Grafana açılıyor ama veri yoksa:
   - Datasource'ların UI'da göründüğünü doğrula.
   - Prometheus ve Loki relation'larını Faz 1 relation skill'leriyle karşılaştır.
   - Gerekirse `../agentic-cos-no-data-playbook/SKILL.md` zincirine geç.
6. Yetki veya action hatası varsa leader unit, model ve Juju erişimini yeniden doğrula.

## Kontrol listesi

- [ ] Grafana application durumu `active` veya beklenen durumda mı?
- [ ] Admin parola akışı Faz 1 ile aynı action üzerinden doğrulandı mı?
- [ ] Traefik veya Catalogue üzerinden erişim URL'si doğrulandı mı?
- [ ] Prometheus ve Loki datasource relation'ları kontrol edildi mi?
- [ ] Parola veya token loga yazılmadı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| Login başarısız | Leader unit ve admin password action | `../../skills/cos-deploy-grafana/SKILL.md` |
| 404 veya erişim yok | Traefik proxied endpoints ve Catalogue URL | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Datasource görünmüyor | Prometheus veya Loki relation durumu | İlgili Faz 1 relation skill'i |
| Pano açılıyor ama veri yok | Datasource health, zaman aralığı, relation | `../agentic-cos-no-data-playbook/SKILL.md` |
| Action başarısız | `juju debug-log` ve model bağlamı | `../agentic-juju-ops-reference/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-grafana/SKILL.md`
- `../../skills/cos-relation-prometheus-grafana/SKILL.md`
- `../../skills/cos-relation-loki-grafana/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
