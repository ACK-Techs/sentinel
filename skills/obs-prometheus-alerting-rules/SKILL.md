---
name: obs-prometheus-alerting-rules
description: Prometheus’ta yeni bir alerting rule yazmak veya mevcut alert’te false-positive / kaçırma (false-negative) sorununu düzeltmek gerektiğinde kullan. “alert rule”, “expr”, “for”, “severity”, “runbook_url”, “flapping” veya “eşik (threshold) nasıl seçilir?” gibi sorularda dar kapsamlı yol gösterir.
---

## Purpose
Bu skill’in çıktısı, doğrudan kullanılabilir bir **alerting rule** (YAML) ve kısa bir **tasarım gerekçesi**dir:
- Kural yapısı: `alert`, `expr`, `for`, `labels`, `annotations`
- Operasyonel kontrat: hangi semptomu yakalar, ne zaman “firing” olur, ne zaman “resolved” olur
- Runbook bağlantısı ve sahiplik (owner/team) label’ları (varsa)

## Workflow
- Semptomu tanımla (kuralı metrikten değil, semptomdan başlat):
  - “Ne kötü?”: latency mi, error rate mi, saturation mı, down mı?
  - Kapsam: hangi service/job/namespace? (label filtresi)
- İyi bir `expr` yaz:
  - Ham metrik yerine oran/percentile kullan (örn. `rate()`/`histogram_quantile()` gibi) ve pencereyi açık yaz.
  - Label kardinalitesini kontrol et: alert 10k seriye bölünmesin (örn. `pod` bazında istemiyorsan `sum by (...)`).
  - Eşik mantığını not et: mutlak eşik mi, baseline’a göre oran mı, SLO türevi mi?
- Flapping’i azalt:
  - `for:` süresi ile “geçici spike” vs “kalıcı sorun” ayrımı yap.
  - Gerekirse `clamp_min`, `min_over_time/max_over_time` gibi stabilizasyon araçlarını düşün; ama okunabilirlikten ödün verme.
- Routing için gerekli metadata’yı ekle:
  - `labels.severity` (örn. `page|ticket|info`) ve ekip/sahiplik label’ı (varsa).
  - `annotations.summary` (1 satır), `annotations.description` (kısa, aksiyon odaklı), `annotations.runbook_url` (varsa).
- Deploy formatını seç:
  - Bare Prometheus: rule dosyası + `rule_files` referansı
  - COS/Juju: Prometheus’un rule mekanizmasına uyacak şekilde (bu repoda kuralın içeriğini üret, yerleştirme kullanıcı akışına kalabilir)
- Validasyon (self-check):
  - PromQL’i önce grafikte çalıştır: beklenen label seti ve değer aralığı doğru mu?
  - “Eşik üstünde” senaryosunu simüle et (geçmiş veriyle) ve `for` etkisini düşün.
  - Mümkünse `promtool check rules` / unit test (ayrı skill) ile syntax + mantık testi öner.

## Common mistakes
- “Neden” yerine “semptom” alert’i: CPU yüksek diye page atmak yerine kullanıcı etkisini yakalayan sinyali öncele.
- `for` yok: kısa spike’lar paging’e dönüşür.
- Annotation yok: alert geldiğinde ne yapılacağı belirsiz kalır.

## References
- `skills/cos-deploy-prometheus`
- `skills/cos-deploy-alertmanager`
- `skills/obs-prometheus-unit-testing`
