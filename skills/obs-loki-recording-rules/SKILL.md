---
name: obs-loki-recording-rules
description: Loki’de LogQL metric query’lerini recording rule olarak kaydedip (ör. error rate, auth fail rate) dashboard/alert’lerde tekrar kullanmak veya Prometheus benzeri metrik tüketimine “bridge” etmek gerektiğinde kullan. “log’dan metrik üret”, “record adı”, “label set’i sabitle” gibi sorular için.
---

## Purpose
Bu skill’in çıktısı:
- Loki recording rule(lar)ı: `record` adı + LogQL metric `expr`
- İsimlendirme ve label set kontratı (cardinality kontrolü)
- Kullanım notu: panel/alert sorgusu “ham LogQL” yerine kaydı nasıl kullanır

## Workflow
- Kaynağı belirle:
  - Ham log query: `{app="..."} |= "error"` gibi
  - Metric query’ye çevir: `rate(...)`, `count_over_time(...)`, `sum by (...) (...)`
- “Metrik kontratı” tasarla:
  - `record` adı: ölçtüğü şeyi anlatan ve stable bir isim (rastgele değil).
  - Label set: dashboard/alert’in ihtiyacından fazlasını bırakma (pod bazında istemiyorsan aggregate et).
- Gürültü kontrolü:
  - Regex/parse maliyetini minimize et; mümkünse ingestion tarafında normalize et.
  - Low traffic’te oranlar gürültülü olabilir; pencereyi ve threshold’u not et.
- Doğrulama:
  - Kaydın üretildiğini doğrula: record adıyla sorgu dönüyor mu?
  - Ham sorgu ile kaydın trendi “yaklaşık” uyumlu mu?

## Common mistakes
- Recording’de label patlaması: log akışı yüksekse hızlıca maliyete dönüşür.
- Record adını belirsiz koymak: dashboard/alert’ler zamanla okunamaz hale gelir.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-query-logql`
- `skills/obs-loki-ruler-alerts`
