---
name: agentic-troubleshoot-prometheus
description: Prometheus scrape, hedef görünürlüğü ve veri akışı sorunlarını teşhis ederken kullan.
---

## Amaç

Bu skill, Prometheus tarafında veri toplanmaması, hedeflerin `down` görünmesi veya Grafana datasource akışının bozulması gibi semptomları sistematik biçimde incelemek için kullanılır.

## Kapsam

- Dahil:
- Application ve unit sağlığı, relation görünürlüğü, hedef scrape semptomları.
- Grafana ile veri akışının neden kesildiğini anlamak için başlangıç teşhisi.
- Hariç:
- Yeni scrape job tasarımı veya Prometheus kural dosyası özelleştirmesi.

## Adımlar

1. Önce şunu doğrula: sorun Prometheus UI erişimi mi, hedeflerin durumu mu, yoksa Grafana'da veri görünmemesi mi.
2. Juju tarafını kontrol et:
   - `juju status --model cos prometheus`
   - `juju show-unit prometheus/0 --model cos`
   - `juju status --model cos --relations`
3. Ingress veya URL sorunu varsa Traefik ve Catalogue görünürlüğünü doğrula.
4. Grafana veri sorunu varsa Prometheus relation akışını Faz 1 skill ile karşılaştır:
   - `../../skills/cos-relation-prometheus-grafana/SKILL.md`
5. Pod veya servis seviyesi şüphe varsa MicroK8s tarafına dön:
   - `microk8s kubectl get pods -A`
   - `microk8s kubectl get svc -A`
6. Semptom “hedefler down” ise önce relation ve endpoint yayınını doğrula; doğrudan scrape config varsayımı yapma.

## Kontrol listesi

- [ ] Prometheus application ve unit durumu doğrulandı mı?
- [ ] Relation görünürlüğü `juju status --relations` ile kontrol edildi mi?
- [ ] Erişim sorunu varsa Traefik veya Catalogue ile URL doğrulandı mı?
- [ ] Grafana tarafındaki datasource akışı Faz 1 relation skill ile karşılaştırıldı mı?
- [ ] Pod veya servis düzeyi hata için MicroK8s kontrolleri yapıldı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| Prometheus açılmıyor | Traefik/Catalogue URL ve servis durumu | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Grafana'da Prometheus datasource yok | Relation kurulumu | `../../skills/cos-relation-prometheus-grafana/SKILL.md` |
| Hedefler `down` | Relation ve pod olayları | `../agentic-microk8s-ops-reference/SKILL.md` |
| Application `blocked` | `juju status` mesajı ve relation bekleyişi | İlgili deploy skill |
| Veri gecikmeli veya yok | Zaman aralığı, relation, no data zinciri | `../agentic-cos-no-data-playbook/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-prometheus/SKILL.md`
- `../../skills/cos-relation-prometheus-grafana/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
