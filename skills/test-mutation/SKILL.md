---
name: test-mutation
description: "Muttest/mutmut ile Python mutasyon testi; test suite kalite ölçümü, mutation score hesaplama ve Sentinel kritik modüllerinde hayatta kalan mutant analizi"
---

## Purpose
Test suite'inin gerçekten hataları yakaladığını doğrulamak; kod mutasyonları (operatör değişimi, sabit değer değişimi) sonrası testlerin başarısız olup olmadığını ölçmek.

## Workflow

### mutmut ile Temel Kullanım
```bash
# Tüm modülü tara
mutmut run --paths-to-mutate sentinel/validators.py \
           --tests-dir tests/unit/ \
           --runner "pytest tests/unit/ -x -q"

# Özet görüntüle
mutmut results

# Hayatta kalan mutantları listele
mutmut show
```

### Örnek Mutasyon Hedefi
```python
# sentinel/validators.py — mutasyon testi için kritik modül
def validate_duration(value: str) -> bool:
    """Prometheus süre formatı doğrulama: 5m, 1h, 30s"""
    import re
    return bool(re.match(r'^\d+[smhd]$', value))

def is_above_threshold(value: float, threshold: float) -> bool:
    return value > threshold  # mutant: > → >= veya < veya ==

def calculate_error_rate(errors: int, total: int) -> float:
    if total == 0:
        return 0.0
    return errors / total  # mutant: / → * veya +
```

### Mutantları Öldüren Test Suite
```python
# tests/unit/test_validators.py
import pytest
from sentinel.validators import validate_duration, is_above_threshold, calculate_error_rate

# Sınır değer testleri mutantları öldürür
class TestIsAboveThreshold:
    def test_strictly_above(self):
        assert is_above_threshold(1.0, 0.9) is True
    
    def test_equal_is_not_above(self):
        # > mutant >= olursa bu test başarısız olur → mutant ölür
        assert is_above_threshold(0.9, 0.9) is False
    
    def test_below(self):
        assert is_above_threshold(0.5, 0.9) is False

class TestCalculateErrorRate:
    def test_normal_calculation(self):
        assert calculate_error_rate(10, 100) == pytest.approx(0.1)
    
    def test_zero_errors(self):
        # errors/total mutantı * ile değişirse farklı sonuç verir
        assert calculate_error_rate(0, 100) == pytest.approx(0.0)
    
    def test_division_by_zero(self):
        assert calculate_error_rate(5, 0) == pytest.approx(0.0)
    
    def test_all_errors(self):
        assert calculate_error_rate(100, 100) == pytest.approx(1.0)
```

### CI Entegrasyonu ve Mutation Score Eşiği
```yaml
# .github/workflows/mutation.yml
- name: Mutation test
  run: |
    mutmut run \
      --paths-to-mutate sentinel/validators.py,sentinel/alert_rules.py \
      --tests-dir tests/unit/ \
      --runner "pytest tests/unit/ -x -q --tb=no"
    
    # Mutation score kontrolü
    python scripts/check_mutation_score.py --min-score 85
```

```python
# scripts/check_mutation_score.py
import subprocess
import sys
import re
import argparse

def get_mutation_score() -> float:
    result = subprocess.run(["mutmut", "results"], capture_output=True, text=True)
    # "Killed: 85 out of 100" formatından score çıkar
    match = re.search(r'Killed:\s+(\d+)\s+out of\s+(\d+)', result.stdout)
    if not match:
        return 0.0
    killed, total = int(match.group(1)), int(match.group(2))
    return (killed / total * 100) if total > 0 else 0.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-score", type=float, default=80.0)
    args = parser.parse_args()
    
    score = get_mutation_score()
    print(f"Mutation score: {score:.1f}%")
    
    if score < args.min_score:
        print(f"BAŞARISIZ: {score:.1f}% < minimum {args.min_score}%")
        sys.exit(1)
    print(f"GEÇTI: {score:.1f}% >= {args.min_score}%")
```

### Hayatta Kalan Mutant İnceleme
```bash
# Belirli mutantı göster
mutmut show 5

# diff formatında göster
mutmut show 5 --diff

# Mutantı manuel test et
mutmut apply 5
pytest tests/unit/ -v
mutmut unapply
```

## Common mistakes
- Tüm codebase'e mutasyon uygulamak — çok yavaş; kritik iş mantığı dosyalarını hedefle
- Sadece coverage yüksek olanı mutasyon testi sanmak — %100 coverage ile hayatta kalan mutant sayısı yüksek olabilir
- Mutation score'u %100 hedeflemek — getiri azalan noktada pratik değil; %80-90 makul
- `assert True` veya boş testlerle coverage şişirmek — mutasyon testi bu hileci testleri ortaya çıkarır

## References
- `skills/test-coverage-reporting`
- `skills/test-property-based`
