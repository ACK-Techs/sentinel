## Bellek Index Şeması v1 (Sentinel)

Bu doküman `agentic-memory-index-schema` için bellek index dosyalarında kullanılacak alanları ve versiyonlama davranışını somutlaştırır.

### Şema hedefi

Index, bellek extract/dream/magic docs gibi pipeline adımlarının:
- hangi konuya ait olduğunu,
- son görünüm zamanını,
- güven seviyesini,
- hangi kaynaklardan türetildiğini
tek yerde bulmasını sağlar.

### Versiyonleme

- Index JSON içinde `schema_version` alanı zorunlu.
- v1 okuyucu:
  - bilinmeyen alanları ignore etmeli,
  - eksik alanlarda default veya “inferable=false” yaklaşımı kullanmalı.

### Zorunlu alanlar (v1)

Her index kaydı için önerilen alanlar:

- `schema_version`: string (ör. `"v1"`)
- `topic`: string
- `last_seen`: ISO 8601 datetime string (timezone dahil önerilir)
- `confidence`: number (0..1)
- `source_refs`: array
  - her eleman en az: `{ "kind": "...", "ref": "..."}`
  - örnek kind: `"conversation_turn"`, `"tool_result"`, `"magic_doc"`
- `enforce_policy`: string veya enum (örn. `"project"` / `"user"` / `"none"`)

Opsiyonel alanlar:
- `tags`: array<string>
- `summary_hint`: kısa özet (uzun metin saklama)
- `embedding_fingerprint`: embedding yeniden üretimi için amaçlı fingerprint

### `source_refs` tasarım kuralı

`source_refs` alanı sadece iz sürme içindir. İçerik/secret taşımamalı.

### Örnek index kaydı (şekil)

```json
{
  "schema_version": "v1",
  "topic": "grafana api auth hatasi",
  "last_seen": "2026-05-09T00:12:34+03:00",
  "confidence": 0.72,
  "enforce_policy": "project",
  "source_refs": [
    { "kind": "conversation_turn", "ref": "turn:14" },
    { "kind": "magic_doc", "ref": "skills/llm-context-rag-pipeline:MAGIC_DOC:03" }
  ],
  "tags": ["grafana", "auth", "troubleshoot"]
}
```

### Redaksiyon uyumu

Index kaydına “secret içeren ham metin” koyma.
Index, secret-safe özetler ve referanslar taşımalı.

### Kabul kriterleri

- Index v1 kayıtları parse edilebilir.
- Eksik alanlarda okuma davranışı predictable.
- Pipeline’lar `topic/last_seen/confidence/source_refs` alanlarına bağımlı kalır.

