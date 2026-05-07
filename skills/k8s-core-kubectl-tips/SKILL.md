---
name: k8s-core-kubectl-tips
description: `kubectl` ile günlük operasyonu hızlandırmak, doğru filtreleme/çıktı alma alışkanlıkları kurmak veya debug sırasında terminal verimini artırmak gerektiğinde kullan. Amaç: **doğru komutu daha hızlı ve daha güvenli kullanmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- Kategori bazlı `kubectl` kullanım kalıpları (listeleme, describe, logs, exec, jsonpath)
- Yanlış komut kullanımından doğan riskleri azaltan pratikler
- Doğrulama: komut çıktısının karar vermek için yeterli hale gelmesi

## Workflow
- Soruna göre komut sınıfı seç:
  - “Ne var?” → `get`
  - “Neden olmuyor?” → `describe`
  - “Container ne diyor?” → `logs`
  - “İçeride bak” → `exec`
- Çıktıyı daralt:
  - Namespace, label selector, field selector kullan.
  - Gerekirse `-o wide`, `-o yaml`, `-o jsonpath` ile hedefli bak.
- Güvenli alışkanlık:
  - Önce read-only komutlar; delete/patch/apply sonradan.
  - Yanlış context riskine karşı context/namespace görünürlüğü.
- Tekrar eden akışlar:
  - Alias/krew plugin kullanımı uygunsa belirt; zorunlu kılma.
- Doğrulama:
  - Çıktı gerçekten root cause’a yaklaştırıyor mu, yoksa gürültü mü?

## Common mistakes
- `-A` ile tüm cluster’ı tarayıp gürültüye boğulmak.
- `describe` yerine sadece `logs` bakmak: scheduler/image pull hatası kaçabilir.

## References
- `skills/debug-k8s-pod`
- `skills/debug-k8s-network`
