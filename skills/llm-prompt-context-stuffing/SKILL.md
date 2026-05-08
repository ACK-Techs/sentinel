---
name: llm-prompt-context-stuffing
description: "Context window'a referans belgeler doldurulacağında; hangi belgelerin, hangi sırayla ve nasıl formatlanarak ekleneceğine karar vermek için kullan"
---

## Purpose
Context stuffing, ilgili bilgiyi model bağlamına gömerek harici araç çağrısı olmadan yanıt kalitesini artırır. Ancak sıra, format ve belge seçimi yanlışsa model kritik bilgiyi gözden kaçırır (lost in the middle problemi).

## Workflow

### Lost in the Middle Problemi
```
Model, context'in başına ve sonuna en fazla dikkat eder.
Ortada kalan belgeler göz ardı edilebilir.

Çözüm: En kritik belgeyi başa veya sona koy.
```

### Belge Ekleme Düzeni
```python
def build_stuffed_context(
    query: str,
    docs: list[str],
    most_relevant_first: bool = True
) -> str:
    """En ilgili belge başa (primer attention zone)"""
    
    header = "Aşağıdaki belgeler sorunu yanıtlamak için referans alınacaktır:\n\n"
    
    separator = "\n\n---\n\n"
    doc_blocks = []
    for i, doc in enumerate(docs):
        doc_blocks.append(f"[BELGE {i+1}]\n{doc}")
    
    context = header + separator.join(doc_blocks)
    return f"{context}\n\n---\n\nSoru: {query}"
```

### Token Bütçesi Yönetimi
```python
def fit_docs_to_budget(
    docs: list[str],
    tokenizer,
    max_tokens: int = 60_000,
    reserve_for_response: int = 4_000
) -> list[str]:
    budget = max_tokens - reserve_for_response
    selected, used = [], 0
    
    for doc in docs:
        doc_tokens = len(tokenizer.encode(doc))
        if used + doc_tokens > budget:
            break
        selected.append(doc)
        used += doc_tokens
    
    return selected
```

### Yapılandırılmış Format
```
Her belgeyi şu yapıda sun:
[KAYNAK: dosya_adı.pdf, Sayfa: 12]
[ÖNEMLİLİK: yüksek]
<içerik>
...
</içerik>
```

## Common mistakes
- Belge sırasını önem sırasına göre düzenlememek — model ortadakileri kaçırır.
- Token bütçesi aşıldığında context'i kesmek — truncation noktasını belgenin ortasında bırakma.
- Ham PDF text'ini temizlemeden koymak — header, footer, sayfa numarası gürültü ekler.
- Tüm belgeyi koymak yerine ilgili pasajı seçmemek — RAG reranking ile kesme yapın.

## References
- `skills/llm-context-rag-pipeline`
- `skills/llm-context-chunking-strategy`
- `skills/llm-context-window-management`
