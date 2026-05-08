## MCP Tool Schema Rehberi (Sentinel)

Bu doküman `agentic-mcp-tool-schema` skill’inde MCP tool’larının input şemalarının kalitesini yükseltmek için kullanılır.

### Hedef

- Modelin tool seçiminde hata yapmasını azaltmak.
- Tool argümanlarının parse/validation aşamasında sürpriz çıkarmamasını sağlamak.
- Token maliyetini aşmadan açıklamaları “yeterli” seviyede tutmak.

### Zorunlu şema kısıtları (pratik)

1. `type`
   - Tool argümanları mümkünse primitive (string/number/boolean) veya controlled object.
2. `required`
   - Kritik alanlar required olmalı; model “boş geçti”ğinde fail hızlı olmalı.
3. `additionalProperties`
   - Varsayılan olarak `false` kullan (ek alanlar parse edilmemeli).
4. Enum ve default
   - Enum’lar modele seçim yapmayı kolaylaştırır.
   - Default değer, “model tahminini” değil “güvenli varsayılanı” temsil etmeli.
5. Numeric ranges
   - timeout, limit, max_items gibi sayılarda min/max tanımla.

### Açıklama metni kalitesi (description)

`description` tek cümlelik genel açıklama değil; modelin doğru parametre seçmesini sağlayan “seçim sinyali” olmalı.

Kural:

- Her parametre açıklamasında en az bir tane:
  - “ne zaman kullanılmalı” veya
  - “ne zaman kullanılmamalı” cümlesi bulunmalı.

### Formatlandırma kuralları

- ISO 8601 datetime bekleniyorsa örnek ver: `2026-05-09T00:12:34+03:00`
- Byte bekleniyorsa bir örnek ver: `1048576` (1 MiB gibi)
- Path bekleniyorsa “relative değil canonical” yaklaşımını yaz (roots politikasıyla birlikte).

### Kabul kriterleri

- Client tarafında şema ihlali “anlamlı hata” ile döner (kullanıcıya secret sızmaz).
- Aynı tool schema ile modelin parse başarısı artar.
- Schema boyutu büyürse bile açıklamalar token bütçesi aşmayacak şekilde kısalır.

### İlgili karar noktaları

- Tool name mapping: `agentic-mcp-tool-mapping` ile isim çakışlarını çöz.
- Transport/auth: `agentic-mcp-sse-transport` ve `agentic-mcp-auth` ile uyumlu log politikası.

