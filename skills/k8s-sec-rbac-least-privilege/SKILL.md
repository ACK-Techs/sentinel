---
name: k8s-sec-rbac-least-privilege
description: "Kubernetes RBAC tasarımını en az ayrıcalık prensibiyle sıkılaştırmak, fazla izinleri budamak veya “şu controller gerçekten hangi verb’lere ihtiyaç duyuyor?” sorusunu cevaplamak gerektiğinde kullan. Amaç: **çalışır ama daraltılmış izin seti üretmektir**."
---

## Purpose
Bu skill’in çıktısı:
- Role/ClusterRole daraltma stratejisi
- Fazla izin tespiti ve budama planı
- Doğrulama: gerekli işlev sürüyor, fazla izinler kalkıyor

## Workflow
- Mevcut rolü incele:
  - Gerçekten kullanılan resource/verb’ler hangileri?
- Daralt:
  - Wildcard resource/verb’leri somut listeye indir.
- Subject doğrula:
  - Aynı rol kaç farklı SA/user tarafından kullanılıyor?
- Güvenli test:
  - Önce `can-i` ve staging benzeri doğrulama.
- Doğrulama:
  - Gerekli operasyon devam ediyor, gereksiz erişim reddediliyor.

## Common mistakes
- “Çalışıyorsa dokunma” diyerek admin benzeri rolleri bırakmak.
- Ortak ServiceAccount’ları çok geniş kullanmak.

## References
- `skills/k8s-core-rbac`
- `skills/k8s-sec-workload-identity`
