---
name: k8s-sec-seccomp-apparmor
description: Pod’larda sistem çağrısı ve process davranışını Seccomp/AppArmor ile kısıtlamak veya “hangi profil bu workload’u kırıyor?” sorusunu çözmek gerektiğinde kullan. Amaç: **runtime ayrıcalığını daraltmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Seccomp ve AppArmor kullanım ayrımı
- Profil seçimi/uyarlaması
- Doğrulama: workload çalışıyor ve gereksiz syscall/path erişimi engelleniyor mu?

## Workflow
- Kontrol seviyesini seç:
  - Seccomp syscall düzeyi, AppArmor path/capability davranışı.
- Başlangıç profili:
  - Runtime default yeterli mi, custom profil mi gerekli?
- Test:
  - Uygulama hangi syscall/path’lere gerçekten ihtiyaç duyuyor?
- Rollout:
  - Önce gözlem, sonra sıkılaştırma.
- Doğrulama:
  - Profil aktif mi ve uygulama normal çalışıyor mu?

## Common mistakes
- Profili copy-paste edip workload ihtiyaçlarını doğrulamamak.
- Seccomp ve AppArmor’ın aynı şeyi yaptığını sanmak.

## References
- `skills/k8s-sec-pod-security-standards`
- `skills/k8s-sec-read-only-filesystem`
