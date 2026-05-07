---
name: k8s-storage-hostpath
description: "HostPath volume kullanmak, risklerini değerlendirmek veya “lokal dosya sistemi pod’a nasıl bağlanır?” sorusunu cevaplamak gerektiğinde kullan. Amaç: **HostPath’i sadece uygun sınırlı senaryolarda kullanmaktır**."
---

## Purpose
Bu skill’in çıktısı:
- HostPath için güvenli kullanım çerçevesi
- Test/lab ile production farkı
- Doğrulama: mount edilen path ve node bağımlılığı kanıtı

## Workflow
- Senaryoyu doğrula:
  - Yerel geliştirme/lab mı? production zorunluluğu mu?
- Path riski:
  - Hangi host dizini bağlanıyor? node-level hassas veri var mı?
- Schedule etkisi:
  - Pod başka node’a giderse veri ne olur?
- Security:
  - HostPath ile container host dosya sistemine ne kadar yaklaşmış oluyor?
- Doğrulama:
  - Pod içinden path görünürlüğü ve node bağımlılığı test et.

## Common mistakes
- HostPath’i “kolay” diye prod’a taşımak.
- Backup/taşınabilirlik planı olmadan stateful workload bağlamak.

## References
- `skills/k8s-storage-local-pv`
- `skills/k8s-storage-microk8s-hostpath`
