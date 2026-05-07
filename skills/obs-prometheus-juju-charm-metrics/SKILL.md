---
name: obs-prometheus-juju-charm-metrics
description: COS/Juju ortamında charm’ların Prometheus’a nasıl metrik “yayınladığını” (metrics-endpoint relation) anlamak, bir uygulamayı scrape kapsamına almak veya “metrik gelmiyor” durumunda relation bazlı teşhis yapmak gerektiğinde kullan.
---

## Purpose
Bu skill’in çıktısı:
- Bir charm’ın metriklerini Prometheus’a bağlamak için gereken relation adımı(ları)
- “Hangi endpoint scrape ediliyor?” ve “hangi label’lar geliyor?” doğrulama kontrolü
- Relation kaynaklı tipik hata senaryoları için teşhis akışı

## Workflow
- Ön koşul:
  - COS modelinde `prometheus-k8s` var mı? (yoksa önce deploy et)
- Relation’ı bul ve bağla:
  - Charm’ın hangi endpoint’i metrik yayıyor? (genelde `metrics-endpoint`)
  - İlişkileri gör: `juju status --relations` (hangi app hangi app’e bağlı)
  - Gerekirse relation ekle/kontrol et (app isimleri modeline göre değişir).
- Scrape’in geldiğini doğrula:
  - Prometheus targets ekranında ilgili job/target görünüyor mu?
  - `up` ve `scrape_samples_scraped` ile “gerçekten scrape var mı?” kontrol et.
- “Metrik gelmiyor” teşhisi (relation odaklı):
  - Relation yok / yanlış endpoint: `juju status --relations` ile netleştir.
  - Charm “blocked”/“waiting”: `juju status` + ilgili unit log/hook hata.
  - TLS/auth: Prometheus’un scrape edemediği durumda target error mesajı (credential’ları log’a dökme).
- Çıktıyı raporla:
  - Hangi relation kuruldu, hangi target(lar) bekleniyor, hangi sinyalle doğrulandı.

## References
- `skills/cos-deploy-prometheus`
- `skills/juju-model-cos`
