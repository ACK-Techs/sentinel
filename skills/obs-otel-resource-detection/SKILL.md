---
name: obs-otel-resource-detection
description: OpenTelemetry resource detection ile `service.name`, `k8s.*`, `container.*`, `host.*`, `cloud.*` gibi resource attribute’larını otomatik ve tutarlı üretmek; “service.name boş/yanlış”, “k8s namespace yok” gibi sorunları Collector/SDK düzeyinde çözmek gerektiğinde kullan.
---

## Purpose
Bu skill’in çıktısı:
- Resource attribute kaynağı kararı (SDK env vs Collector detector) ve öncelik sırası
- K8s/container/process detector seçimi ve güvenli default’lar
- Doğrulama: backend’de resource attribute’ları ile filtreleme yapılabildiğini kanıt

## Workflow
- Kaynakları belirle:
  - Env var mı? (OTEL_RESOURCE_ATTRIBUTES)
  - Collector agent gateway mi? (detection stratejisi değişir)
- Öncelik kuralı:
  - “tek kaynak” seç veya override sırasını açık yaz (env > detector gibi).
- K8s özelinde:
  - Pod/namespace/node attribute’ları gerekli mi? (routing/tenancy için)
  - Yüksek kardinaliteyi resource’a taşımama (pod UID gibi).
- Doğrulama:
  - Tempo/Loki/metrics backend’de `service.name` ve `deployment.environment` ile filtrele.
  - K8s attribute’ları ile “namespace=…” araması çalışıyor mu?

## Common mistakes
- `service.name`’i otomatiğe bırakıp her pod için farklı üretmek: servis parçalanır.
- Detector’ları açıp PII taşıyan env değişkenlerini resource’a sızdırmak.

## References
- `skills/obs-otel-collector-processors`
- `skills/obs-otel-collector-receivers`
