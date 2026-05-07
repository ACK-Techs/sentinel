---
name: obs-alertmanager-opsgenie
description: Alertmanager’dan OpsGenie’ye alert/incident açmak (API key, responder/team mapping, priority/severity) veya “duplicate açıyor / kapanmıyor / yanlış ekibe gidiyor” sorununu çözmek gerektiğinde kullan. OpsGenie’ye özgü responder ve lifecycle semantiğine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- OpsGenie receiver YAML snippet’i (API key maskeli) + responder mapping kararı
- Dedup/lifecycle stratejisi: firing → create, resolved → close
- Doğrulama: test alert’i ile doğru team’e düşen ve kapanan incident kanıtı

## Workflow
- OpsGenie hedefini netleştir:
  - Hangi team/schedule? hangi integration key?
- Secret hijyen:
  - API key’i config’e düz yazma; secret store/ENV referansı kullan.
- Responder mapping:
  - Alert label’larından (`team`, `service`) OpsGenie responder’a map kuralını yaz.
  - Fall-back responder belirle (label eksikse).
- Priority/severity:
  - `severity=page` → yüksek öncelik; notify kanalı ayrı.
- Dedup ve close:
  - Tekilleştirme anahtarını sabitle (fingerprint/group key).
  - Resolved event’in aynı anahtarla close yapabildiğini doğrula.
- Doğrulama:
  - Test alert’i ile incident oluştur; responder doğru mu?
  - Alert resolved olunca incident kapanıyor mu?

## Common mistakes
- Responder mapping’i label kontratı olmadan yapmak: yanlış ekip/schedule.
- Dedup anahtarını sabitlememek: aynı issue için çok incident.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-receivers`
