## LLM Output Trust Policy (Sentinel)

Bu doküman `agentic-sec-llm-output-trust` skill’inin kritik eylemlerde “LLM çıktısına körü körüne güvenme” politikasını operasyonel hale getirir.

### Varlık ayrımı (Proposed vs Executed)

LLM’den gelen iki şey ayrı düşünülmeli:

1. **Proposed command / proposed tool args**
   - Modelin önerisi.
   - Bu öneri *asla* doğrudan çalıştırılmaz.

2. **Executed command / executed tool args**
   - Sentinel’in validasyon katmanından geçmiş ve policy ile uyumlu hale getirilmiş nihai emir.

Doküman kuralı:

- “modelin önerdiği komut” ile “çalıştırılan komut” metin/argüman düzeyinde birebir aynı olmak zorunda değildir; doğrulama sonucu canonicalize edilebilir.

### Validation katmanı (minimum kontrol seti)

- Tool adı:
  - izinli tool listesinde mi?
  - built-in aracı mı (veya MCP isim çakışması mı)?
- Tool argümanları:
  - JSON/format parse edilebiliyor mu?
  - required alanlar var mı?
  - type/enum/range kuralları sağlanıyor mu?
- Eylem sınırları:
  - path/jail kuralları: `write_file` veya shell komutlarında traversal engeli uygulanıyor mu?
  - ağ erişimi: dışarı veri gönderebilecek tool patternleri var mı?

### Suspicion flag’leri

Şu durumda “yüksek risk modu” tetiklenmeli:

- Prompt injection pattern’leri:
  - “ignore previous”, “system prompt”, “developer message” gibi role override anlatımları
- Tool overreach:
  - modeli gereksiz shell/web/credential tool çağırmaya iten argümanlar
- Output karışıklığı:
  - JSON/format bozuluyor ve model serbest metinle “tool args” üretmeye çalışıyor

Risk modu:
- default: `dry-run` ve kullanıcıya kısa açıklama + önerilen güvenli alternatif
- kritik operasyonlarda: explicit onay veya tamamen reddet

### Degrade stratejileri

Validation başarısızsa:

1. parse/format bozuksa:
   - modelden yeniden “sadece schema” formatında output isteme (tek deneme)
2. argüman kural dışıysa:
   - ilgili argümanı canonicalize et (mümkün değilse reddet)
3. tool izni yoksa:
   - “neden izin yok”u ifşa etmeden (secret-safe) policy gerekçesiyle reddet

### Kabul kriterleri

- Executed komut/argümanlar her zaman policy’den geçmiş olmalı.
- Loglar secret içermemeli.
- Risk modu tetiklendiğinde eylem niyeti kullanıcıya şeffaf raporlanmalı.

