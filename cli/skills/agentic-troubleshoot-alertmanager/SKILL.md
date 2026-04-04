---
name: agentic-troubleshoot-alertmanager
description: Alertmanager erişim, route görünürlüğü ve alarm teslim akışı sorunlarını teşhis ederken kullan.
---

## Amaç

Bu skill, Alertmanager tarafında UI erişimi, Juju application sağlığı ve alarm akışının beklenmediği gibi davranması durumlarında temel teşhis sırasını verir.

## Kapsam

- Dahil:
- Alertmanager application durumu, endpoint görünürlüğü ve relation kaynaklı blokajların ilk teşhisi.
- Ingress, unit ve pod semptomlarını ayırma.
- Hariç:
- Yeni alert route tasarımı, alıcı entegrasyonu veya özel bildirim politikası yazımı.

## Adımlar

1. Önce şunu doğrula: sorun Alertmanager UI erişimi mi, alarm oluşmaması mı, yoksa alarmın teslim edilmemesi mi.
2. Juju görünürlüğünü kontrol et:
   - `juju status --model cos alertmanager`
   - `juju show-unit alertmanager/0 --model cos`
3. Endpoint görünürlüğü için Traefik veya Catalogue bilgisini doğrula.
4. Application `blocked` veya `waiting` ise relation veya config mesajını incele; otomatik varsayım üretme.
5. Pod veya servis düzeyinde sorun şüphesi varsa MicroK8s kontrollerine dön.
6. Alarm akışı şikayetinde önce veri kaynağı ve kural üretim zincirinin ayrı bir konu olabileceğini belirt; Alertmanager'ı suçlamadan önce upstream doğrula.

## Kontrol listesi

- [ ] Alertmanager application ve unit durumu doğrulandı mı?
- [ ] URL veya ingress görünürlüğü kontrol edildi mi?
- [ ] Juju durum mesajı relation veya config eksikliğine işaret ediyor mu?
- [ ] Pod ve servis kontrolleri gerektiğinde yapıldı mı?
- [ ] Alarmın hiç üretilmemesi ile teslim edilememesi ayrıştırıldı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| UI açılmıyor | Traefik/Catalogue endpoint | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Application `blocked` | Juju status mesajı | `../../skills/cos-deploy-alertmanager/SKILL.md` |
| Pod çalışmıyor | `microk8s kubectl get pods -A` ve olaylar | `../agentic-microk8s-ops-reference/SKILL.md` |
| Alarm gelmiyor | Upstream kural veya veri akışı | İlgili Prometheus ve no data zinciri |
| Yetki veya action sorunu | Model bağlamı ve Juju erişimi | `../agentic-juju-ops-reference/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-alertmanager/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-troubleshoot-prometheus/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
