---
name: obs-prometheus-service-discovery
description: Prometheus’ta hedefleri otomatik bulmak için service discovery (Kubernetes SD / file SD / static) seçmek ve doğru filtre-relabel kurgusunu yapmak gerektiğinde kullan. “Neyi scrape etmeli?”, “SD mi ServiceMonitor mu?”, “annotation/label ile hedef seçimi” gibi durumlara odaklanır.
---

## Purpose
Bu skill’in çıktısı, seçilen keşif yöntemine göre **net bir hedefleme planı** ve uygulanabilir bir config parçasıdır:
- SD seçimi (static vs file SD vs k8s SD vs operator CRD) + gerekçe
- “Hedef seçme kuralı” (label/annotation/selector) + relabel ile filtre
- Yanlış keşfi önleyen guardrail’ler (kardinalite ve gürültü kontrolü)

## Workflow
- Keşif yöntemini seç (karar ağacı):
  - **Static**: <20 hedef, nadir değişim, elle yönetim kabul edilebilir.
  - **File SD**: hedef listesi başka sistemce üretiliyor (CMDB, script) ve Prometheus sadece “okuyucu”.
  - **Kubernetes SD**: cluster içinde dinamik servis/pod keşfi; filtreleme şart.
  - **Operator (ServiceMonitor/PodMonitor)**: k8s-native lifecycle isteniyor; en temiz yol.
- Kubernetes SD kullanıyorsan hedef tipini netleştir:
  - `role: service` mi `role: pod` mu? (hangi metadata’ya göre seçeceğin değişir)
  - Port seçimi: named port mu, number mı? (yanlış port en sık hata)
- Hedef seçme kuralını “opt-in” yap:
  - Varsayılan: her şeyi keşfetme. Örn. `prometheus.io/scrape="true"` gibi annotation veya `monitoring=enabled` label’ı şart koş.
  - Namespace sınırı: `namespace` allowlist/selector.
- Relabel ile filtreyi kesinleştir:
  - `keep` ile seç, `drop` ile gürültüyü temizle (ikisini karıştırma).
  - “Kardinalite tuzakları”: pod adı gibi yüksek churn label’larını otomatik ekleme.
- Doğrulama:
  - Hedefler: Prometheus’ta target listesinde beklenen sayıda mı?
  - `up{job="..."} ` ve `count(up{job="..."})` ile hızlı doğrula.

## Anti-patterns
- “Cluster’daki her pod’u scrape et”: kısa sürede TSDB ve alert gürültüsü üretir.
- Hedefi annotation/label ile seçmek yerine sadece `drop` ile “temizlemeye çalışmak”.

## References
- `skills/obs-prometheus-scrape-config`
