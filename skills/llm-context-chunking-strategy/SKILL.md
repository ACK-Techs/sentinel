---
name: llm-context-chunking-strategy
description: "RAG için belgeleri parçalara bölerken; chunk boyutu, overlap ve bölme stratejisini belge türüne göre seçmek için kullan"
---

## Purpose
Chunking, retrieval kalitesini belirleyen kritik adımdır. Çok büyük chunk'lar irrelevant bilgi taşır; çok küçük chunk'lar bağlamı kaybeder. Bu skill, belge türüne göre doğru stratejiyi seçer.

## Workflow

### Strateji Seçimi
```
Belge Türü          | Yöntem              | Boyut     | Overlap
--------------------|---------------------|-----------|--------
Düz metin           | Fixed-size          | 512 token | 50-100
Teknik dok          | Semantic (başlık)   | 400-800   | 50
Kod                 | Fonksiyon bazlı     | değişken  | 0
HTML/Markdown       | Başlık hiyerarşisi  | değişken  | 0
Sözleşme/hukuki     | Madde bazlı         | değişken  | tam madde
```

### Fixed-Size Chunking
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_text(document)
```

### Semantic Chunking (Başlık Bazlı)
```python
import re

def chunk_by_headers(markdown_text: str) -> list[dict]:
    """Markdown başlıklarına göre chunk oluştur."""
    sections = re.split(r'\n(#{1,3} .+)\n', markdown_text)
    chunks = []
    current_header = "Giriş"
    
    for i, section in enumerate(sections):
        if section.startswith('#'):
            current_header = section.strip()
        else:
            if section.strip():
                chunks.append({
                    "header": current_header,
                    "content": section.strip(),
                    "tokens": estimate_tokens(section)
                })
    return chunks
```

### Kod Chunking (Fonksiyon Bazlı)
```python
import ast

def chunk_python_file(source: str) -> list[dict]:
    """Python kaynak kodunu fonksiyon/sınıf bazlı böl."""
    tree = ast.parse(source)
    chunks = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = node.end_lineno
            lines = source.split('\n')[start:end]
            chunks.append({
                "type": type(node).__name__,
                "name": node.name,
                "content": '\n'.join(lines)
            })
    return chunks
```

### Chunk Kalite Testi
```python
def test_chunk_quality(chunks: list[str], test_queries: list[str]) -> float:
    """Test sorgular için hit@5 hesapla."""
    hits = 0
    for query in test_queries:
        results = retrieve(query, chunks, k=5)
        if any(is_relevant(r, query) for r in results):
            hits += 1
    return hits / len(test_queries)
```

## Common mistakes
- Tüm belgeler için aynı chunk boyutu kullanmak — kod ve roman aynı strateji gerektirmez.
- Overlap olmadan chunk'lamak — cümle başında kesilen bilgi kaybolur.
- Chunk'ları metadata olmadan saklamak — kaynak takibi imkansızlaşır.
- Çok küçük chunk'lar üretmek (< 100 token) — embedding anlamsızlaşır.

## References
- `skills/llm-context-rag-pipeline`
- `skills/llm-context-vector-store`
