---
name: llm-context-vector-store
description: "RAG için vector store seçilecek ve yönetilecekken; ChromaDB, pgvector, Qdrant arasındaki farklar ve Sentinel entegrasyonu için kullan"
---

## Purpose
Vector store seçimi; ölçek, deployment ortamı ve query latency gereksinimlerine göre değişir. Yanlış seçim ya overkill ya da production'da bottleneck üretir.

## Workflow

### Seçim Kriterleri
```
Kullanım              | Tavsiye
----------------------|------------------
Prototip / yerel dev  | ChromaDB (in-memory)
Production, Postgres  | pgvector
Yüksek ölçek (10M+)  | Qdrant
Bulut-managed         | Pinecone / Weaviate
```

### ChromaDB (Prototip)
```python
import chromadb
from chromadb.utils import embedding_functions

# In-memory (test)
client = chromadb.Client()

# Persistent (dev)
client = chromadb.PersistentClient(path="/data/chroma")

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_or_create_collection("docs", embedding_function=ef)

collection.add(documents=["..."], ids=["doc1"])
results = collection.query(query_texts=["soru"], n_results=5)
```

### pgvector (Production, Postgres)
```sql
-- Kurulum
CREATE EXTENSION IF NOT EXISTS vector;

-- Tablo
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding vector(1536)  -- OpenAI text-embedding-3-small
);

-- Index
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Arama
SELECT content, 1 - (embedding <=> '[...]'::vector) AS similarity
FROM embeddings
ORDER BY embedding <=> '[...]'::vector
LIMIT 5;
```

### Qdrant (Yüksek Ölçek)
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

qclient = QdrantClient(url="http://localhost:6333")
qclient.create_collection(
    "sentinel-docs",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

qclient.upsert("sentinel-docs", points=[
    PointStruct(id=1, vector=[...], payload={"text": "...", "source": "doc.pdf"})
])

hits = qclient.search("sentinel-docs", query_vector=[...], limit=10)
```

### Metadata Filtreleme
```python
# Kategori filtreli arama
results = collection.query(
    query_texts=["teknik sorun"],
    where={"category": "technical", "language": "tr"},
    n_results=5
)
```

## Common mistakes
- ChromaDB'yi production'da kullanmak — concurrent write desteği zayıf.
- pgvector'de index oluşturmadan sorgu yapmak — table scan, çok yavaş.
- Embedding modelini sonradan değiştirmek — tüm index yeniden oluşturulmalı.
- Vektör boyutunu (dimension) modele göre ayarlamamak — hata verir.

## References
- `skills/llm-context-rag-pipeline`
- `skills/llm-context-chunking-strategy`
- `skills/llm-context-hybrid-search`
