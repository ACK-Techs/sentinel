---
name: obs-grafana-logs-panel
description: Grafana dashboard’unda Logs paneli tasarlamak (Loki query, label filtreleri, satır formatı, max lines) veya “panel çok gürültülü/çok pahalı” problemini çözmek gerektiğinde kullan. Dashboard içine gömülü log görünümüne odaklanır (Explore değil).
---

## Purpose
Bu skill’in çıktısı:
- Logs panel için “dar ve hızlı” LogQL taslağı (selector + filtre + parse)
- Panel UX ayarları (max lines, wrap, time format) ve maliyet kontrolü
- Drilldown: satırdan Explore’a veya trace’e gidiş linkleri

## Workflow
- Panelin amacını seç:
  - Incident dashboard: sadece hata/uyarı logları ve kısa zaman aralığı.
  - Servis dashboard: “son hatalar” + “slow request” gibi 1–2 odak.
- LogQL tasarla:
  - Label selector ile daralt (`service`, `namespace`, `app`).
  - İçerik filtresi ekle (`|= "error"`).
  - Yapısal log varsa parse et (`| json` / `| logfmt`) ve alan filtresi uygula.
- Panel ayarları:
  - Max lines’i sınırlı tut (dashboard’da 50–200 arası).
  - Line wrap ve highlight ile okunabilirlik.
  - Zaman aralığını değişkenle kontrol et (örn. “last 15m”).
- Drilldown:
  - “View in Explore” linki: aynı selector + aynı time range.
  - Trace id varsa derived field ile Tempo linki.
- Doğrulama:
  - Panel render süresi ve sonuç sayısı makul mü?

## Common mistakes
- Selector olmadan regex aramak: panel yavaşlar ve pahalılaşır.
- Dashboard’a “live tail” benzeri davranış yüklemek: UX ve maliyet bozulur.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-loki-query-logql`
- `skills/obs-grafana-loki-explore`
