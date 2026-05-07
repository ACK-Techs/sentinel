---
name: k8s-core-init-containers
description: Uygulama başlamadan önce hazırlık işi çalıştırmak (migration, config render, dependency wait, volume prepare) veya “main container çok erken başlıyor” problemini çözmek gerektiğinde kullan. Amaç: **başlangıç önkoşullarını deterministik hale getirmek**.
---

## Purpose
Bu skill’in çıktısı:
- Init container gereksinimi ve sınırı (ne init’te kalmalı, ne ana container’da)
- Başlangıç sırası ve başarısızlık davranışı
- Doğrulama: init log’u + Pod phase/event üzerinden kanıt

## Workflow
- Hazırlık işini sınıflandır:
  - Tek seferlik mi? idempotent mi? uzun sürerse startup’ı kabul edilebilir mi?
- Init container’a taşı:
  - Volume hazırlama, config dosyası üretme, bağımlı endpoint bekleme, hafif migration kontrolleri.
  - Uygulamanın asıl işi veya sonsuz bekleme döngüsü init’e konmamalı.
- Veri paylaşımı:
  - Sonuç nereye yazılacak? `emptyDir`, projected volume, PVC?
- Başarısızlık modeli:
  - Retry ile düzelebilir hata mı, yoksa Pod sürekli CrashLoop’a mı girecek?
  - Timeout ve bekleme stratejisi belirle.
- Doğrulama:
  - `kubectl logs <pod> -c <init-name>`
  - Pod `Initialized=True` olduktan sonra main container ayağa kalkıyor mu?

## Common mistakes
- DB migration’ı uzun ve riskli halde init’e koymak: rollout tamamen kilitlenebilir.
- “sleep 30” ile bağımlılık beklemek: sahte stabilite yaratır.

## References
- `skills/k8s-core-pod-lifecycle`
- `skills/k8s-core-configmap-secret`
