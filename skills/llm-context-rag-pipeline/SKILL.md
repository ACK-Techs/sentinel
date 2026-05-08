---
name: llm-context-rag-pipeline
description: "Retrieval-Augmented Generation pipeline kurmak gerektiğinde; embed→index→retrieve→augment→generate adımlarını ve hata noktalarını yönetmek için kullan"
---

## Purpose
RAG pipeline, modelin bilmediği veya güncel olmayan bilgiyi dış belgeden alıp yanıta entegre etmesini sağlar. Her adımda kalite kaybı olabilir; bu skill kritik kontrol noktalarını tanımlar.

## Workflow

### Pipeline Adımları
```
[1] INGEST    → Belgeleri yükle, temizle, chunk'la
[2] EMBED     → Her chunk'ı vector'e çevir
[3] INDEX     → Vector store'a kaydet
[4] RETRIEVE  → Sorguya benzer chunk'ları getir
[5] RERANK    → Relevance sırasını iyileştir
[6] AUGMENT   → Chunk'ları prompt'a ekle
[7] GENERATE  → LLM yanıt üretir
```

### Minimal RAG Implementasyonu
```python
from anthropic import Anthropic
import chromadb

client = Anthropic()
chroma = chromadb.Client()
collection = chroma.get_or_create_collection("sentinel-docs")

def ingest_document(text: str, doc_id: str, metadata: dict):
    chunks = chunk_text(text, size=500, overlap=50)
    embeddings = embed_batch(chunks)
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{doc_id}-{i}" for i in range(len(chunks))],
        metadatas=[{**metadata, "chunk_idx": i} for i in range(len(chunks))]
    )

def rag_query(question: str, top_k: int = 5) -> str:
    q_embedding = embed(question)
    results = collection.query(query_embeddings=[q_embedding], n_results=top_k)
    
    context = "\n\n---\n\n".join(results["documents"][0])
    
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="Sağlanan belgelerden yanıt ver. Belgede yoksa 'Bu bilgi mevcut belgede yok' de.",
        messages=[{
            "role": "user",
            "content": f"Belgeler:\n{context}\n\nSoru: {question}"
        }]
    )
    return response.content[0].text
```

### Kalite Kontrol Noktaları
```python
# Retrieval kalitesi
def check_retrieval_quality(question: str, retrieved_chunks: list) -> float:
    """LLM ile alaka puanı hesapla"""
    prompt = f"Soru: {question}\n\nBelge: {retrieved_chunks[0]}\n\nAlaka puanı (0-10):"
    score = float(llm.complete(prompt).strip())
    return score

# Hallüsinasyon kontrolü
def check_grounded(answer: str, sources: list[str]) -> bool:
    """Yanıt kaynaklarda destekleniyor mu?"""
    prompt = f"Yanıt: {answer}\nKaynaklar: {sources}\nYanıt yalnızca kaynaklardaki bilgiye dayanıyor mu? (evet/hayır)"
    return "evet" in llm.complete(prompt).lower()
```

## Common mistakes
- Chunk boyutunu optimize etmeden `1000 token` sabit kullanmak — belgeye göre değişir.
- Reranking adımını atlamak — embedding benzerliği = semantic relevance değil.
- Kaynak göstermeden yanıt üretmek — hangi chunk'tan geldiğini takip edin.
- Belge güncelleme politikası olmadan stale index bırakmak.

## References
- `skills/llm-context-chunking-strategy`
- `skills/llm-context-vector-store`
- `skills/llm-context-reranking`
- `skills/llm-eval-ragas`
