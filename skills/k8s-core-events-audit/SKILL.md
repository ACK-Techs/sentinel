---
name: k8s-core-events-audit
description: Kubernetes event’leri ve audit log’larını kullanarak “ne oldu?” sorusunu cevaplamak, operasyon geçmişi çıkarmak veya cluster davranışını sonradan kanıtlamak gerektiğinde kullan. Amaç: **geçici event ile kalıcı audit izini ayırmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Hangi olay event’ten, hangisi audit log’dan aranmalı ayrımı
- Event/audit toplama ve filtreleme yaklaşımı
- Doğrulama: zaman çizelgesi halinde kök olay sırası

## Workflow
- Soruyu sınıflandır:
  - Scheduler/Pod lifecycle sorunu mu? önce event.
  - “Kim sildi/değiştirdi?” sorusu mu? audit log.
- Event kullanımı:
  - Pod, node, namespace, controller bazında yakın zamanlı event topla.
  - Warning event’leri öne al.
- Audit kullanımı:
  - API server audit policy varsa request user, verb, objectRef üzerinden izle.
  - CI/CD service account’ları ile insan kullanıcılarını ayır.
- Zaman korelasyonu:
  - Event timestamp ile audit request zamanını eşleştir.
- Doğrulama:
  - Kök olay → yan etki → iyileşme akışını çıkar.

## Common mistakes
- Event’leri uzun süreli tarihçe sanmak: retention düşüktür.
- Audit log açmadan “kim yaptı?”yı event’lerden beklemek.

## References
- `skills/k8s-sec-audit-logging`
- `skills/debug-log-correlation`
