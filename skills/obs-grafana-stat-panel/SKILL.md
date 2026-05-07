---
name: obs-grafana-stat-panel
description: Grafana Stat/Gauge paneliyle tek bir KPI’ı doğru göstermek (reduce fonksiyonu, null handling, unit, threshold renkleri) gerektiğinde kullan. “Stat yanlış değer gösteriyor”, “renkler ters”, “son değer mi ortalama mı?” gibi panel-konfig odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Stat/Gauge panel konfigürasyon checklist’i (value reduction, unit, decimals, mapping)
- Threshold stratejisi (iyi/kötü yön, ters metriklerde renk mantığı)
- Doğrulama: aynı metriğin time series paneli ile tutarlılık kontrolü

## Workflow
- KPI tipini belirle:
  - Anlık (gauge): CPU %, queue depth.
  - Oran/percent: error rate, availability.
  - Kümülatif sayaç: stat için önce rate/irate gerekir.
- Reduce kararını yaz:
  - “Last” mı “Mean/Min/Max” mı? (incident ekranı genelde last)
  - Zaman aralığı ile uyumlu mu?
- Null/No data:
  - No data durumunda panel ne yazmalı? (N/A) ve renk vermemeli.
- Unit/format:
  - ms/s/%/bytes doğru; decimals aşırı olmasın.
  - Value mapping gerekiyorsa (“0=OK, 1=FAIL”) ekle.
- Threshold:
  - Kötü yönü belirle (yüksek kötü mü düşük kötü mü).
  - Renk mantığını ters metriklerde düzelt (örn. availability düşükse kırmızı).
- Doğrulama:
  - Aynı metriği time series olarak yanına koy; stat değeri o grafikteki seçilen reduce ile aynı olmalı.

## Common mistakes
- Counter metriği doğrudan stat’te göstermek (rate olmadan).
- “Last” ile “Mean” karışıklığı: ekip farklı yorumlar.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-dashboard-design`
