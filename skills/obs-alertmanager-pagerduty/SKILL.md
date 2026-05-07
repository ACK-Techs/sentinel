---
name: obs-alertmanager-pagerduty
description: Alertmanager’dan PagerDuty’ye page göndermek (integration key, dedup, severity mapping, incident lifecycle) veya “duplicate incident açılıyor / resolve olmuyor” sorununu çözmek gerektiğinde kullan. PagerDuty’ye özgü dedup ve event semantiğine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- PagerDuty receiver YAML snippet’i (integration key maskeli) + event field mapping önerisi
- Dedup stratejisi: hangi alan incident’i tekilleştirir? (fingerprint/group key)
- Doğrulama: firing → trigger, resolved → resolve akışının PagerDuty’de doğru görünmesi

## Workflow
- PagerDuty nesnelerini netleştir:
  - Hangi service/integration key kullanılacak? (prod ayrı, staging ayrı)
- Secret hijyen:
  - Integration key’i config’e düz yazma; secret store/ENV referansı kullan.
- Dedup ve lifecycle:
  - Aynı incident’in tekrar trigger olmaması için dedup anahtarı seç.
  - Resolve için: Alert’in “resolved” event’i aynı dedup anahtarını üretmeli.
- Severity mapping:
  - Alert label’ı (`severity`) → PD severity/urgency mapping kuralını yaz.
  - Notify kanalı ile page kanalını ayır (her alert PD’ye gitmesin).
- Rate limit ve hata modu:
  - 429/backoff; transient hatalarda retry davranışı.
- Doğrulama:
  - Test alert’i ile bir incident aç.
  - Aynı alert tekrarlandığında duplicate incident açılmıyor mu kontrol et.
  - Alert resolve olduğunda PD incident kapanıyor mu?

## Common mistakes
- Dedup anahtarını sabitlememek: aynı issue için çok sayıda PD incident açılır.
- Resolved event’i mapping/dedup farkı yüzünden kapanmıyor: incident açık kalır.

## References
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
- `skills/obs-alertmanager-receivers`
