---
name: obs-prometheus-unit-testing
description: Prometheus alerting/recording rule’larını canlıya almadan önce `promtool test rules` ile birim test yazmak gerektiğinde kullan. “promtool test formatı”, “eval_time”, “input_series nasıl yazılır?”, “beklenen alert/value” gibi test-yazımı sorularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- `promtool test rules` için test dosyası iskeleti (input series + rule_files + test cases)
- Bir kural için en az 2 senaryo: “tetiklenmeli” ve “tetiklenmemeli”
- Sık hatalara karşı kontrol listesi (zaman, pencere, `for`, label set)

## Workflow
- Test edeceğin kuralı sabitle:
  - Kural dosyası yolu (record/alert adı)
  - Kuralın kullandığı pencere (`rate()[5m]` gibi) ve `for:` süresi
- Input series tasarla:
  - Kuralın beklediği label set’iyle minimal seri üret (gereksiz label ekleme).
  - Örnekleme aralığını belirle (genelde 1m veya 30s); pencereyi besleyecek kadar uzun veri yaz.
- Test case yaz:
  - `eval_time`: tam olarak hangi anda bekliyorsun?
  - Recording için beklenen sample değeri, alerting için beklenen label+annotation (en kritik alanlar).
  - “Negatif” case: eşik altı veya `for` süresi dolmadan önce.
- `promtool` ile çalıştır:
  - `promtool test rules <test-file>` komutunu ver.
  - Fail çıktısında “expected vs got” farkını okuyup input series/eval_time’ı düzelt.

## Common mistakes
- `eval_time`’ı `for:` süresini karşılamayacak kadar erken seçmek.
- `rate()` penceresini beslemeden anlık veriyle test etmeye çalışmak.
- Alert label set’i ile test input label set’inin uyuşmaması (ör. `job` filtreleri).

## References
- `skills/obs-prometheus-alerting-rules`
- `skills/obs-prometheus-recording-rules`
