---
name: obs-prometheus-instant-query
description: Prometheus HTTP API `GET /api/v1/query` ile “anlık” sorgu atmak, `time=` parametresiyle geçmişte bir ana bakmak veya JSON `resultType` (vector/scalar/string) çıktısını doğru parse etmek gerektiğinde kullan. `query_range` değil; tek zaman noktasına odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- `query` endpoint’i için örnek istek (URL encoding + opsiyonel `time=`)
- Dönen `resultType`’a göre parser beklentisi (vector vs scalar)
- “Boş sonuç / hata” durumlarında hızlı kontrol listesi

## Workflow
- Sorgu tipini belirle (çıktı modeli buradan gelir):
  - **Instant vector**: label set’i + tek değer (çoğu metric sorgusu)
  - **Scalar**: tek sayı (örn. `scalar(...)` veya `count(...)` bazen)
  - **String**: nadir (bazı fonksiyonlar)
- Parametreleri seç:
  - `query=<promql>` zorunlu
  - `time=` opsiyonel: “o andaki” değer için unix/RFC3339 (client tarafında tek standardı seç)
- JSON’u doğru oku:
  - `data.resultType=vector` → `data.result[]` içinde `metric` + `value` (ts,value)
  - `data.resultType=scalar` → `data.result` doğrudan `[ts,value]`
- “Boş sonuç” için hızlı teşhis:
  - Scrape var mı? `up` kontrolü.
  - Label filtresi doğru mu? (`job`, `namespace`)
  - `time` gelecekte mi / çok eski mi? (retention)
- Ne zaman `query_range` kullanacağını söyle:
  - Trend/çizgi gerekiyorsa `query_range`; tek snapshot gerekiyorsa `query`.

## References
- `skills/obs-prometheus-query-range`
