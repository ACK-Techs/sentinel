---
name: llm-context-semantic-compaction
description: "Sentinel semantic compaction ile oturum belleğini kalıcı hale getirmek, context dolulukta otomatik özetleme tetiklemek için kullan"
---

## Purpose
Semantic compaction, uzun konuşmalarda context window'u aşmadan oturum bilgisini korumayı sağlar. Sentinel bunu post-turn hook olarak çalıştırır: belirlenen eşiğe ulaşınca mevcut context'i LLM ile özetleyip index.md'ye yazar.

## Workflow

### Compaction Tetikleme Koşulları
```yaml
# sentinel.yaml
memory:
  semantic_compaction:
    enabled: true
    trigger_at_pct: 75        # context %75 dolduğunda tetikle
    min_turns_before_compact: 5
    preserve_last_n_turns: 4
    summary_max_tokens: 2000
```

### Compaction Pipeline
```python
def run_semantic_compaction(session: Session) -> str:
    """Mevcut context'i özetleyip döndür."""
    
    # Korunacak son N turu ayır
    protected_turns = session.messages[-session.config.preserve_last_n_turns:]
    compactable = session.messages[:-session.config.preserve_last_n_turns]
    
    if not compactable:
        return ""
    
    # LLM ile özetle
    summary_prompt = f"""Bu konuşma geçmişini kompakt bir özete dönüştür.
Şunları koru:
- Alınan kararlar ve gerekçeleri
- Çözülen ve çözülemeyen sorunlar
- Kullanıcının tercihleri ve kısıtlamaları
- Devam eden görevler

Konuşma:
{format_turns(compactable)}"""

    summary = llm.complete(summary_prompt, max_tokens=2000)
    
    # Oturum mesajlarını güncelle
    session.messages = [
        {"role": "system", "content": f"[Önceki konuşma özeti]\n{summary}"},
        *protected_turns
    ]
    
    return summary
```

### Belleğe Yazma
```python
def persist_compaction(summary: str, session_id: str, memory_dir: Path):
    """Özeti bellek deposuna yaz."""
    ts = datetime.utcnow().isoformat()
    entry = {
        "session_id": session_id,
        "compacted_at": ts,
        "summary": summary
    }
    
    memory_file = memory_dir / f"compact_{session_id}_{ts[:10]}.json"
    memory_file.write_text(json.dumps(entry, ensure_ascii=False, indent=2))
    
    # index.md güncelle
    update_memory_index(memory_dir, session_id, summary[:200])
```

### Compaction Kalitesi Kontrolü
```python
# Özetleme sonrası test sorusu
def verify_compaction(summary: str, original_key_facts: list[str]) -> float:
    """Kritik bilgilerin özette korunduğunu kontrol et."""
    hits = sum(1 for fact in original_key_facts if fact.lower() in summary.lower())
    return hits / len(original_key_facts)
```

## Common mistakes
- Compaction'ı çok erken tetiklemek (%50'de) — gerekli bağlam henüz oluşmamış olabilir.
- Son N turu korumadan tüm context'i özetlemek — araç çağrı döngüsü kesilebilir.
- Özeti system mesajına değil user mesajına koymak — model sistematik olarak görmez.
- Lock dosyası olmadan concurrent compaction yapmak — çakışan yazımlar index bozar.

## References
- `skills/llm-context-conversation-history`
- `skills/llm-context-window-management`
- `skills/agentic-memory-extract-pipeline`
- `documantations/INTEGRATION_SENTINEL_CLI_FROM_CLI_CLAUDE.md`
