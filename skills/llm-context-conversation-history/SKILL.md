---
name: llm-context-conversation-history
description: "Çok turlu konuşmada geçmişi yönetmek, mesaj kısaltmak ve bağlamı taşımak gerektiğinde; özellikle Sentinel session persistence ile birlikte kullan"
---

## Purpose
Konuşma geçmişi yönetimi, modelin tutarlı davranması için gerekli bağlamı aktarırken token bütçesini aşmamayı hedefler. Yanlış yönetim ya context overflow ya da bağlam kaybına yol açar.

## Workflow

### Mesaj Deposu Yapısı
```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Message:
    role: Literal["user", "assistant", "system", "tool"]
    content: str
    turn_id: int
    timestamp: float
    tokens: int = 0
    is_compacted: bool = False

@dataclass
class ConversationHistory:
    messages: list[Message] = field(default_factory=list)
    max_tokens: int = 100_000
    
    def add(self, role: str, content: str) -> Message:
        msg = Message(
            role=role,
            content=content,
            turn_id=len(self.messages),
            timestamp=time.time(),
            tokens=estimate_tokens(content)
        )
        self.messages.append(msg)
        self._auto_trim()
        return msg
    
    def _auto_trim(self):
        total = sum(m.tokens for m in self.messages)
        while total > self.max_tokens * 0.9:
            # İlk compactable mesajı özetle
            self._compact_oldest()
            total = sum(m.tokens for m in self.messages)
```

### Kısaltma Stratejileri
```python
# 1. Silme: en eski kullanıcı/asistan mesajlarını sil
def drop_oldest(messages, n=2):
    # System mesajları ve araç çağrıları koru
    droppable = [m for m in messages if m.role in ("user", "assistant") and not m.is_compacted]
    for m in droppable[:n]:
        messages.remove(m)

# 2. Özetleme: eski konuşmayı tek mesaja dönüştür
def summarize_to_single(messages: list[Message]) -> Message:
    text = "\n".join(f"{m.role}: {m.content}" for m in messages)
    summary = llm.complete(f"Bu konuşmayı 100 kelimede özetle:\n{text}")
    return Message(role="system", content=f"[Geçmiş özeti]\n{summary}", 
                   turn_id=0, timestamp=time.time(), is_compacted=True)
```

### Sentinel ile Oturum Sürekliliği
```python
# Oturumlar arası geçmişi kaydet/yükle
def save_history(history: ConversationHistory, path: Path):
    data = [{"role": m.role, "content": m.content, "turn_id": m.turn_id}
            for m in history.messages]
    path.write_text(json.dumps(data, ensure_ascii=False))

def load_history(path: Path) -> ConversationHistory:
    data = json.loads(path.read_text())
    h = ConversationHistory()
    h.messages = [Message(**d, timestamp=0, tokens=estimate_tokens(d["content"])) 
                  for d in data]
    return h
```

## Common mistakes
- Tool mesajlarını özetlemek — tool_use_id bağlantısı kopar, API hata verir.
- Geçmişi yalnızca RAM'de tutmak — process restart'ta tüm konuşma kaybolur.
- Sistem mesajı sırasını değiştirmek — bazı modeller system mesajını en başta bekler.
- Tarih sıralamasını korumadan mesaj eklemek — model sıra bozukluğunda yanıltılır.

## References
- `skills/llm-context-window-management`
- `skills/llm-context-semantic-compaction`
- `skills/agentic-memory-extract-pipeline`
