---
name: llm-context-window-management
description: "Context window dolmaya yaklaştığında hangi mesajların atılacağına, nasıl kısaltılacağına karar vermek ve rolling buffer uygulamak için kullan"
---

## Purpose
Context window limitine ulaşınca en eski mesajları kesmek en kötü stratejidir — kritik sistem promptu veya önemli bağlam kaybolabilir. Bu skill, öncelik tabanlı context yönetimi ve rolling buffer uygulamasını kapsar.

## Workflow

### Context Öncelik Sırası (Koruma Altında)
```
1. System prompt         → asla kesilmez
2. Task instructions     → korunur
3. Recent N turns        → son 4-6 tur korunur
4. Tool results          → özetlenebilir
5. Orta yaştaki dialog   → silinebilir / özetlenebilir
```

### Token Sayım ve Bütçe
```python
def estimate_tokens(text: str) -> int:
    """Yaklaşık: 1 token ≈ 4 karakter (İngilizce), ≈ 2.5-3 karakter (Türkçe)"""
    return len(text) // 3

def get_context_budget(model: str) -> dict:
    LIMITS = {
        "claude-sonnet-4-5": 200_000,
        "gpt-4o": 128_000,
        "gemma3:4b": 8_192,
    }
    total = LIMITS.get(model, 8_192)
    return {
        "total": total,
        "for_history": int(total * 0.6),
        "for_response": int(total * 0.25),
        "for_system": int(total * 0.15),
    }
```

### Rolling Buffer Implementasyonu
```python
def trim_messages(
    messages: list[dict],
    system_prompt: str,
    max_tokens: int,
    keep_last_n: int = 6
) -> list[dict]:
    system_tokens = estimate_tokens(system_prompt)
    available = max_tokens - system_tokens - 2000  # response reserve
    
    # Son N turu her zaman koru
    protected = messages[-keep_last_n:]
    cuttable = messages[:-keep_last_n]
    
    # Korunmayan mesajları özetle
    if cuttable:
        summary = summarize_history(cuttable)
        protected = [{"role": "system", "content": f"[Önceki konuşma özeti]\n{summary}"}] + protected
    
    return protected
```

### Token Sayımı Uyarısı
```python
WARN_THRESHOLD = 0.85  # %85 dolulukta uyar

def check_context_usage(messages, model):
    used = sum(estimate_tokens(m["content"]) for m in messages)
    budget = get_context_budget(model)["for_history"]
    ratio = used / budget
    if ratio > WARN_THRESHOLD:
        logger.warning(f"Context %{ratio*100:.0f} dolu — trim yapılacak")
    return ratio
```

## Common mistakes
- En eski mesajları basitçe keserek başlamak — tool call result'ları aynı tur içinde kesilirse hata.
- System promptu token sayımına dahil etmemek — gerçek available space yanlış hesaplanır.
- Özetleme yapmadan silmek — konuşma bağlamı kaybolur, model tutarsız yanıt verir.
- Trim sıklığını her tur yerine limit aşıldığında yaparak geç kalmak.

## References
- `skills/llm-context-conversation-history`
- `skills/llm-context-semantic-compaction`
- `skills/llm-prompt-summarization`
