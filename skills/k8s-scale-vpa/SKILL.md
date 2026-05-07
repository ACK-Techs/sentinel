---
name: k8s-scale-vpa
description: "Vertical Pod Autoscaler ile resource request/limit önerisi üretmek veya “pod sürekli OOM / fazla overprovision” sorunlarını düzeltmek gerektiğinde kullan. Amaç: **dikey kaynak ayarını gözlem verisine dayandırmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- VPA kullanım modu kararı (off/recommendation/auto)
- Request tuning yaklaşımı
- Doğrulama: öneri kalitesi ve rollout etkisi

## Workflow
- Hedefi belirle:
  - Otomatik uygulama mı, sadece öneri mi?
- Uyum:
  - HPA ile birlikte mi çalışacak? hangi metrik üzerinden?
- Yeniden başlatma etkisi:
  - VPA update pod restart gerektirir mi?
- Öneriyi oku:
  - CPU/memory lower/target/upper aralıkları makul mi?
- Doğrulama:
  - OOM ve throttling azalıyor mu, maliyet dengesi iyileşiyor mu?

## Common mistakes
- Stateful/latency kritik iş yüklerinde restart etkisini hesaba katmamak.
- HPA + VPA’yı aynı resource üzerinde düşüncesizce birleştirmek.

## References
- `skills/k8s-scale-hpa`
- `skills/k8s-core-resource-requests-limits`
