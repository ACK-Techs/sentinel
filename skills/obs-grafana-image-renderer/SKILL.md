---
name: obs-grafana-image-renderer
description: Grafana’da panel/dashboard görüntüsü render etmek (alert notification’da screenshot, rapor çıktısı) için image renderer kurmak veya “render timeout/blank image” sorunlarını çözmek gerektiğinde kullan. Kaynak tüketimi (CPU/RAM) ve izolasyon (renderer ayrı servis) odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Kurulum topolojisi kararı: embedded plugin vs ayrı renderer servisi
- Kaynak ve stabilite checklist’i (timeout, concurrency, memory)
- Doğrulama: örnek panel render isteği ve beklenen çıktı

## Workflow
- İhtiyacı netleştir:
  - Nerede kullanılacak? (alert bildirimleri, scheduled report, API render)
  - Render edilen paneller ağır mı? (çok seri / büyük heatmap)
- Topoloji:
  - Ayrı renderer servisi tercih et (Grafana’yı headless browser yükünden izole).
- Kaynak planı:
  - Concurrency sınırı + render timeout belirle.
  - RAM/CPU limitlerini panel ağırlığına göre ayarla.
- Ağ ve güvenlik:
  - Renderer’ın Grafana’ya erişimi kısıtlı olmalı (internal).
  - Auth/URL parametrelerinde token sızıntısını engelle.
- “Boş/timeout” teşhisi:
  - Panel query çok mu ağır? (time range/step)
  - Renderer kapasitesi yetiyor mu? (concurrency)
  - DNS/TLS/reverse proxy sorunları?
- Doğrulama:
  - Tek bir panel için render isteği at, görsel düzgün mü?

## Common mistakes
- Renderer’ı Grafana ile aynı pod/container’da koşturmak: CPU/RAM pikleri Grafana’yı da düşürür.
- Çok geniş time range ile render: timeout ve boş görsel.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-grafana-plugin-install`
