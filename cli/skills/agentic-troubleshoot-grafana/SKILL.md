---
name: agentic-troubleshoot-grafana
description: Grafana giriş, datasource, boş pano ve admin parolası akışında COS ile uyumlu teşhis adımları verirken kullan.
---

## Amaç

**Admin parolası**: Faz 1 ile uyumlu — `juju run grafana/leader get-admin-password --model <model>` (`../../skills/cos-deploy-grafana/SKILL.md`). **Traefik URL**: `juju run traefik/0 show-proxied-endpoints` ve Catalogue; Grafana her zaman proxied listede olmayabilir — **`juju show-unit catalogue/0`** içindeki `url` alanlarına bakın (Faz 1 tutorial notu). **Boş pano / no data**: datasource ve ilişki zinciri → `../agentic-cos-no-data-playbook/SKILL.md`.

## Kapsam

### Dahil

- Giriş sorunları (yanlış parola, ingress yok).
- İlişki eksikliği belirtileri (yüksek seviye).

### Hariç

- Grafana plugin kurulumu (ürün dışı).

## Kurallar

- Komut örnekleri Faz 1 skill’lerden sapmamalı; yeni alt yol önermiyorsan “proje kararı gerektirir”.
- Parolayı log veya trajectory’ye yazma.
- Resmi: [Grafana-k8s actions](https://charmhub.io/grafana-k8s/actions).

## Kontrol listesi

- [ ] `grafana-k8s` `active` mi?
- [ ] `grafana-source` / dashboard ilişkileri kurulu mu (Faz 1 relation skill’leri)?
- [ ] Traefik / MetalLB önkoşulları sağlandı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| 404 ingress | show-proxied-endpoints / catalogue | `../../skills/cos-ingress-config` |
| Login fail | get-admin-password yeniden | Unit leader doğru mu |

## İlgili belgeler ve skill'ler

- `../../skills/cos-deploy-grafana/SKILL.md`
- `../../skills/cos-relation-prometheus-grafana/SKILL.md`
- `../../skills/cos-relation-loki-grafana/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
