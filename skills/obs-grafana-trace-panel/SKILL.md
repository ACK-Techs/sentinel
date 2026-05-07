---
name: obs-grafana-trace-panel
description: Grafana dashboard’unda Trace paneli kurgulamak (Tempo datasource, traceId değişkeni, span detayları, drilldown) gerektiğinde kullan. “Latency panelinden trace’e geç”, “traceId ile panel”, “span detayını göster” gibi trace‑odaklı dashboard deneyimine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Trace panel yerleşimi: metrik panel → exemplar/traceId → trace panel drilldown akışı
- Dashboard variable tasarımı: `trace_id`, `service`, `env` (minimum)
- Doğrulama: bir incident örneğinde panelden doğru trace açılabiliyor mu?

## Workflow
- Giriş yolu seç:
  - Exemplar üzerinden “tıkla → trace aç” (tercih).
  - Log satırındaki trace id’den “tıkla → trace aç”.
  - Manuel: dashboard variable `trace_id`.
- Dashboard variable:
  - `trace_id` için textbox değişkeni (boşsa panel gizle/placeholder).
  - Bağlam değişkenleri: `service`, `env` (panel sorgularında ortak).
- Panel davranışı:
  - `trace_id` doluysa tek trace’i göster.
  - `trace_id` yoksa kullanıcıya “nasıl bulunur” yönlendirmesi (exemplar/log link).
- Span detayları:
  - Kritik attribute’lar: route, status, db, peer.service (gürültüyü azalt).
  - PII/secrets olabilecek attribute’ları göstermemeye dikkat et.
- Doğrulama:
  - Metrik panelde yüksek latency anında exemplar tıklayınca aynı aralıkta trace açılıyor mu?

## Common mistakes
- Trace paneli “arama paneli” gibi kullanmak: dashboard’da pahalı ve UX kötü; Explore’a yönlendir.
- Her span attribute’unu göstermek: PII riski ve okunabilirlik kaybı.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-tempo-exemplars-grafana`
- `skills/obs-grafana-tempo-explore`
