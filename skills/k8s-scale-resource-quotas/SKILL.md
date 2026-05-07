---
name: k8s-scale-resource-quotas
description: Namespace bazlı kaynak tüketimini sınırlamak, “bir ekip tüm cluster CPU’sunu yiyor” sorununu önlemek veya çok kiracılı kümelerde adil kullanım politikası kurmak gerektiğinde kullan. Amaç: **kapasiteyi yönetişim kuralına dönüştürmektir**.
---

## Purpose
Bu skill’in çıktısı:
- ResourceQuota ve gerekirse LimitRange tasarımı
- Namespace bazlı CPU/RAM/object count sınırları
- Doğrulama: aşım durumunda beklenen admission davranışı

## Workflow
- Tüketim modelini çıkar:
  - Namespace’in normal tavanı nedir? burst ihtiyacı var mı?
- Quota alanlarını seç:
  - requests, limits, PVC sayısı, object count vb.
- LimitRange ile tamamla:
  - Default request/limit gerekiyorsa ekle.
- Operasyon etkisi:
  - CI namespace’leri veya kısa ömürlü job’lar gereksiz bloklanır mı?
- Doğrulama:
  - Bilinçli bir aşım denemesinde admission beklenen hatayı veriyor mu?

## Common mistakes
- Quota koyup default request/limit tanımlamamak: kullanıcı deneyimi kötüleşir.
- Tüm namespace’lere aynı tavanı vermek.

## References
- `skills/k8s-core-namespace`
- `skills/k8s-core-resource-requests-limits`
