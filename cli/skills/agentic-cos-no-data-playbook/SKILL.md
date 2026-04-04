---
name: agentic-cos-no-data-playbook
description: Grafana’da “no data” için datasource, dashboard, scrape, ilişki ve zaman aralığı sırasıyla sistematik kontrol listesi verirken kullan.
---

## Amaç

Sıra: **(1) Datasource** tanımlı ve çalışıyor mu → **(2) Dashboard** doğru datasource’u kullanıyor mu → **(3) Scrape / hedef** (Prometheus) → **(4) Juju ilişkileri** (`cos-relation-*`) → **(5) Zaman aralığı** ve refresh. Resmi troubleshooting: Ubuntu Observability how-to bölümlerine köprü; spesifik URL’ler için güncel dokümantasyonda doğrula.

## Kapsam

### Dahil

- Metrik ve log “no data” ayrımı (hangi skill devreye girer).
- Faz 1 skill zincirine yönlendirme.

### Hariç

- Özel iş uygulaması metrik enstrümantasyonu.

## Kurallar

- Her adımda kullanıcıya tek net eylem; paralel spekülasyon yok.
- Prometheus ve Grafana skill’leri ile çelişen teşhis adımı verme.
- İki başarısız düzeltme denemesinden sonra dur (`PROJECT_ROOT.md`).

## Kontrol listesi

- [ ] Datasource test butonu / sorgu (uygunsa) yapıldı mı?
- [ ] Prometheus’ta hedef var mı?
- [ ] İlişki eksikliği `juju status` ile görülüyor mu?
- [ ] Zaman aralığı çok dar mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Datasource hata | URL / auth | `../agentic-troubleshoot-grafana` |
| Hedef yok | scrape | `../agentic-troubleshoot-prometheus` |
| Log yok | Loki | `../agentic-troubleshoot-loki` |

## İlgili belgeler ve skill'ler

- `../agentic-troubleshoot-grafana/SKILL.md`
- `../agentic-troubleshoot-prometheus/SKILL.md`
- `../agentic-troubleshoot-loki/SKILL.md`
- `../../skills/cos-relation-prometheus-grafana/SKILL.md`
- `https://documentation.ubuntu.com/observability/`
