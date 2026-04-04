# Faz 2.E Telemetri Politikası

Sentinel CLI için telemetri varsayılan olarak **kapalıdır**. Faz 2.E kapsamında yalnız politika kararı dokümante edilmiştir; üretim telemetrisi veya OpenTelemetry exporter entegrasyonu bu turda eklenmemiştir.

## Karar

- Varsayılan durum: kapalı
- Etkinleştirme modeli: ileride açık bir opt-in config veya env alanı ile
- PII politikası: kullanıcı prompt içeriği, API anahtarı, dosya içeriği ve tool stdout gövdesi dışarı gönderilmez
- İzin verilen özet alanlar: istek sayısı, hata sınıfı, süre, sağlayıcı adı, tool adı, oturum kimliğinin redakte veya hash edilmiş türevi

## Bu turdaki kapsam

- Kod tarafında exporter, span veya metrik gönderimi yok
- README ve bu belge üzerinden “kapalı varsayılan” politika netleştirildi
- Trajectory ve log mekanizmaları telemetri yerine yerel tanılama amacıyla kullanılmaya devam eder

## Sonraki adım ilkeleri

- Telemetri açılacaksa açık opt-in alanı eklenmeli
- Erişilemeyen exporter, CLI akışını bozmamalı
- Secret redaction kuralları log politikasından daha gevşek olamaz
