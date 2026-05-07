---
name: obs-loki-promtail-config
description: Promtail ile log toplamak için scrape config yazmak, pipeline stages ile parse/normalize yapmak veya multiline (stacktrace) logları doğru birleştirmek gerektiğinde kullan. “promtail config örneği”, “pipeline stages”, “multiline stacktrace” gibi sorularda.
---

## Purpose
Bu skill’in çıktısı:
- Hedef kaynak için promtail `scrape_configs` (file/k8s) iskeleti
- Pipeline stages planı: label ekleme/çıkarma, parse (json/logfmt), normalize
- Multiline birleşimi için kural (başlangıç regex’i + max lines/timeout düşüncesi)

## Workflow
- Kaynağı seç:
  - Dosya log’u mu? k8s pod log’u mu? (scrape config farklı)
- Label set’ini minimal tasarla:
  - Routing label’ları (`namespace`, `app`, `cluster`, `level`) küçük tut.
  - Pod adı / container id gibi churn label’larını varsayılan ekleme.
- Pipeline stages:
  - Parse gerekiyorsa: `json` / `logfmt` stage.
  - Normalize: `level` map’leme, status class, route grouping (dinamik path’i sınıfa indir).
  - “Label promotion” kararını ver: field’ı label’a taşıma = index maliyeti.
- Multiline (stacktrace):
  - Başlangıç satırı regex’i belirle (örn. timestamp ile başlayan satır).
  - “En kötü durum”u düşün: çok uzun trace → max lines/timeout.
- Doğrulama:
  - Canary log üret; Loki’de tek satır mı birleşti mi kontrol et.
  - Label selector ile hızlı sorgu: `{app="..."} |= "canary"`

## Common mistakes
- Multiline kuralını çok geniş yazmak: farklı logları yanlış birleştirir.
- Her field’ı label’a taşımak: Loki index’i şişer.

## References
- `skills/cos-deploy-loki`
- `skills/obs-loki-label-strategy`
