---
name: obs-grafana-annotations
description: Grafana dashboard’larda olayları (deploy, incident, config change) zaman çizgisine annotation olarak koymak veya otomatik event-driven annotation akışı kurmak gerektiğinde kullan. “Deploy çizgisi ekle”, “annotation API”, “neden timeline boş” gibi konulara odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Annotation stratejisi: hangi event’ler annotation olmalı, hangi tag’lerle sınıflanmalı
- Otomasyon planı: event kaynağı → Grafana annotation (API veya datasource)
- Doğrulama: dashboard’da ilgili zaman penceresinde annotation görünür mü?

## Workflow
- Annotation kapsamını seç:
  - Deploy (version/commit), incident start/end, feature flag change, config rollout.
- Tag tasarımı:
  - `service`, `env`, `team`, `type=deploy|incident` gibi 2–4 tag ile filtrelenebilir yap.
- Üretim yolu:
  - Manuel: incident sırasında hızlı not.
  - Otomatik: CI/CD veya release pipeline’dan annotation gönder (event-driven).
- Veri kalitesi:
  - Zaman damgası doğru mu? (UTC vs local)
  - Metin kısa ve aksiyon odaklı mı? (link varsa runbook/PR)
- Doğrulama:
  - Dashboard’da doğru time range seçildiğinde annotation çizgisi görünmeli.

## Anti-patterns
- Her küçük event’i annotation yapmak: timeline gürültü olur, incident’ta işe yaramaz.
- Tagsiz annotation: filtrelenemez, arama zorlaşır.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
