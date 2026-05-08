---
name: llm-local-context-length
description: "Yerel modellerde context window sınırını anlamak, uzun bağlam stratejisi (sliding window, RAG, compaction) seçmek ve büyük context'in VRAM + gecikme etkisini yönetmek gerektiğinde kullan."
---

## Purpose
Yerel modeller çoğunlukla max 8K-128K context ile gelir ama büyük context = daha fazla VRAM + daha yavaş çıkarım. Doğru strateji seçimi performans-kalite dengesini kurar.

## Context sınırını belirleme

### Model bazlı maksimumlar (2025)
| Model | Max Context |
|---|---|
| Llama 3.2 3B/8B | 128K |
| Llama 3.1 70B | 128K |
| Mistral 7B v0.3 | 32K |
| Phi-3 mini | 128K |

Bu değerler teorik maksimum; VRAM kısıtı genellikle daha düşük bir pratik sınır belirler.

### VRAM etkisi
```
KV_cache ≈ context_length × num_layers × 2 × head_dim × dtype_bytes
```
4096 context → ~1 GB; 32K context → ~8 GB (8B model için yaklaşık).

## Uzun context stratejileri

### 1. Sliding window (rolling buffer)
```python
MAX_TOKENS = 6000
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

def add_message(role, content, token_estimate):
    messages.append({"role": role, "content": content})
    while sum(len(m["content"])//4 for m in messages[1:]) > MAX_TOKENS:
        messages.pop(1)  # en eski user/assistant çiftini sil
```

### 2. RAG ile bağlam kısaltma
Uzun doküman → chunk → embed → yalnızca ilgili chunk'ları context'e koy.

### 3. Ollama context yapılandırma
```bash
ollama run llama3.2 --context-length 16384  # CLI
```
Python:
```python
llm = Llama(model_path="...", n_ctx=16384)
```

### 4. vLLM max sequence length
```bash
python -m vllm.entrypoints.openai.api_server \
  --max-model-len 16384  # context window sınırla
```

## Performans ipuçları
- Yüksek context = quadratic attention cost → 8K → 32K geçişi 4x değil 16x yavaşlayabilir.
- Flash Attention ile vLLM: uzun context'te belirgin hızlanma.

## Common mistakes
- Modelin desteklediği max context'i VRAM hesabı olmadan açmak.
- Konuşma geçmişini hiç temizlemeden uzun oturumlarda context'i doldurmak.

## References
- `skills/llm-local-gpu-memory`
- `skills/llm-context-window-management`
- `skills/llm-local-vllm-setup`
