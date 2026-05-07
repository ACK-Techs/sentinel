---
name: k8s-scale-keda
description: "Event-driven autoscaling kurmak, kuyruk uzunluğu/Prometheus metric/Kafka lag gibi sinyallere göre pod sayısı ayarlamak gerektiğinde kullan. Amaç: **HPA’nın ötesindeki olay tabanlı yükü doğru sinyalle ölçeklemektir**."
---

## Purpose
Bu skill’in çıktısı:
- ScaledObject/scaler seçimi
- Event sinyali ile replica davranışı eşleştirmesi
- Doğrulama: gerçek event altında scale-out/scale-in kanıtı

## Workflow
- Olay kaynağını netleştir:
  - Queue, Kafka, Redis, Prometheus metric?
- Sinyali yorumla:
  - Kuyruk derinliği mi, tüketim lag’i mi, request rate mi?
- Davranış:
  - Scale-to-zero uygun mu?
  - Poll interval/cooldown nasıl olmalı?
- HPA ilişkisi:
  - KEDA hangi HPA’yı üretiyor, çakışma var mı?
- Doğrulama:
  - Olay artınca replica yükseliyor, olay bitince kontrollü düşüyor mu?

## Common mistakes
- Gecikmeli metrikle agresif autoscaling yapmak.
- Kuyruk sinyalini işlem süresiyle birlikte değerlendirmemek.

## References
- `skills/k8s-scale-hpa`
- `skills/target-app-load-generator`
