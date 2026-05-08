---
name: test-golden-dataset
description: "LLM agent için golden dataset oluşturma; Sentinel alert analiz agent'ı için input/expected output çiftleri, CI değerlendirme pipeline ve regresyon tespiti"
---

## Purpose
Sentinel'in LLM tabanlı agent'larının (alert açıklama, anomali tespiti) kalite regresyonlarını golden dataset üzerinde otomatik ölçmek; yeni model veya prompt değişikliği sonrası kalite kontrolü sağlamak.

## Workflow

### Golden Dataset Yapısı
```json
// tests/golden/alert_analysis_dataset.json
{
  "dataset_version": "1.0.0",
  "description": "Sentinel alert analiz agent golden dataset",
  "examples": [
    {
      "id": "mem-001",
      "input": {
        "alert": {
          "alertname": "HighMemoryUsage",
          "instance": "sentinel-api-pod-3",
          "severity": "warning",
          "value": "87%",
          "labels": {"namespace": "sentinel", "app": "api"}
        },
        "context": {
          "recent_deployments": ["v1.2.3 deployed 2h ago"],
          "related_metrics": {"cpu_usage": "45%", "request_rate": "1200/s"}
        }
      },
      "expected": {
        "root_cause_category": "memory_pressure",
        "confidence": "high",
        "recommendations": ["investigate memory leak", "check heap dumps"],
        "severity_assessment": "warning"
      },
      "evaluation_criteria": {
        "must_mention": ["memory", "leak", "heap"],
        "must_not_mention": ["network", "disk"],
        "expected_category": "memory_pressure"
      }
    }
  ]
}
```

### Golden Dataset Evaluator
```python
# tests/golden/evaluator.py
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class EvalResult:
    example_id: str
    passed: bool
    score: float
    failures: list[str] = field(default_factory=list)

class GoldenDatasetEvaluator:
    def __init__(self, dataset_path: str):
        with open(dataset_path) as f:
            self.dataset = json.load(f)
    
    def evaluate_example(self, example: dict, actual_output: dict) -> EvalResult:
        criteria = example["evaluation_criteria"]
        failures = []
        scores = []
        
        # Kategori kontrolü
        if "expected_category" in criteria:
            if actual_output.get("root_cause_category") == criteria["expected_category"]:
                scores.append(1.0)
            else:
                scores.append(0.0)
                failures.append(
                    f"Kategori yanlış: beklenen={criteria['expected_category']}, "
                    f"alınan={actual_output.get('root_cause_category')}"
                )
        
        # Zorunlu kelimeler
        explanation = actual_output.get("explanation", "").lower()
        for word in criteria.get("must_mention", []):
            if word.lower() in explanation:
                scores.append(1.0)
            else:
                scores.append(0.0)
                failures.append(f"'{word}' açıklamada geçmiyor")
        
        # Yasaklı kelimeler
        for word in criteria.get("must_not_mention", []):
            if word.lower() not in explanation:
                scores.append(1.0)
            else:
                scores.append(0.0)
                failures.append(f"'{word}' açıklamada geçmemeli")
        
        avg_score = sum(scores) / len(scores) if scores else 0.0
        return EvalResult(
            example_id=example["id"],
            passed=avg_score >= 0.8,
            score=avg_score,
            failures=failures
        )
```

### CI Değerlendirme Testi
```python
# tests/golden/test_alert_analyzer_golden.py
import pytest
import json
from sentinel.agents.alert_analyzer import AlertAnalyzer
from tests.golden.evaluator import GoldenDatasetEvaluator

DATASET_PATH = "tests/golden/alert_analysis_dataset.json"
MIN_PASS_RATE = 0.85  # %85 minimum geçme oranı

@pytest.fixture(scope="session")
def evaluator():
    return GoldenDatasetEvaluator(DATASET_PATH)

@pytest.fixture(scope="session")
def analyzer():
    return AlertAnalyzer()

@pytest.mark.asyncio
async def test_golden_dataset_pass_rate(evaluator, analyzer):
    results = []
    
    for example in evaluator.dataset["examples"]:
        output = await analyzer.analyze(example["input"]["alert"])
        result = evaluator.evaluate_example(example, output.__dict__)
        results.append(result)
        
        if not result.passed:
            print(f"BAŞARISIZ [{result.example_id}]: {result.failures}")
    
    pass_rate = sum(1 for r in results if r.passed) / len(results)
    avg_score = sum(r.score for r in results) / len(results)
    
    print(f"\nGeçme oranı: {pass_rate:.1%} | Ortalama skor: {avg_score:.2f}")
    
    assert pass_rate >= MIN_PASS_RATE, (
        f"Golden dataset geçme oranı {pass_rate:.1%} < minimum {MIN_PASS_RATE:.1%}"
    )
```

### Dataset Yönetimi
```bash
# Yeni örnek ekle
python scripts/add_golden_example.py \
  --alert '{"alertname": "DiskFull", "value": "99%"}' \
  --expected-category disk_pressure

# Mevcut agent ile tüm dataset'i yeniden değerlendir
python scripts/regenerate_expected.py --dataset tests/golden/alert_analysis_dataset.json
```

## Common mistakes
- Golden dataset'e çok az örnek koymak — her kategori için en az 3-5 örnek; nadir ama kritik case'ler mutlaka dahil
- Expected output'u çok katı tanımlamak — kelime bazlı eşleşme yerine semantik kategori kontrolü
- Dataset versiyonlamak yerine in-place düzenlemek — `dataset_version` artır ve git tag at
- Sadece mutlu yol örnekleri eklemek — edge case'ler (boş context, unusual alert name) dataset'te temsil edilmeli

## References
- `skills/test-mock-llm`
- `skills/test-snapshot`
