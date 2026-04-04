---
name: agentic-troubleshoot-prometheus
description: Prometheus hedef yok, scrape hatası, PVC ve charm blocked durumları için Juju ve küme kontrolleri verirken kullan.
---

## Amaç

**Juju**: `juju status` mesajları — `blocked`, `waiting`, hata metni. **Kubernetes**: pod logları, PVC bağlama (`kubectl describe` / `get pvc`). **Metrics endpoint ilişkileri**: Faz 1 `cos-relation-prometheus-grafana` ve deploy skill’lerindeki relation isimleri ile uyumlu kal; hedef keşfi için Prometheus UI veya API yolları yüksek seviyede, detay resmi doküman.

## Kapsam

### Dahil

- `prometheus-k8s` charm sağlık sinyalleri (isim Faz 1 ile aynı).
- Scrape/config sorunlarında yönlendirme.

### Hariç

- PromQL yazım eğitimi.

## Kurallar

- Faz 1 `../../skills/cos-deploy-prometheus/SKILL.md` komut ve kanal notlarına aykırı öneri verme.
- Uzun log çıktısı araç limitlerinde kırpılmalı.
- İki denemeden sonra kullanıcı onayı (`../../documantations/PROJECT_ROOT.md` protokolü).

## Kontrol listesi

- [ ] Prometheus pod’ları çalışıyor mu?
- [ ] Storage class / PVC hatası var mı?
- [ ] İlişkili exporter/scrape hedefleri tanımlı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| No targets | scrape config / relation | Faz 1 relation skill |
| PVC pending | Storage addon | `../../skills/microk8s-addons-dns-storage` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-prometheus/SKILL.md`
- `../../skills/cos-relation-prometheus-grafana/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
