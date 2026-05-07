---
name: obs-prometheus-query-range
description: Prometheus HTTP API `GET /api/v1/query_range` çağrısı tasarlamak, doğru `start/end/step` seçmek veya “neden timeout/çok büyük sonuç dönüyor?” sorunlarını çözmek gerektiğinde kullan. PromQL yazımı değil; **query_range API parametreleri ve sonuç şekli** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- `query_range` için doğru parametre seti (zaman aralığı + step) ve örnek `curl/http` isteği
- Dönen JSON’da `matrix` sonuç tipini okuma (series + [ts,value] çiftleri)
- Sık hata modları için çözüm: 400/422, timeout, “çok seri” (cardinality)

## Workflow
- Girdileri sabitle:
  - PromQL: tek satır `query=...`
  - Zaman: `start`, `end` (RFC3339 veya unix seconds) ve **timezone** netliği
  - Örnekleme: `step` (kaç saniyede bir nokta istiyorsun?)
- `step` seçimi (grafik + maliyet dengesi):
  - Panel 6h/24h/7d gibi aralıklarda “piksel yoğunluğu” hedefle (çok küçük step → büyük payload).
  - Kural: `((end-start)/step)` nokta sayısı makul olmalı; binlerce seri varsa step’i büyüt.
- Sonuç tipini doğru bekle:
  - `query_range` genelde `resultType=matrix` döner.
  - Her seri: `metric` (label map) + `values` (timestamp,value dizisi).
- Hata modlarına göre teşhis:
  - **Timeout**: step’i büyüt, filtreyi daralt (`{job="..."}`), recording rule kullan.
  - **Çok seri**: label patlaması var; önce `count(...) by (...)` ile cardinality’i ölç.
  - **Boş sonuç**: zaman aralığı yanlış, label filtresi yanlış, scrape yok (up kontrolü).
- Çıktı üret:
  - İstek örneği (URL encode + parametreler)
  - “Beklenen” `resultType` ve bir seri örnek şeması (tam veri dump etme)

## References
- `skills/obs-prometheus-instant-query`
- `skills/obs-prometheus-recording-rules`
