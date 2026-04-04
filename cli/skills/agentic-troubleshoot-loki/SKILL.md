---
name: agentic-troubleshoot-loki
description: Loki log akışı, datasource görünürlüğü ve sorgu sonucu eksikliği sorunlarını teşhis ederken kullan.
---

## Amaç

Bu skill, Loki'nin log kabul etmemesi, Grafana'da datasource görünmemesi veya sorgularda sonuç dönmemesi gibi semptomları tutarlı bir sırayla incelemek için kullanılır.

## Kapsam

- Dahil:
- Loki application sağlığı, relation görünürlüğü ve Grafana datasource akışı.
- Log verisi görünmeme semptomunun relation, ingress veya pod tarafında mı olduğunu ayırma.
- Hariç:
- Özel retention, index veya dış obje depolama tasarımı.

## Adımlar

1. Önce şunu doğrula: sorun Loki URL erişimi mi, Grafana datasource'u mu, yoksa log sorgularının boş dönmesi mi.
2. Juju durumunu kontrol et:
   - `juju status --model cos loki`
   - `juju show-unit loki/0 --model cos`
   - `juju status --model cos --relations`
3. Grafana entegrasyonunu Faz 1 relation skill'i ile karşılaştır:
   - `../../skills/cos-relation-loki-grafana/SKILL.md`
4. UI erişimi yoksa Traefik veya Catalogue görünürlüğünü kontrol et.
5. Pod veya servis seviyesi hata şüphesinde MicroK8s kontrollerine dön.
6. “Log yok” durumunda önce veri yolunu doğrula; doğrudan sorgu sözdizimine takılma:
   - Relation var mı
   - Datasource sağlıklı mı
   - Zaman aralığı doğru mu

## Kontrol listesi

- [ ] Loki application ve unit durumu doğrulandı mı?
- [ ] Grafana ile Loki relation görünürlüğü kontrol edildi mi?
- [ ] Erişim endpoint'i Traefik veya Catalogue üzerinden doğrulandı mı?
- [ ] Pod ve servis durumu MicroK8s tarafında kontrol edildi mi?
- [ ] “Veri yok” kararı vermeden önce zaman aralığı ve datasource sağlık durumu doğrulandı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| Grafana'da Loki datasource yok | Relation kurulumu | `../../skills/cos-relation-loki-grafana/SKILL.md` |
| Loki UI veya endpoint açılmıyor | Traefik/Catalogue görünürlüğü | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Sorgu boş dönüyor | Zaman aralığı, datasource health, relation | `../agentic-cos-no-data-playbook/SKILL.md` |
| Application `blocked` | Juju relation ve config mesajı | `../../skills/cos-deploy-loki/SKILL.md` |
| Pod restart ediyor | K8s olayları ve loglar | `../agentic-microk8s-ops-reference/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-loki/SKILL.md`
- `../../skills/cos-relation-loki-grafana/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
