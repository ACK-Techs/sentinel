---
name: obs-grafana-prometheus-explore
description: Grafana Explore’da Prometheus datasource ile PromQL denemek, metric browser ile doğru metriği bulmak veya “grafikte veri yok/çok gürültü var” sorununu hızlı teşhis etmek gerektiğinde kullan. Explore kullanım akışı ve doğru step/interval seçimine odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Explore’da hızlı PromQL iterasyonu için akış (metric bul → filtre → aggregate → doğrula)
- Step/interval kararları (çok ince step → büyük payload, çok kalın → detay kaybı)
- “No data” teşhis adımları (label filtresi, zaman aralığı, scrape/up)

## Workflow
- Explore başlangıcı:
  - Prometheus datasource seç.
  - Zaman aralığını incident penceresine çek.
- Metric’i bul:
  - Metric browser/auto-complete ile adayı seç.
  - Önce “ham” değeri gör (tek seri).
- Filtre ve aggregate:
  - Label filtresi ekle (`job`, `service`, `namespace`).
  - İstenmeyen kardinaliteyi topla: `sum by (...)` / `avg by (...)`.
- Step/interval:
  - Aralığa göre step’i makul seç; panel “data points” patlamasın.
- “No data” teşhisi:
  - `up{job="..."} ` ile scrape var mı?
  - Label filtresi yanlış mı?
  - Aralık retention dışında mı?
- Doğrulama:
  - Aynı metriğin “count” ve “rate” varyantlarını karşılaştır (anlamlı mı?).

## References
- `skills/cos-deploy-grafana`
- `skills/obs-prometheus-instant-query`
