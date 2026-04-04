---
name: agentic-telemetry-optional
description: Opt-in OpenTelemetry veya metrik hatları; PII yok ve örnek span adları için rehber hazırlarken kullan.
---

## Amaç

**Varsayılan kapalı** veya ürün kararıyla açık — tek cümleyle README’de yazılmalı. **PII yok**: kullanıcı prompt içeriği span attribute’una konmaz; yalnız hash veya uzunluk. **Örnek span adları**: `llm.request`, `llm.stream.chunk`, `tool.execute`, `session.lifecycle`. **Exporter env**: OTLP endpoint, header (secret env’den), protokol — `codex-otel` benzeri desen referans (`../agentic-reference-agentic-folder`).

## Kapsam

### Dahil

- Log ile korelasyon trace id (`agentic-cli-logging`).
- Metrik: istek sayısı, süre, hata oranı (örnek).

### Hariç

- Üçüncü parti analitik SDK (Google Analytics vb.) zorunluluğu.

## Kurallar

- Opt-in onayı config dosyasında açık alan.
- Regülasyon gereksinimi varsa veri minimizasyonu dokümante.
- Devre dışıyken zero overhead hedefi (no-op exporter).

## Kontrol listesi

- [ ] Açıkken bile prompt/log PII sızıntısı testi yapıldı mı?
- [ ] Exporter endpoint erişilemezse graceful degrade?
- [ ] Span isimleri kararlı ve dokümante mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Export başarısız | network / TLS | Kullanıcıyı bilgilendir, CLI çalışmaya devam |
| Çok yüksek volume | sampling | Oran ayarı (proje kararı) |

## İlgili belgeler ve skill'ler

- `../agentic-cli-logging/SKILL.md`
- `../agentic-trajectory-recording/SKILL.md`
- `../agentic-secrets-handling/SKILL.md`
- `../agentic-reference-agentic-folder/SKILL.md`
