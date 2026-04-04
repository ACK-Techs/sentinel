---
name: agentic-cos-no-data-playbook
description: COS içinde “no data” semptomunu relation, datasource ve endpoint zinciri üzerinden teşhis ederken kullan.
---

## Amaç

Bu skill, Grafana panolarında veya COS UI'larında görülen “no data” semptomunu sistematik biçimde ayırmak için kullanılır. Amaç, veri yok sorununu veri kaynağı yokluğu, relation eksikliği, datasource görünürlüğü, yanlış zaman aralığı veya ingress yanılgısından ayırmaktır.

## Kapsam

- Dahil:
- Grafana, Prometheus ve Loki arasında relation ve datasource akışının kontrolü.
- Endpoint, ingress ve uygulama sağlığı ile no data semptomunu ilişkilendirme.
- Hariç:
- Uygulama içi metrik üretimi veya özel log pipeline tasarımı.

## Adımlar

1. Önce şunu doğrula: “no data” hangi ekranda görülüyor, hangi zaman aralığında görülüyor, tüm datasource'larda mı yoksa tek bir datasource'da mı.
2. Grafana erişimini ve datasource görünürlüğünü doğrula:
   - Gerekirse `../agentic-troubleshoot-grafana/SKILL.md`
3. Prometheus veri yolu için relation zincirini kontrol et:
   - `../../skills/cos-relation-prometheus-grafana/SKILL.md`
   - `../agentic-troubleshoot-prometheus/SKILL.md`
4. Loki veri yolu için relation zincirini kontrol et:
   - `../../skills/cos-relation-loki-grafana/SKILL.md`
   - `../agentic-troubleshoot-loki/SKILL.md`
5. Endpoint veya URL belirsizliği varsa:
   - `../agentic-cos-catalogue-endpoints/SKILL.md`
   - `../agentic-troubleshoot-traefik-ingress/SKILL.md`
6. Uygulama veya pod sağlığı şüphesi varsa:
   - `../agentic-juju-ops-reference/SKILL.md`
   - `../agentic-microk8s-ops-reference/SKILL.md`
7. Relation eksikliği veya datasource görünmezliği doğrulanmadan “uygulama veri üretmiyor” sonucuna atlama.

## Kontrol listesi

- [ ] Sorunun tek datasource mu yoksa genel bir “no data” semptomu mu olduğu ayrıştırıldı mı?
- [ ] Zaman aralığı ve yanlış dashboard filtreleri kontrol edildi mi?
- [ ] Prometheus-Grafana relation zinciri doğrulandı mı?
- [ ] Loki-Grafana relation zinciri doğrulandı mı?
- [ ] Endpoint ve ingress görünürlüğü kontrol edildi mi?
- [ ] Juju ve MicroK8s sağlığı gerektiğinde çapraz kontrol edildi mi?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| Grafana açılıyor ama tüm panolar boş | Datasource health ve relation zinciri | Grafana ve ilgili relation skill |
| Sadece Prometheus verisi yok | Prometheus relation ve app sağlığı | `../agentic-troubleshoot-prometheus/SKILL.md` |
| Sadece Loki logları yok | Loki relation ve app sağlığı | `../agentic-troubleshoot-loki/SKILL.md` |
| URL doğru değil | Catalogue ve Traefik endpoint görünürlüğü | `../agentic-cos-catalogue-endpoints/SKILL.md` |
| Unit veya pod sağlıksız | Juju status ve K8s pod olayları | `../agentic-juju-ops-reference/SKILL.md` ve `../agentic-microk8s-ops-reference/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../../skills/cos-relation-prometheus-grafana/SKILL.md`
- `../../skills/cos-relation-loki-grafana/SKILL.md`
- `../../skills/cos-ingress-config/SKILL.md`
- `../agentic-troubleshoot-grafana/SKILL.md`
- `../agentic-troubleshoot-prometheus/SKILL.md`
- `../agentic-troubleshoot-loki/SKILL.md`
- `../agentic-cos-catalogue-endpoints/SKILL.md`
- `../agentic-troubleshoot-traefik-ingress/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
