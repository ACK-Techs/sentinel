---
name: llm-openai-embeddings
description: "OpenAI Embeddings API ile metin vektörü üretmek, boyut seçimi yapmak ve RAG pipeline için vektör index oluşturmak gerektiğinde kullan."
---

## Purpose
Embedding, metni sayısal vektöre dönüştürür; anlam benzerliği hesaplama ve RAG (Retrieval-Augmented Generation) sistemlerinin temel bileşenidir.

## Embedding üretme
```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=["Prometheus nedir?", "Grafana dashboard nasıl oluşturulur?"],
    encoding_format="float"  # veya "base64" (bant genişliği tasarrufu)
)

# İlk metnin vektörü:
vector = response.data[0].embedding  # 1536 elemanlı liste
print(f"Boyut: {len(vector)}")
print(f"Kullanılan token: {response.usage.total_tokens}")
```

## Model karşılaştırması

| Model | Boyut | Maliyet | Kalite |
|---|---|---|---|
| `text-embedding-3-small` | 1536 | Düşük | İyi |
| `text-embedding-3-large` | 3072 | Orta | Yüksek |
| `text-embedding-ada-002` | 1536 | Orta | Eski nesil |

## Boyut küçültme
```python
# text-embedding-3-* modelleri boyut küçültmeyi destekler:
response = client.embeddings.create(
    model="text-embedding-3-large",
    input=["metin"],
    dimensions=512  # 3072'den 512'ye düşür, maliyet azalır
)
```

## Basit benzerlik hesabı
```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query_vec = get_embedding("Loki'de log sorgulama")
doc_vecs  = [get_embedding(doc) for doc in documents]
scores    = [cosine_similarity(query_vec, dv) for dv in doc_vecs]
top_docs  = sorted(zip(scores, documents), reverse=True)[:3]
```

## Üretim önerileri
- Batch embed: `input` listesi ile birden fazla metni tek API çağrısında gönder.
- Vektörleri normalize et (norm=1) — cosine similarity = dot product olur, hesaplama hızlanır.

## Common mistakes
- Modeli değiştirince mevcut vektörleri geçersiz saymayı unutmak — yeni model farklı uzay kullanır.
- Çok uzun metni tek seferde embedding'e sokmak — token limiti aşılır.

## References
- `skills/llm-openai-chat-completion`
- `skills/llm-context-rag-pipeline`
- `skills/llm-context-vector-store`
