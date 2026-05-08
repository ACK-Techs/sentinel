## Vector Store Seçim Rehberi (Sentinel)

Bu doküman `llm-context-vector-store` skill’inde “hangi vektör deposu / hangi konfigürasyon” sorusuna karar verirken kullanılacak kriterleri sabitler. Amaç: hız tek kriter olmasın; TTL, metadata filtre ve yönetilebilirlik önceliklensin.

### Karar kriterleri (öncelik sırası)

1. **Metadata filtre gücü**
   - Query başına “sadece şu scope” (profil/workspace, kaynak tipi, güven seviyesi) filtreleme mümkün olmalı.
   - En azından `profile_id`, `doc_type`, `security_level`, `workspace_hash` filtrelenebilir olmalı.

2. **Silme/ayar yönetilebilirliği**
   - Yanlış indexlemeyi geri almak için delete/overwrite veya yeniden index imkanı olmalı.
   - “Index sadece eklenir” senaryosu kabul edilecekse, TTL ve compaction planı yazılmalı.

3. **TTL / aging stratejisi**
   - Bellek politikası değiştiğinde (ör. `policy:user` -> `policy:project`) eski dokümanlar birikmemeli.
   - TTL, metrik ile birlikte raporlanmalı (ör. “expired_docs_count”).

4. **Metadata şeması uyumu**
   - Embedding model değişince yeniden index gerekebilir; bu durumda metadatalar yeniden yazılabilir olmalı.
   - `doc_id` stabil olmalı (hash orijinal doküman + chunk id).

5. **Performans profili (hız + determinism)**
   - Hız önemli; fakat aynı girişte benzer sonuç determinism beklentisi korunmalı.
   - Non-deterministic rerank veya approximate search varsa recall düşüşünü ölç.

6. **Hata modları**
   - Depo down olursa fail-fast mı, degrade mi? Bu karar skill katmanında açık olmalı.

### Sentinel entegrasyon önerileri

1. **Store scope isimlendirmesi**
   - Her profile/workspace için ayrı “collection” veya namespace kullan.
   - Örn: `ws_<workspace_hash>__profile_<profile_name>`

2. **Path & kalıcılık**
   - Yerel depoda veri `cli/.sentinel/` veya proje bellek kökü ile uyumlu tutulmalı.
   - `.gitignore` ile korunmalı; secret/kapsamlı içerik repoya girmemeli.

3. **Metadata minimal set (zorunlu)**
   - `doc_id` (stabil)
   - `source_uri` (varsa)
   - `doc_type` (markdown, code, log, etc.)
   - `workspace_hash`
   - `profile_id` (veya profil adı)
   - `security_level` (trusted/untrusted)

### “Doğru” indexleme yaklaşımı

- Indexlemede tek doküman başına:
  - chunk’ları üret
  - her chunk için `doc_id` + `chunk_id` türet
  - embedding üret
  - payload olarak `metadata + text` birlikte sakla
- Indexleme aşaması “idempotent” olmalı:
  - aynı `doc_id` tekrar indexlenirse overwrite davranışı tanımlı olmalı.

### Kabul kriterleri

- Aynı query için cache hit / retrieval recall metrikleri takip edilebiliyor.
- Metadata filtre “en az” `workspace_hash` ve `security_level` ile çalışıyor.
- TTL/compaction planı dokümante.

### İlgili skill’ler

- `../llm-context-rag-pipeline/references/rag-pipeline-contract.md`
- `../llm-context-chunking-strategy/references/chunking-strategy-matrix.md`

