---
name: obs-grafana-tempo-explore
description: Grafana Explore’da Tempo ile trace aramak (TraceQL), bir trace’i açıp span’ları incelemek veya “Grafana’da trace bulunmuyor” sorununu hızlı teşhis etmek gerektiğinde kullan. Explore kullanım akışına odaklanır (kurulum değil).
---

## Purpose
Bu skill’in çıktısı:
- Explore’da trace bulmak için daraltma stratejisi (service + kısa aralık + attribute)
- Trace inceleme checklist’i (root span, error span, en yavaş span, critical path)
- Boş sonuç/timeout için hızlı teşhis (service.name, sampling, tenant, aralık)

## Workflow
- Explore başlangıcı:
  - Tempo datasource seç.
  - Zaman aralığını incident penceresine çek (son 30–60 dk).
- Sorgu yaz:
  - Önce `service.name` ile daralt.
  - Sonra attribute filtreleri ekle (status, route, duration).
  - Regex’i en sona bırak.
- Trace aç ve analiz et:
  - Root span: request kapsamı.
  - Error span: status=ERROR ve hata mesajı.
  - En yavaş span: latency kaynağı.
  - Span attribute’ları: route, db statement gibi alanlar (sızıntı riskine dikkat).
- Boş sonuç/timeout:
  - Aralığı daralt.
  - Sampling oranını kontrol et.
  - Multi-tenancy varsa tenant header doğru mu kontrol et.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-tempo-trace-query`
- `skills/obs-tempo-troubleshoot-query`
