---
name: llm-prompt-summarization
description: "Uzun belge veya konuşma özetlemesi gerektiğinde; map-reduce, recursive ve incremental stratejilerden hangisini seçmek ve uygulamak için kullan"
---

## Purpose
Tek seferde sığmayan belgeler için hierarchical özetleme gerekir. Bu skill, belge boyutuna göre doğru stratejiyi seçmeyi ve Sentinel'de uygulanabilir pipeline kurmayı kapsar.

## Workflow

### Strateji Seçim Ağacı
```
Belge < 50K token    → Tek geçiş (doğrudan)
50K–200K token       → Recursive summarization
200K+ token          → Map-Reduce
Streaming belge      → Incremental (rolling) summarization
```

### Map-Reduce Implementasyonu
```python
def map_reduce_summarize(text: str, chunk_size: int = 8000) -> str:
    # MAP: Her chunk'ı ayrı özetle
    chunks = split_text(text, chunk_size)
    chunk_summaries = []
    for chunk in chunks:
        summary = llm.complete(f"Şu metni 200 kelimede özetle:\n\n{chunk}")
        chunk_summaries.append(summary)
    
    # REDUCE: Özetleri birleştir
    combined = "\n\n---\n\n".join(chunk_summaries)
    final = llm.complete(
        f"Aşağıdaki bölüm özetlerini tek tutarlı özete birleştir. "
        f"Tekrarları kaldır, önem sırasına göre düzenle:\n\n{combined}"
    )
    return final
```

### Recursive Summarization
```python
def recursive_summarize(text: str, max_tokens: int = 4000) -> str:
    if token_count(text) <= max_tokens:
        return llm.complete(f"Özetle:\n\n{text}")
    
    # Ortadan böl
    mid = len(text) // 2
    left_summary = recursive_summarize(text[:mid])
    right_summary = recursive_summarize(text[mid:])
    
    combined = f"{left_summary}\n\n{right_summary}"
    return recursive_summarize(combined)
```

### Özetleme Prompt Şablonları
```python
# Yönetici özeti
EXEC_SUMMARY = "Bu belgeyi 5 madde halinde yönetici özetine dönüştür. Her madde eylem odaklı olsun."

# Teknik özet
TECH_SUMMARY = "Teknik kararları, kullanılan teknolojileri ve açık sorular/riskleri listele."

# Konuşma özeti
CHAT_SUMMARY = "Bu konuşmanın önemli noktalarını çıkar: kararlar, eylem maddeleri, açık sorular."
```

## Common mistakes
- Map aşamasında özetleri çok kısa tutmak (50 kelime) — reduce aşamasında bağlam kaybı.
- Chunk sınırlarını cümle ortasında kesmek — anlam kırılıyor, cümle sınırında kesin.
- Her chunk için farklı prompt kullanmak — tutarsız özetler reduce aşamasını zorlaştırır.
- Incremental özetlerde önceki özeti yeni chunk'a vermemeyi unutmak — devamlılık bozulur.

## References
- `skills/llm-context-chunking-strategy`
- `skills/llm-context-window-management`
- `skills/llm-context-long-doc-processing`
