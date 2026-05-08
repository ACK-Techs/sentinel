---
name: llm-context-reranking
description: "RAG pipeline'da ilk retrieval sonuçlarının alakasını artırmak için cross-encoder reranking uygulanacağında kullan"
---

## Purpose
Bi-encoder embedding araması hız için optimize edilmiştir ama precision düşüktür. Cross-encoder reranker, her (query, document) çiftini ayrı ayrı değerlendirerek daha hassas sıralama yapar. Bu, pahalıdır ama top-k kalitesini önemli ölçüde artırır.

## Workflow

### İki Aşamalı Retrieval
```
[1] Bi-encoder retrieval → top-50 hızlı getir (recall odaklı)
[2] Cross-encoder rerank → top-50'den top-5 seç (precision odaklı)
```

### Cross-Encoder ile Reranking
```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, candidates: list[str], top_k: int = 5) -> list[str]:
    """Cross-encoder ile yeniden sırala."""
    pairs = [(query, doc) for doc in candidates]
    scores = reranker.predict(pairs)
    
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in ranked[:top_k]]
```

### LLM Tabanlı Reranker (Daha Pahalı, Daha Esnek)
```python
def llm_rerank(query: str, candidates: list[str], top_k: int = 3) -> list[str]:
    prompt = f"""Sorgu: {query}

Aşağıdaki belge parçalarını alaka düzeyine göre 1-10 arası puanla.
JSON formatında: [{{"idx": 0, "score": 8}}, ...]

Belgeler:
{chr(10).join(f"[{i}] {doc[:200]}" for i, doc in enumerate(candidates))}"""
    
    result = json.loads(llm.complete(prompt))
    ranked = sorted(result, key=lambda x: x["score"], reverse=True)
    return [candidates[r["idx"]] for r in ranked[:top_k]]
```

### Cohere Rerank API
```python
import cohere
co = cohere.Client(api_key=os.environ["COHERE_API_KEY"])

results = co.rerank(
    query=query,
    documents=candidates,
    model="rerank-multilingual-v3.0",
    top_n=5
)
reranked_docs = [r.document["text"] for r in results.results]
```

### Performans Dengesi
```python
# top_initial büyük tutarak recall'u artır, reranker'ı küçük top_k ile bitir
def retrieve_and_rerank(query: str) -> list[str]:
    candidates = vector_search(query, k=50)   # geniş arama
    return rerank(query, candidates, top_k=5)  # precision odaklı daralt
```

## Common mistakes
- Tüm corpus'u cross-encoder'dan geçirmek — O(n) maliyeti, çok yavaş.
- Reranker ve embedding modelini farklı dillerde kullanmak — Türkçe için multilingual model seçin.
- Initial retrieval top_k'yı çok küçük tutmak (5) — iyi sonuç reranker'a hiç gelmez.
- Cross-encoder skorunu threshold olarak kullanmadan tüm sonuçları döndürmek.

## References
- `skills/llm-context-rag-pipeline`
- `skills/llm-context-hybrid-search`
