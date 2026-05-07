---
name: obs-prometheus-remote-write
description: Prometheus metriklerini uzun süreli saklama / merkezi depolama için `remote_write` ile dış sisteme göndermek gerektiğinde kullan. “remote_write url”, “write_relabel_configs”, “queue_config”, “dropped samples”, “backpressure/timeout” gibi konularda doğru ayar ve failure-mode analizi üretmek için.
---

## Purpose
Bu skill’in çıktısı, bir veya daha fazla hedefe gönderim yapan **`remote_write` konfigürasyonu** ve “ne gönderiyoruz / neyi drop ediyoruz?” karar kaydıdır:
- `remote_write[]` hedef(ler)i (URL + auth/TLS placeholder)
- `write_relabel_configs` ile **gönderilecek seri kapsamı**
- `queue_config` ile **dayanıklılık + latency + kayıp** dengesini ayarlama

Amaç sadece “URL eklemek” değil; remote backend sorunlarında Prometheus’un nasıl davranacağını öngörmektir.

## Workflow
- İhtiyacı netleştir:
  - Neden remote_write? (uzun retention, multi-cluster merkezi sorgu, DR)
  - Hedef sistem: Thanos/Cortex/Mimir/VM/etc. (protokol beklentisi, auth şekli)
- Gönderim kapsamını seç (en kritik karar):
  - Varsayılan: **her şeyi göndermeyin**. Önce “kritik metrikler” + recording’ler.
  - `write_relabel_configs` ile `__name__`, `job`, `namespace` gibi filtrelerle `keep/drop` kararlarını yaz.
  - Kardinalite yüksek serileri drop etmek için açık kural ekle (örn. path/query gibi etiket patlatanlar).
- Güvenlik ve bağlantı:
  - `basic_auth` / `authorization` / mTLS gerekiyorsa **secret değerlerini yazma**; kaynaklarını belirt.
  - `remote_timeout` ve retry davranışını hedef SLA’ya göre belirle.
- Kuyruk ve failure mode:
  - `queue_config` ile batch boyutu ve paralellik: backend yavaşsa ne olur?
  - Beklenen semptomlar: `remote_write` backlog, `dropped_samples_total`, artan memory.
  - Karar notu: “backend down iken veri kaybı kabul edilebilir mi?” (kayıp/latency trade-off)
- Doğrulama:
  - Prometheus tarafı: `prometheus_remote_storage_*` metrikleriyle gönderim/düşürme var mı?
  - Backend tarafı: hedef sistemde yeni seri görülüyor mu? (küçük bir canary seri ile)

## Common mistakes
- “Her şeyi gönder”: gereksiz maliyet + çok yüksek egress + backend cardinality patlaması.
- Drop/keep kararı olmadan canlıya çıkmak: sorun çıktığında hangi serilerin gittiği belirsiz olur.
- Secret’ları YAML’e yazmak: repo/terminal log’larında sızıntı riski.

## References
- `skills/cos-deploy-prometheus`
- `skills/obs-prometheus-storage-tsdb`
