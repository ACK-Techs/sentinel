---
name: obs-gateway-health-status
description: Gateway’de `/health` ve `/api/v1/status` gibi endpoint’lerle kendi durumunu ve Prometheus/Loki/Tempo backends durum özetini döndürmek; “gateway up ama backend down” ayrımını netleştirmek gerektiğinde kullan. Odak: **health semantics + dependency checks**.
---

## Purpose
Bu skill’in çıktısı:
- Health endpoint sözleşmesi: liveness vs readiness vs dependency status ayrımı
- Backend check stratejisi: hangi lightweight sorgularla “çalışıyor” denecek?
- Doğrulama: backend down/up senaryolarında dönen status ve cache davranışı

## Workflow
- Endpoint’leri ayır:
  - Liveness: process ayakta mı? (DB/backends kontrol etme).
  - Readiness: gateway trafik alabilir mi? (kritik dependency kontrolü).
  - Status: backend’lerin özet durumu (latency, last_ok, error).
- Backend check tasarımı:
  - Prometheus: hafif `/-/ready` veya basit API ping.
  - Loki: hafif endpoint/ping; pahalı query kullanma.
  - Tempo: readiness/health; pahalı TraceQL araması yapma.
- Zamanlama ve cache:
  - Status check’lerini her istekte backend’e vurma; kısa TTL cache uygula.
  - “Stale” bilgisini döndür (son başarılı check zamanı).
- Güvenlik:
  - Status endpoint’i internal erişime açık olmalı; dış dünyaya backend detaylarını saçma.
- Doğrulama:
  - Bir backend’i kapat; status bunu doğru yansıtsın ama liveness 200 kalsın.

## Common mistakes
- /health çağrısında pahalı backend sorgusu yapmak: self-DoS.
- Liveness’i dependency durumuna bağlamak: restart loop üretir.

## References
- `skills/obs-gateway-caching`
- `skills/obs-gateway-error-model`
