---
name: agentic-troubleshoot-alertmanager
description: Alertmanager ready endpoint, routing ve sessiz uyarılar için ingress ve ilişki kontrolleri verirken kullan.
---

## Amaç

**Ready endpoint**: pod IP + path örneği Faz 1 `../../skills/cos-ingress-config/SKILL.md` (ör. `/-/ready` ingress path ile birlikte). **Ingress path örnekleri**: `http://<LB>/cos-alertmanager/...` yapısı tutorial ile uyumlu kabul; kesin path için `show-proxied-endpoints` ve doküman. **Routing / sessiz uyarı**: Prometheus → Alertmanager ilişkisi ve notification channel Faz 1 `cos-deploy-alertmanager` ve ilişki skill’lerinde.

## Kapsam

### Dahil

- Charm `blocked` / `error` özet teşhisi.
- Traefik / Catalogue URL keşfi yönlendirmesi.

### Hariç

- PagerDuty entegrasyon kurulumu (operasyonel karar).

## Kurallar

- Faz 1 skill komutlarıyla çelişme yok.
- Uyarı “sessiz” ise önce Alertmanager UI/endpoint, sonra Prometheus rule yükleme (yüksek seviye).
- TLS sorunları `../agentic-troubleshoot-traefik-ingress/SKILL.md` ile örtüşebilir.

## Kontrol listesi

- [ ] `alertmanager-k8s` aktif mi?
- [ ] Ingress’ten ready yanıt alınıyor mu?
- [ ] Prometheus alerting ilişkisi kurulu mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| 502 ingress | Traefik / backend | `../../skills/cos-deploy-traefik` |
| No alerts | Rule yok | Prometheus skill zinciri |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-alertmanager/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-troubleshoot-prometheus/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
