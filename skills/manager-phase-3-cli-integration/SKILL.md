---
name: manager-phase-3-cli-integration
description: >-
  Sentinel Faz 3 yöneticisi: Sentinel CLI'nin config-driven ve modüler sorgu
  katmanıyla Prometheus/Loki/Tempo'ya bağlanmasını planlar ve alt-AI prompt'larına
  böler. "Sentinel CLI", "config yaml", "prom/loki/tempo sorgu", "trace by id",
  "RED query", "~/.sentinel/config.yaml" gibi konularda tetiklenir.
---

## Purpose

Bu skill yönetici ajan içindir; doğrudan kod yazmaz, alt-AI prompt'u üretir.
Faz 3'ün hedefi: Faz 2'de doğrulanan COS stack'i üzerine oturacak, URL hardcode
etmeyen, config + env override ile yönetilen modüler bir CLI sorgu katmanı
kurmaktır. Tempo/traces da smoke planının parçasıdır.

## Scope (In / Out)

In:
- `~/.sentinel/config.yaml` şeması: `prometheus.url`, `loki.url`, `tempo.url`
- Config layering: default → file → env override; validation + secret handling
- Modüler sorgu katmanı: prom / loki / tempo için ayrı modüller
- Temel komutlar: RED metrics, log tail, trace by id
- Smoke: üç stack'a bağlanma ve örnek sorgu

Out:
- Yeni telemetri stack bileşeni (Faz 2)
- Target-app değişikliği (Faz 1)
- Otomatik remediation / karar motoru (kapsam dışı)

## Deliverables / Exit Criteria

- CLI üç stack'a config üzerinden bağlanır; hiçbir URL kodda sabit değil.
- Config doğrulama hatalı YAML'da anlamlı hata verir; env override çalışır.
- Secret'lar (token/bearer) dosyadan veya env'den okunur, log'a sızmaz.
- RED metrics sorgusu, Loki tail ve `trace by id` komutları canlı stack'te döner.
- Smoke senaryosu Faz 2'nin örnek sorgu setiyle uyumlu çalışır.

## Sub-task Breakdown Template

1. **Config şeması + layering**: YAML şema tanımı, default/file/env birleştirme,
   validation ve secret handling.
2. **Sorgu katmanı**: `prom`, `loki`, `tempo` modülleri; ortak hata tipi,
   timeout, retry politikası.
3. **Komutlar + smoke**: CLI entrypoint, RED/log tail/trace-by-id komutları,
   uçtan uca smoke script'i.

Her alt göreve: hedef modül yolu, imza taslağı, test edilmeyecek alan ve
referans skill listesi verilir.

## Key References

- `sentinel-coming/cli/skills/agentic-config-*`
- `sentinel-coming/cli/skills/agentic-cli-entrypoint`
- `sentinel-coming/cli/skills/agentic-troubleshoot-*`
- Faz 2 çıktısı: doğrulanmış örnek sorgu seti

## Risks

- URL veya token'ın koda sızması: review adımı her alt görevde zorunlu.
- Config layering'de sessiz override: efektif config'i dump eden komut gerekir.
- Prom/Loki/Tempo client kütüphanelerinde sürüm uyumsuzluğu.
- CLI'nin kapsamını aşıp karar motoruna kayma; scope-out disiplini korunur.

## Coordination Checkpoints

- Alt görev 1 tamamlanmadan 2'ye geçilmez; şema dondurulur.
- Alt görev 2'nin modülleri Faz 2 örnek sorgularıyla birebir eşlenir.
- Smoke başarısızsa hata Faz 2'ye mi Faz 3'e mi ait, yönetici kararıyla ayrılır.
- Kapsam dışı istekler (dashboard üretimi, alerting) reddedilir.
