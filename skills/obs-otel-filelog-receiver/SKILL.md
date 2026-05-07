---
name: obs-otel-filelog-receiver
description: OpenTelemetry Collector `filelog` receiver ile node/pod üzerindeki log dosyalarını okuyup parse ederek Loki’ye göndermek veya “log gelmiyor / multiline bozuluyor / label’lar yanlış” sorunlarını çözmek gerektiğinde kullan. Promtail değil; **Collector filelog pipeline** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- `filelog` receiver + parse (json/logfmt/regex) + Loki exporter için örnek YAML iskeleti
- Multiline ve rotation (tailing) davranışı için kararlar
- Doğrulama: Collector telemetry + Loki’de basit LogQL ile “log ulaştı” kanıtı

## Workflow
- Kaynağı netleştir:
  - Dosya yolları (container runtime, app log path), multiline var mı?
  - Agent mı çalışacak (node’a yakın) yoksa gateway mi? (filelog genelde agent)
- Okuma stratejisi:
  - Rotation senaryosu: inode değişimi, “başından okuma” riski.
  - Exclude/include pattern’leri ile gürültüyü azalt.
- Parse ve zenginleştirme:
  - JSON/logfmt parse et; timestamp alanını normalize et.
  - Resource attribute’larından Loki label set’ine minimum mapping (kardinaliteyi patlatma).
- Loki’ye gönderim:
  - Tenant/env ayrımı gerekiyorsa header/label stratejisini yaz.
- Doğrulama:
  - Collector’da receiver accepted ve exporter sent artıyor mu?
  - Loki’de dar selector ile son 5 dk log geliyor mu?

## Common mistakes
- Her field’ı label yapmak: Loki kardinalitesi patlar, query pahalılaşır.
- Multiline’ı “regex ile her şeyi yakala” yapmak: parse hatası ve CPU yükü.

## References
- `skills/obs-otel-collector-receivers`
- `skills/obs-loki-label-strategy`
