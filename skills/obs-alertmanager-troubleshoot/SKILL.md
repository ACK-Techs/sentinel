---
name: obs-alertmanager-troubleshoot
description: Alertmanager’da “alert var ama bildirim yok”, “yanlış receiver’a gidiyor” veya “duplicate bildirim gidiyor” problemlerini semptom→teşhis→doğrulama akışıyla çözmek gerektiğinde kullan. Hedef: sorunu rule/ingest/routing/receiver/HA katmanında doğru yere indirgemek.
---

## Purpose
Bu skill’in çıktısı:
- Kısa teşhis ağacı: (Prometheus rule) → (Alertmanager ingest) → (routing) → (receiver delivery) → (HA/dedup)
- Her adım için kanıt önerisi (UI/API/log) ve bir sonraki net aksiyon

## Workflow
- Semptomu sınıflandır:
  - A) Alert Prometheus’ta hiç firing olmuyor
  - B) Alert firing ama Alertmanager’da görünmüyor
  - C) Alert görünüyor ama bildirim yok/yanlış
  - D) Duplicate bildirim var
- A) Rule katmanı:
  - Alert state ve `for` koşulu; beklenen label’lar set ediliyor mu?
- B) Ingest katmanı:
  - Prometheus → Alertmanager hedefi doğru mu? (network/TLS/auth)
  - Alertmanager API’de aktif alerts listesi var mı?
- C) Routing/receiver:
  - Route matcher’lar uyuşuyor mu? (özellikle `team/service/severity/env`)
  - `continue` ve route sırası beklenen mi?
  - Receiver hata modları: 401/403, timeout, 429.
- D) HA/dedup:
  - Alertmanager cluster tek parça mı? split brain var mı?
  - Aynı alert iki AM instance tarafından mı gönderiliyor?
- Doğrulama:
  - Tek bir test alert’i ile uçtan uca: firing → doğru receiver → resolved kapanış.

## References
- `skills/obs-alertmanager-routing`
- `skills/obs-alertmanager-receivers`
- `skills/obs-alertmanager-high-availability`
- `skills/cos-deploy-alertmanager`
- `cli/skills/agentic-troubleshoot-alertmanager`
