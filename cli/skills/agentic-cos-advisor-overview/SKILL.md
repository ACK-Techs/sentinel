---
name: agentic-cos-advisor-overview
description: Danışman ajanının COS Lite bileşen haritası ve Faz 1 belge/skill okuma sırasını yönlendirirken kullan.
---

## Amaç

Ajan, COS sorularında **`../../documantations/PROJECT_ROOT.md`**, **`../../documantations/ARCHITECTURE_COS.md`**, **`../../documantations/IMPLEMENTATION_PLAN.md`** ile **Faz 1 skill** zincirine yönlendirir. Bileşen haritası: Prometheus, Loki, Alertmanager, Grafana, Traefik, Catalogue — Juju modelinde charm ilişkileri Faz 1 `cos-relation-*` ve `cos-deploy-*` skill’lerinde tanımlıdır; burada yalnız **okuma sırası** ve **hangi skill ne zaman** özeti verilir.

## Kapsam

### Dahil

- Yüksek seviye COS Lite akışı ve Ubuntu Observability resmi dokümanına köprü.
- `agentic-troubleshoot-*` skill’lerine yönlendirme karar ağacı (kısa).

### Hariç

- Faz 1’de olmayan charm kanal sabitleme (orada kalır).

## Kurallar

- Komut ve charm adları Faz 1 skill’lerle **çelişmez**; şüphede Faz 1 `SKILL.md` kazanır.
- Kurulum “yeniden icat etme”; kullanıcıya önce ilgili `../../skills/cos-*` / `juju-*` / `microk8s-*` dosyasını öner.
- Canonical dışı iddia yoksa “resmi dokümanda doğrula” de.

## Kontrol listesi

- [ ] Soru türü (kurulum / ilişki / ingress / teşhis) doğru Faz 1 skill’e map edildi mi?
- [ ] `cos` modeli kuralı (`../../skills/juju-model-cos/SKILL.md`) hatırlatıldı mı?
- [ ] Ubuntu Observability linki güncel mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Belirsiz semptom | Hangi UI (Grafana vs ingress) | İlgili troubleshoot skill |
| Faz 1 eksik adım | IMPLEMENTATION_PLAN | Skill sırasını takip et |

## İlgili belgeler ve skill'ler

- `../../documantations/PROJECT_ROOT.md`
- `../../documantations/ARCHITECTURE_COS.md`
- `../../documantations/IMPLEMENTATION_PLAN.md`
- `../../skills/juju-model-cos/SKILL.md`
- `../agentic-microk8s-ops-reference/SKILL.md`
- `../agentic-juju-ops-reference/SKILL.md`
- `../agentic-cos-no-data-playbook/SKILL.md`
- `https://documentation.ubuntu.com/observability/`
