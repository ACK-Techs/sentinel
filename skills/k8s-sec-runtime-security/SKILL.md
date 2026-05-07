---
name: k8s-sec-runtime-security
description: "Runtime tehdit tespiti kurmak, Falco benzeri kurallarla şüpheli davranışları yakalamak veya “container çalışırken neyi alarm sayacağız?” kararını vermek gerektiğinde kullan. Amaç: **çalışma zamanı görünürlüğünü aksiyona çevirmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Runtime detection kapsamı
- Temel kural sınıfları ve alarm yönlendirmesi
- Doğrulama: kontrollü olayla alert akışının test edilmesi

## Workflow
- Tehdit modelini seç:
  - Shell spawn, hassas path erişimi, ayrıcalık yükseltme, beklenmeyen network.
- Kural seviyesi:
  - Gürültü yaratmayacak minimum değerli kurallarla başla.
- Entegrasyon:
  - Alert nereye gidecek? SIEM, webhook, Slack?
- Operasyon:
  - False positive’leri bastırma ve tuned policy süreci.
- Doğrulama:
  - Güvenli test olayı üret ve kural tetiklenmesini doğrula.

## Common mistakes
- Default kural set’ini körlemesine açıp alarm seli yaratmak.
- Tetiklenen alarm için runbook tanımlamamak.

## References
- `skills/sec-incident-response`
- `skills/obs-alertmanager-routing`
