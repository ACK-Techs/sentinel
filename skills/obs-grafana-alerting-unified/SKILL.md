---
name: obs-grafana-alerting-unified
description: Grafana Unified Alerting’de contact point (bildirim kanalı) ve notification policy (routing) kurmak veya “alert gidiyor ama yanlış kişiye gidiyor / hiç gitmiyor” sorununu çözmek gerektiğinde kullan. Alert kural yazmaktan çok **routing ve delivery** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Contact point taslağı (hangi kanal, hangi ortam, hangi maskleme)
- Notification policy ağacı (matchers, grouping, repeat) ve “neden böyle?” notu
- Doğrulama: test notification ve gerçek bir alert’in doğru policy’ye düştüğünü kanıtlama

## Workflow
- Envanter çıkar:
  - Kaç ekip/servis var? (routing key ne olacak: `team`, `service`, `severity`?)
  - Ortam ayrımı var mı? (prod vs staging → ayrı contact point)
- Contact point tasarla:
  - Kanal: Slack/Email/PagerDuty/Webhook vs.
  - Secret’lar: token/webhook URL’lerini repo/mesaj içine yazma; Grafana secret store üzerinden yönet.
- Policy ağacını kur:
  - Root policy: default receiver (genelde düşük öncelik).
  - Alt policy: matcher ile `severity="page"` gibi kritik olanları ayrı kanala.
  - Grouping: `group_by` (örn. `alertname`, `service`) ve `group_wait/interval/repeat` kararlarını yaz.
- “Yanlış yere gidiyor” teşhisi:
  - Alert rule label’ları matcher’larla uyuşuyor mu?
  - Bir policy daha genel olup diğerini gölgeliyor mu? (sıra/öncelik)
- Doğrulama:
  - Contact point test mesajı gönder.
  - Bir örnek alert’i “firing” yaptırıp hangi policy’ye düştüğünü doğrula.

## Common mistakes
- Matcher’ı yanlış label adına yazmak (ör. `team` yokken `team=...`).
- Grouping’i aşırı dar yapmak: aynı incident 100 bildirim olur.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
