---
name: k8s-core-configmap-secret
description: ConfigMap/Secret ile konfig ve credential yönetmek (env inject vs volume mount, reload stratejisi) veya “config değişti ama pod görmüyor / secret sızdı” sorunlarını çözmek gerektiğinde kullan. Odak: **konfig dağıtımı + güvenli secret yönetimi**.
---

## Purpose
Bu skill’in çıktısı:
- “Ne ConfigMap, ne Secret?” karar rehberi + dağıtım yöntemi (env vs mount)
- Reload/rollout stratejisi (checksum annotation, sidecar reload vs restart)
- Doğrulama: config güncellemesi sonrası pod’da yeni değerlerin aktif olduğuna dair kanıt

## Workflow
- İçeriği sınıflandır:
  - Public config → ConfigMap.
  - Secret (token/password/key) → Secret (ve mümkünse dış secret manager).
- Enjeksiyon yöntemi:
  - Env: basit ama runtime update için restart gerekir.
  - Volume mount: dosya tabanlı config; bazı uygulamalar reload edebilir.
- Değişiklik yayma:
  - “otomatik rollout” isteniyorsa checksum annotation ile Deployment yeniden başlat.
  - Uygulama hot-reload destekliyorsa sinyal/sidecar stratejisini yaz.
- Güvenlik:
  - Secret’ları log’lama; RBAC ile okuma yetkisini daralt.
  - Secret’ı yanlışlıkla ConfigMap’e koyma.
- Doğrulama:
  - Pod içine bak: env veya mount dosyası güncellendi mi?
  - Uygulama gerçekten yeni config ile çalışıyor mu? (health/version endpoint)

## Common mistakes
- Secret’ı env olarak verip “update olur” sanmak: restart olmadan değişmez.
- ConfigMap’e büyük binary/sertifika koymak: yönetim ve güvenlik zorlaşır.

## References
- `skills/k8s-sec-secrets-management`
