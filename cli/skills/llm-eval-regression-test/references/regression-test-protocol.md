## Regresyon Test Protokolü (Sentinel)

Bu doküman `llm-eval-regression-test` skill’inin regresyon yakalamada “ne test edilir, nasıl assert edilir ve CI’de nasıl gate’lenir” kısmını somutlaştırır.

### Regresyon kapsamı

Minimum kapsam:

- **Yanıt kalitesi**: doğru bilgi, format uyumu, iddiaların kaynaklarla uyumu (mümkünse)
- **Güvenlik**: yasaklı aksiyon/format ihlali yok
- **Tool-call davranışı** (varsa): doğru tool seçimi + doğru argüman + doğru hedef

Opsiyonel kapsam:

- Bağlam yönetimi: retrieval recall/trim davranışı beklenen aralıkta mı
- Çoklu tur tutarlılık: konu kayması var mı

### Golden dataset formatı (önerilen)

Tek dosya veya dizin halinde saklanabilir. Mantık:

- Her test case içinde:
  - `id`
  - `task_type` (rag_answer, tool_call, classification, etc.)
  - `input`: modelin aldığı mesaj/bağlam başlangıcı
  - `expected_contract`: kesin alanlar (örn. JSON schema alanları)
  - `expected_observations`: semantik doğrulama için beklenen özellikler
  - `assertions`: hangi assert türleri uygulanacak

### Assert türleri (ayrı ayrı)

1. **Exact contract**
   - JSON/format parse edilebiliyor mu?
   - Required alanlar var mı? Type uygun mu?
2. **Semantic match**
   - “Aynı anlam” hedefi için embedding/heuristic benzerlik eşiği.
3. **Constraint violation check**
   - Yasaklı output pattern var mı (örn. gizli bilgi sızıntısı, shell komutu önerisi)?
4. **Tool-call accuracy**
   - `tool_name` eşleşiyor mu?
   - `tool_args` gerekli alanları içeriyor mu ve tip/enum doğru mu?
   - Kısmi doğru çağrı ayrı kategoride raporlanır.

### Gate’leme mantığı

Gate, tek metrikle değil “risk ağırlıklı” olmalı:

- Format ihlali veya security ihlali = hard fail
- Yanıt kalite metrikleri = soft fail (eşik altında)
- Tool-call accuracy = “critical task_type”larda hard fail olabilir

### Raporda bulunması gerekenler

- Baseline vs candidate farkı (delta)
- Hata kümeleri (en sık hangi case’ler kırılıyor)
- İyileştirmeden çok regress olan örnekler
- Maliyet/latency değişimi (kalite artışı vs maliyet trade-off)

### Kabul kriterleri

- Yeni bir bug için önce test case eklenmeli.
- Test case’ler versiyonlu olmalı (`v1/v2`).
- Aynı test seti tekrar çalıştırıldığında ölçüm dalgalanması anlaşılır bir aralıkta kalmalı.

