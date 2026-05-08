---
name: llm-prompt-react-pattern
description: "LLM'in Reason→Act→Observe döngüsüyle araç çağrısı yapması gerektiğinde; Sentinel ajan döngüsünde tool use akışını yönetirken kullan"
---

## Purpose
ReAct (Reason + Act), modelin önce düşünmesini (Thought), sonra araç çağırmasını (Action), ardından sonucu gözlemlemesini (Observation) sağlayan döngüsel bir promptlama desenidir. Sentinel'in ajan döngüsü bu pattern üzerine kuruludur.

## Workflow

### ReAct Prompt Yapısı
```
Bir araç setine erişimin var. Her adımda şu formatı kullan:

Thought: [Ne yapman gerektiğini düşün]
Action: tool_name({"param": "value"})
Observation: [Araç çıktısı buraya gelecek]
... (döngü devam eder)
Final Answer: [Kullanıcıya nihai yanıt]
```

### Sentinel Araç Döngüsü
```python
def react_loop(user_message: str, tools: list, max_steps: int = 10):
    messages = [{"role": "user", "content": user_message}]
    
    for step in range(max_steps):
        response = llm.complete(messages=messages, tools=tools)
        
        if response.stop_reason == "end_turn":
            return response.text
        
        if response.stop_reason == "tool_use":
            for tool_call in response.tool_calls:
                result = execute_tool(tool_call.name, tool_call.params)
                messages.append({
                    "role": "tool",
                    "tool_use_id": tool_call.id,
                    "content": str(result)
                })
    
    raise MaxStepsExceeded(f"{max_steps} adım aşıldı")
```

### Action Format Kontrolü
```python
import re

ACTION_PATTERN = re.compile(
    r"Action:\s*(\w+)\((\{.*?\})\)",
    re.DOTALL
)

def parse_action(text: str):
    m = ACTION_PATTERN.search(text)
    if not m:
        raise ValueError(f"Geçersiz Action formatı: {text[:100]}")
    tool_name = m.group(1)
    params = json.loads(m.group(2))
    return tool_name, params
```

## Common mistakes
- Sonsuz döngüyü önlemek için `max_steps` koymamak.
- Observation'ı prompt'a geri beslememek — model önceki araç sonuçlarını göremez.
- Araç hatasını Observation olarak değil exception olarak yönetmek — hata da observation'dır, modele bildirin.
- Thought bloğunu kullanıcıya göstermek — üretimde filtreleyin.

## References
- `skills/llm-prompt-tool-descriptions`
- `skills/llm-prompt-chain-of-thought`
- `skills/llm-eval-tool-call-accuracy`
