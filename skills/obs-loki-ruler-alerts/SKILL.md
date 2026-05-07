---
name: obs-loki-ruler-alerts
description: Loki Ruler ile log tabanlı alert yazmak gerektiğinde kullan. LogQL metric query (rate/count_over_time) ile eşik belirleme, gürültüyü azaltma ve Alertmanager’a yönlendirme (routing için label/annotation) konularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Bir Ruler alert kuralı (adı, LogQL expr, `for`, labels, annotations)
- “Neden bu eşik?” ve “gürültü kontrolü” notu (regex/filter, min volume, grouping)
- Doğrulama adımı: Loki query ile tetikleyici senaryoyu geçmişte kanıtlama

## Workflow
- Semptomu seç:
  - “error log sayısı arttı”, “panic görüldü”, “auth failed spike” gibi net tanım.
- LogQL’i metric query’ye çevir:
  - Stream selector dar: `{app="...", namespace="..."}`
  - İçerik filtresi: `|=`, `|~` (regex’i minimal)
  - Metrik: `sum(rate(<log query> [5m]))` veya `count_over_time(...)`
- Gürültü kontrolü ekle:
  - Low traffic’te oranlar gürültülü: gerekiyorsa min volume koşulu.
  - `for:` ile kısa spike’ları filtrele.
  - Çok fazla label ile alert’i parçalama (pod bazında istemiyorsan aggregate et).
- Alert metadata:
  - `labels.severity` ve sahiplik label’ı (varsa)
  - `annotations.summary` + aksiyon odaklı `description`
- Doğrulama:
  - Son 24h/7d üzerinde query çalıştır; ne sıklıkla tetikler?
  - “False-positive” örnekleri varsa filter/threshold’u revize et.

## References
- `skills/cos-deploy-loki`
- `skills/cos-deploy-alertmanager`
- `skills/obs-loki-query-logql`
