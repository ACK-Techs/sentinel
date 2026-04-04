---
name: agentic-troubleshoot-loki
description: Loki log akışı yok, depolama ve charm hatalarında ilişki ve küme kontrolleri verirken kullan.
---

## Amaç

**Loki ↔ Grafana**: datasource ilişkisi Faz 1 `../../skills/cos-relation-loki-grafana/SKILL.md` ve `cos-deploy-loki`. **Log akışı yok**: pod durumu, PVC, charm `blocked` mesajı, sonra Grafana tarafında datasource seçimi (LogQL ayrıntısı bu skill’de zorunlu değil — yalnız “sorgu yolu var mı” seviyesi).

## Kapsam

### Dahil

- `loki-k8s` birim durumu ve temel `kubectl` kontrolleri.
- Ingress üzerinden erişim varsa path notları (`cos-ingress-config` ile uyum).

### Hariç

- Log retention tuning üretim politikası.

## Kurallar

- Faz 1 deploy skill’indeki charm adı ve aksiyonlar önceliklidir.
- Büyük log indirme önerme; önce küçük örnek.
- Şüphede Ubuntu Observability troubleshooting sayfalarına yönlendir.

## Kontrol listesi

- [ ] Loki pod’ları ready mi?
- [ ] Grafana’da Loki datasource tanımlı mı?
- [ ] Depolama hatası (disk dolu) var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| 500 query | Loki logları | Charm mesajı |
| Boş stream | Promtail/agent yok | Mimari kapsam dışı olabilir — kullanıcıya sor |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-loki/SKILL.md`
- `../../skills/cos-relation-loki-grafana/SKILL.md`
- `../agentic-troubleshoot-grafana/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
