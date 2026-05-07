---
name: k8s-storage-emptydir
description: Geçici pod ömrü kadar storage kullanmak, container’lar arasında ephemeral veri paylaşmak veya “disk mi memory mi kullanmalıyım?” kararını vermek gerektiğinde kullan. Amaç: **kalıcı olmayan depolamayı doğru sınırlar içinde kullanmaktır**.
---

## Purpose
Bu skill’in çıktısı:
- `emptyDir` kullanım uygunluğu
- Disk-backed vs `medium: Memory` kararı
- Doğrulama: pod restart/silme sonrası veri davranışı

## Workflow
- Veri ömrünü doğrula:
  - Pod ölünce veri kaybolabilir mi?
- Medium seç:
  - Disk mi RAM mi? boyut limiti gerekli mi?
- Kullanım deseni:
  - Cache, scratch space, init→main paylaşımı gibi hafif senaryolar.
- Kaynak etkisi:
  - Memory-backed ise node RAM baskısı yaratır mı?
- Doğrulama:
  - Pod restart/schedule sonrası veri beklentisi net mi?

## Common mistakes
- Kalıcı veri için `emptyDir` kullanmak.
- `medium: Memory` ile node RAM’ini sessizce tüketmek.

## References
- `skills/k8s-core-init-containers`
- `skills/k8s-core-sidecar-pattern`
