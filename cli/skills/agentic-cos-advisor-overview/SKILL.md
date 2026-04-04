---
name: agentic-cos-advisor-overview
description: COS danışmanlığında Faz 1 bağlamını, bileşen haritasını ve doğru skill yönlendirmesini özetlerken kullan.
---

## Amaç

Bu skill, Faz 2 ajanının COS Lite sorularında önce hangi Faz 1 belge ve skill'lere bakacağını standartlaştırır. Amaç, Prometheus, Loki, Alertmanager, Grafana, Traefik ve Catalogue bileşenlerini aynı harita içinde açıklamak ve belirsizlikte operatörü doğru Faz 1 skill zincirine yönlendirmektir.

## Kapsam

- Dahil:
- Faz 1 `PROJECT_ROOT.md` ve COS mimarisiyle uyumlu yüksek seviye danışman özeti.
- Soru tipini kurulum, ilişki, ingress, endpoint veya teşhis başlığına ayırma.
- Hangi durumda hangi Faz 1 skill'e geçileceğini söyleme.
- Hariç:
- Yeni charm kombinasyonu, yeni kanal önerisi veya Faz 1 dokümanıyla çelişen mimari yorumu üretme.
- Resmi Ubuntu Observability dokümanı veya Faz 1 skill'lerinde olmayan kesin sürüm iddiası verme.

## Kurallar

- Önce şunu doğrula: kullanıcı hangi modelde çalışıyor, sorun hangi bileşende görülüyor, sorun kurulum mu yoksa işletim mi.
- Faz 1 belge veya skill ile çelişen bir durum görürsen yeni yorum üretme; ilgili Faz 1 skill'e yönlendir.
- Bileşen özeti şu sırayla anlatılır: Juju model ve deploy temeli, veri toplama, veri saklama, görselleştirme, alarm, ingress ve endpoint yayımı.
- Genel yönlendirme sırası:
1. Model ve temel kurulum için `../../skills/juju-model-cos/SKILL.md`, `../../skills/juju-bootstrap-microk8s/SKILL.md`, `../../skills/microk8s-install-base/SKILL.md`.
2. Bileşen kurulumu için ilgili `../../skills/cos-deploy-*/SKILL.md`.
3. Veri akışı veya datasource için `../../skills/cos-relation-prometheus-grafana/SKILL.md` ve `../../skills/cos-relation-loki-grafana/SKILL.md`.
4. Ingress ve dış erişim için `../../skills/cos-ingress-config/SKILL.md`.
5. Semptom bazlı işletim teşhisi için ilgili `../agentic-troubleshoot-*/SKILL.md`.
- Belirsizlikte kullanıcıya kısa bir karar ağacı ver:
1. Erişim yoksa Traefik veya endpoint tarafına bak.
2. UI açılıyor ama veri yoksa relation ve datasource tarafına bak.
3. Pod veya unit sağlıksızsa MicroK8s ve Juju işletim referansına dön.

## Kontrol listesi

- [ ] Sorunun hangi COS bileşeninde görüldüğü netleştirildi mi?
- [ ] Kullanıcının kurulum mu, ilişki mi, işletim mi sorduğu ayrıştırıldı mı?
- [ ] İlgili Faz 1 skill veya belgeye açık yönlendirme yapıldı mı?
- [ ] Belirsiz durumda “önce şunu doğrula” maddeleri verildi mi?
- [ ] Faz 1 ile çelişen yeni mimari varsayım üretilmedi mi?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| Hangi bileşenin sorunlu olduğu belirsiz | UI, relation, endpoint veya pod semptomunu ayır | Önce `../agentic-cos-no-data-playbook/SKILL.md` veya ilgili troubleshoot skill |
| Kurulum akışı karışmış | Model adı, MicroK8s tabanı, deploy sırası | `../../skills/juju-model-cos/SKILL.md` ve ilgili deploy skill |
| Erişim var ama veri yok | Grafana datasource, Prometheus relation, Loki relation | `../agentic-cos-no-data-playbook/SKILL.md` |
| Yetki veya komut hatası | Juju erişimi, MicroK8s grup üyeliği, `sudo` gereksinimi | `../agentic-juju-ops-reference/SKILL.md` ve `../agentic-microk8s-ops-reference/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../../documantations/PROJECT_ROOT.md`
- `../../documantations/ARCHITECTURE_COS.md`
- `../documantations/PROJECT_ROOT_PHASE2.md`
- `../documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `../../skills/juju-model-cos/SKILL.md`
- `../../skills/juju-bootstrap-microk8s/SKILL.md`
- `../../skills/cos-deploy-prometheus/SKILL.md`
- `../../skills/cos-deploy-loki/SKILL.md`
- `../../skills/cos-deploy-grafana/SKILL.md`
- `../../skills/cos-deploy-alertmanager/SKILL.md`
- `../../skills/cos-deploy-traefik/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
