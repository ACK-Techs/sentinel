---
name: llm-context-hybrid-search
description: "Vektör araması ile BM25 keyword aramasını birleştiren hibrit arama uygulanacağında; her ikisinin zayıf noktalarını telafi etmek için kullan"
---

## Purpose
Semantic search (vektör), bağlamsal benzerliği iyi yakalar ama tam kelime eşleşmesinde zayıftır. BM25, tam terim eşleşmesinde güçlüdür ama anlam tutmaz. Hibrit kombinasyon her iki yöntemin üstün yanlarını birleştirir.

## Workflow

### Hibrit Skor Birleştirme (RRF)
```python
def reciprocal_rank_fusion(
    dense_results: list[str],
    sparse_results: list[str],
    k: int = 60
) -> list[str]:
    """Reciprocal Rank Fusion — skor normalize gerektirmez."""
    scores = {}
    
    for rank, doc_id in enumerate(dense_results):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    
    for rank, doc_id in enumerate(sparse_results):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    
    return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
```

### BM25 Kurulumu
```python
from rank_bm25 import BM25Okapi
import nltk

def build_bm25_index(documents: list[str]) -> BM25Okapi:
    tokenized = [nltk.word_tokenize(d.lower()) for d in documents]
    return BM25Okapi(tokenized)

def bm25_search(index: BM25Okapi, query: str, documents: list[str], k: int = 20) -> list[str]:
    tokens = nltk.word_tokenize(query.lower())
    scores = index.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [documents[i] for i in top_indices]
```

### Tam Hibrit Pipeline
```python
def hybrid_search(query: str, top_k: int = 10) -> list[str]:
    # Dense retrieval (semantic)
    q_embed = embed(query)
    dense_results = vector_store.search(q_embed, k=20)
    
    # Sparse retrieval (BM25)
    sparse_results = bm25_search(bm25_index, query, all_docs, k=20)
    
    # Birleştir
    fused = reciprocal_rank_fusion(dense_results, sparse_results)
    
    # Rerank (opsiyonel)
    return reranker.rerank(query, fused[:30])[:top_k]
```

### Qdrant Hibrit Arama
```python
from qdrant_client.models import SparseVector, NamedVector, NamedSparseVector

# Qdrant native sparse+dense hibrit desteği
results = qclient.query_points(
    collection_name="docs",
    prefetch=[
        {"query": dense_vector, "using": "dense", "limit": 20},
        {"query": SparseVector(indices=[...], values=[...]), "using": "sparse", "limit": 20},
    ],
    query={"fusion": "rrf"},
    limit=10
)
```

## Common mistakes
- Ağırlıklı toplam yerine normalize edilmemiş skorları doğrudan toplamak — ölçek farklılığı bias üretir.
- Türkçe için İngilizce tokenizer kullanmak — BM25 kalitesi düşer, nltk Türkçe tokenizer gerekli.
- Hibritten sonra reranking atlamak — birleştirme mükemmel değildir, reranker kaliteyi artırır.
- Her iki kanaldan top-5 alıp birleştirmek — en az top-20 alın sonra fuse edin.

## References
- `skills/llm-context-rag-pipeline`
- `skills/llm-context-reranking`
- `skills/llm-context-vector-store`
