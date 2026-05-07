---
name: obs-prometheus-anomaly-detection
description: Prometheus verisiyle “beklenmeyen sapma” tespiti yapmak gerektiğinde kullan. Özellikle z‑score (mean/stddev) veya “şimdi vs geçmiş baseline” ratio yaklaşımıyla anomali alarmı yazmak, false-positive’i azaltmak ve düşük trafik/gürültü durumlarını ele almak için.
---

## Purpose
Bu skill’in çıktısı:
- Seçilen anomali yöntemine uygun PromQL şablonu (z‑score veya ratio-to-baseline)
- “Ne zaman anlamlı?” koşulları (min trafik / min örnek sayısı / pencere)
- Alarm eşiği ve stabilizasyon notu (for/window, clamp, outlier etkisi)

## Workflow
- Önce “anomali”yi tanımla (metrik adı değil, davranış):
  - Spike mı (ani artış), drop mu (ani düşüş), drift mi (yavaş kayma)?
  - Hangi sinyal: error rate, latency, saturation, traffic?
- Yöntemi seç:
  - **Ratio-to-baseline**: şimdi ile geçmişin aynı dilimini kıyasla (günlük/haftalık pattern varsa).
  - **Z‑score**: kısa pencerede ortalamadan kaç std sapma? (noise düşükse iyi çalışır).
- Trafik/gürültü guardrail’i ekle:
  - Low traffic’te oranlar patlar: `requests_total` gibi bir “min volume” koşulu ekle.
  - `clamp_min` ile bölme/0 hatalarını önle.
- PromQL şablonları (kısa, uyarlanabilir):
  - Ratio: `(now / baseline)` gibi bir oran üret ve eşik belirle (örn. >1.5 veya <0.5).
  - Z‑score: `(x - avg_over_time(x[W])) / stddev_over_time(x[W])`
  - Baseline için `offset` kullan (örn. 1w) ve pencereyi stabil seç.
- Alarm tasarımı:
  - “Anomali” genelde semptomdur; severity’yi düşük başlat (`ticket`) ve gözlemle.
  - `for:` ile kısa spike’ları filtrele.
- Doğrulama:
  - Grafikte şimdi + baseline + skor/ratio’yu aynı panelde göster.
  - Son 7/14 gün üzerinde geçmişte sürekli tetikleniyor mu? (threshold’u revize et)

## Common mistakes
- Volume koşulu olmadan ratio alarmı: 0→1 geçişlerinde “sonsuz” görünür.
- Sezonlukluk varken z‑score kullanmak: düzenli günlük/haftalık pattern false-positive üretir.

## References
- `skills/obs-prometheus-alerting-rules`
- `skills/obs-prometheus-recording-rules`
