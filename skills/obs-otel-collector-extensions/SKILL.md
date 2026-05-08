---
name: obs-otel-collector-extensions
description: OpenTelemetry Collector’a `health_check`, `pprof`, `zpages` gibi extension’ları eklemek; “collector canlı mı?”, “CPU/RAM niye patladı?”, “pipeline nerede tıkanıyor?” sorularına teşhis yüzeyi kazandırmak gerektiğinde kullan. Pipeline içeriklerinden çok **operability endpoint’leri** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Extension seçimi ve minimal YAML parçaları (hangi port/endpoint, hangi ortamda açılmalı)
- Prod güvenlik notu: debug endpoint’leri **internal-only** tutma önerisi
- Doğrulama: health endpoint + (opsiyonel) pprof/zpages erişimiyle “çalışıyor” kanıtı

## Workflow
- İhtiyacı sınıflandır:
  - Liveness/readiness için basit sağlık kontrolü mü?
  - Performans teşhisi için pprof mu?
  - Pipeline gözlemi için zpages mi?
- Extension’ları ekle:
  - `health_check`: k8s probe/monitoring için.
  - `pprof`: kısa süreli profilleme ve memory leak teşhisi için.
  - `zpages`: trace/metrics pipeline akışını interaktif görmek için.
- Ağ/güvenlik:
  - Bu endpoint’leri public yapma; cluster internal / localhost / allowlist kullan.
  - TLS/ingress gerekiyorsa “debug endpoint’leri” ayrı path ve ayrı auth ile yönet.
- Operasyonel kullanım:
  - Incident sırasında pprof/zpages aç-kapat planı (kalıcı açık bırakma).
- Doğrulama:
  - `health_check` endpoint 200 dönüyor mu?
  - pprof/zpages erişimi yalnız internal’dan mümkün mü?

## Common mistakes
- pprof/zpages’ı internete açmak: ciddi bilgi sızıntısı ve saldırı yüzeyi.
- Extension ekleyip `service.extensions` listesine bağlamayı unutmak: config var ama etkisiz.

## References
- `skills/obs-otel-collector-pipeline`
