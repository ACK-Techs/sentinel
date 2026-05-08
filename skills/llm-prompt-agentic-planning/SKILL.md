---
name: llm-prompt-agentic-planning
description: "LLM'den karmaşık görevi alt görevlere bölmesi, bağımlılık sırası belirlemesi ve yürütme planı üretmesi gerektiğinde kullan"
---

## Purpose
Agentic planning, LLM'in bir hedefi analiz edip bağımsız alt görevlere decompose etmesini ve bu görevler arasındaki bağımlılıkları belirlemesini sağlar. Sentinel'de multi-step ajan görevlerinde ilk adımdır.

## Workflow

### Planlama Promptu
```python
PLANNING_PROMPT = """Aşağıdaki görevi analiz et ve bir yürütme planı üret.

GÖREV: {task}

Mevcut araçlar:
{tools_summary}

Plan formatı:
```json
{{
  "goal": "Ana hedef tek cümle",
  "steps": [
    {{
      "id": "step_1",
      "action": "Ne yapılacak",
      "tool": "kullanılacak_araç veya null",
      "depends_on": [],
      "output": "Bu adımın çıktısı"
    }},
    {{
      "id": "step_2",
      "depends_on": ["step_1"],
      ...
    }}
  ],
  "risks": ["Potansiyel başarısızlık senaryoları"]
}}
```"""
```

### Plan Yürütücü
```python
import json
from collections import defaultdict

def execute_plan(plan: dict, agent) -> dict:
    steps = {s["id"]: s for s in plan["steps"]}
    completed = {}
    
    def can_run(step):
        return all(dep in completed for dep in step["depends_on"])
    
    pending = list(steps.values())
    while pending:
        runnable = [s for s in pending if can_run(s)]
        if not runnable:
            raise CircularDependency("Bağımlılık döngüsü tespit edildi")
        
        for step in runnable:
            result = agent.execute_step(step, context=completed)
            completed[step["id"]] = result
            pending.remove(step)
    
    return completed
```

### Plan Doğrulama
```python
def validate_plan(plan: dict) -> list[str]:
    errors = []
    step_ids = {s["id"] for s in plan["steps"]}
    
    for step in plan["steps"]:
        for dep in step.get("depends_on", []):
            if dep not in step_ids:
                errors.append(f"Geçersiz bağımlılık: {step['id']} -> {dep}")
    
    # DAG döngü kontrolü
    # ... topological sort
    return errors
```

## Common mistakes
- Planı sabit kodlamak — LLM'e dinamik plan ürettirin ki araç değişikliklerine adapte olsun.
- Bağımlılıkları belirtmeden sıralı liste almak — paralel çalıştırılabilir adımlar kaybolur.
- Maksimum adım sınırı koymamak — çok granüler planlar inefficient çalışır.
- Planı doğrulamadan yürütmeye geçmek — döngüsel bağımlılık çıkmazına girer.

## References
- `skills/llm-prompt-react-pattern`
- `skills/llm-prompt-tool-descriptions`
- `skills/llm-prompt-chain-of-thought`
