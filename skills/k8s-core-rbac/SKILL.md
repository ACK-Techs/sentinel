---
name: k8s-core-rbac
description: Kubernetes RBAC (Role/ClusterRole ve Binding’ler) tasarlamak, least-privilege uygulamak veya “Forbidden” hatalarını teşhis etmek gerektiğinde kullan. Odak: **izin modelini doğru küçültmek** ve doğrulama komutlarıyla kanıt üretmektir.
---

## Purpose
Bu skill’in çıktısı:
- İhtiyaca göre Role vs ClusterRole kararı ve minimal izin seti
- Binding taslağı (hangi subject: SA/user/group; hangi namespace kapsamı)
- Doğrulama: `kubectl auth can-i` ile izin kanıtı + tipik “Forbidden” kök neden analizi

## Workflow
- İhtiyacı netleştir:
  - Hangi API grupları/kaynaklar/verb’ler gerekli? (get/list/watch vs create/delete)
  - Namespace scope yeterli mi, cluster scope zorunlu mu?
- Rol tasarımı:
  - Minimum verb set’i: çoğu controller için get/list/watch.
  - Write verb’leri sadece gerektiğinde.
- Binding:
  - Subject’i seç: ServiceAccount mı, insan kullanıcı mı?
  - Namespace’ler arası erişim gerekiyorsa açıkça belirt.
- Teşhis (Forbidden):
  - Hata hangi identity ile geliyor? (SA token mı, kubeconfig user mı)
  - Hangi resource/verb eksik? (audit/event’ten çıkar)
  - Impersonate ile test (uygunsa).
- Doğrulama:
  - `kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa> -n <ns>`

## Common mistakes
- ClusterRole’ü “kolay” diye her şeye vermek: gereksiz geniş saldırı yüzeyi.
- Binding namespace’ini karıştırmak: Role doğru ama yanlış namespace’e bağlanmış.

## References
- `skills/k8s-sec-rbac-least-privilege`
