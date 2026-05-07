---
name: k8s-sec-pod-security-standards
description: "Kubernetes Pod Security Standards seviyelerini uygulamak, namespace admission etiketlerini ayarlamak veya “pod neden admission’da reddedildi?” sorusunu çözmek gerektiğinde kullan. Amaç: **baseline/restricted kurallarını pratik workload etkisiyle birlikte yönetmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Namespace için uygun PSS seviyesi
- Bloke olan alanların kısa teşhis listesi
- Doğrulama: admission davranışı ve workload uyumu

## Workflow
- Güvenlik seviyesini seç:
  - Privileged, baseline, restricted arasından ortam ihtiyacına göre karar ver.
- Namespace stratejisi:
  - Hangi namespace’ler istisna, hangileri sıkı?
- Uygulama etkisi:
  - `runAsNonRoot`, privilege escalation, hostPath, capabilities gibi kırılacak alanları not et.
- Teşhis:
  - Admission hatası hangi alanı hedefliyor?
- Doğrulama:
  - Örnek pod deploy’u PSS kuralına göre beklenen sonucu veriyor mu?

## Common mistakes
- Tüm cluster’a restricted basıp sistem namespace’lerini bozmak.
- PSS’yi belgeleyip workload migration planı yapmamak.

## References
- `skills/k8s-sec-read-only-filesystem`
- `skills/k8s-sec-seccomp-apparmor`
