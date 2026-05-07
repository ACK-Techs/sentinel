---
name: obs-otel-sampling-config
description: OpenTelemetry Collector’da tail-sampling ile kural tabanlı trace örnekleme tasarlamak (error/latency/route bazlı) veya “trace yok çünkü sampling çok agresif” sorununu çözmek gerektiğinde kullan. Head sampling değil; **tail sampling policy** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Tail sampling policy set’i (hata, yüksek latency, kritik route) ve öncelik sırası
- Kapasite notu: tail sampling’in bellek/CPU maliyeti ve riskleri
- Doğrulama: hedef senaryoda trace’in gerçekten tutulduğunu kanıt

## Workflow
- Hedefi tanımla:
  - Neyi “mutlaka sakla”? (status=ERROR, p99>eşik, belirli endpoint)
  - Neyi “tutmasan olur”? (healthcheck, statik asset)
- Politika tasarımı:
  - Öncelik: error > yüksek latency > belirli servis/route > probabilistic fallback.
  - Policy matcher’ları semantic conventions’a göre yaz (uydurma key kullanma).
- Maliyet ve güvenlik:
  - Tail sampling buffer süresi ve beklenen throughput.
  - Çok geniş policy backlog yaratır mı?
- Doğrulama:
  - Hata üreten bir request gönder; trace backend’de var mı?
  - Normal request’lerde örnekleme oranı beklenen mi?

## Common mistakes
- Her şeyi tail sample etmeye çalışmak: collector memory/CPU patlar.
- Attribute adları tutarsız: policy hiç eşleşmez, trace’ler kaybolur.

## References
- `skills/obs-otel-semantic-conventions`
- `skills/obs-otel-collector-processors`
