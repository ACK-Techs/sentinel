---
name: test-coverage-reporting
description: "pytest-cov ile Sentinel coverage raporu; minimum eşik zorunluluğu, branch coverage, XML/HTML rapor ve CI'da coverage badge güncelleme"
---

## Purpose
Sentinel codebase'inin test kapsama oranını ölçmek, kritik modüller için minimum eşikler belirlemek ve CI'da otomatik kontrol sağlamak.

## Workflow

### pytest-cov Çalıştırma
```bash
# Terminal raporu + minimum eşik
pytest tests/ \
  --cov=sentinel \
  --cov-report=term-missing \
  --cov-report=html:htmlcov/ \
  --cov-report=xml:coverage.xml \
  --cov-fail-under=80

# Branch coverage (if/else dalları)
pytest tests/ --cov=sentinel --cov-branch --cov-fail-under=75
```

### pyproject.toml Konfigürasyonu
```toml
[tool.coverage.run]
source = ["sentinel"]
branch = true
omit = [
    "*/tests/*",
    "*/migrations/*",
    "sentinel/cli/__main__.py",  # entry point, manual test yeterli
    "sentinel/dev_tools.py",     # geliştirici araçları
]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "@overload",
]

[tool.coverage.paths]
source = ["sentinel", "*/site-packages/sentinel"]
```

### Modül Bazlı Minimum Eşikler
```python
# scripts/check_coverage_by_module.py
import json
import sys

MINIMUM_COVERAGE = {
    "sentinel/validators.py": 95,
    "sentinel/alert_rules.py": 90,
    "sentinel/clients/": 80,
    "sentinel/models/": 85,
    "sentinel/agents/": 70,  # LLM tabanlı, test zor
}

def check(coverage_json: str):
    with open(coverage_json) as f:
        data = json.load(f)
    
    failures = []
    for file_path, min_pct in MINIMUM_COVERAGE.items():
        for fname, fdata in data["files"].items():
            if file_path in fname:
                actual = fdata["summary"]["percent_covered"]
                if actual < min_pct:
                    failures.append(
                        f"{fname}: {actual:.1f}% < minimum {min_pct}%"
                    )
    
    if failures:
        print("Coverage eşik hatası:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print("Tüm coverage eşikleri geçildi")

if __name__ == "__main__":
    check(sys.argv[1])
```

### CI Konfigürasyonu
```yaml
# .github/workflows/test.yml
- name: Test with coverage
  run: |
    pytest tests/ \
      --cov=sentinel \
      --cov-report=xml:coverage.xml \
      --cov-report=term-missing \
      --cov-fail-under=80

- name: Module coverage check
  run: python scripts/check_coverage_by_module.py coverage.xml

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: coverage.xml
    fail_ci_if_error: true
```

### Coverage Raporu Yorumlama
```
Name                          Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------
sentinel/validators.py           45      2      18      1    95%
sentinel/alert_rules.py          89     12      32      4    87%
sentinel/clients/prometheus.py   67      8      24      3    89%
sentinel/agents/analyzer.py     134     41      46     12    69%
---------------------------------------------------------------
TOTAL                           335     63     120     20    81%
```

```bash
# Eksik satırları detaylı gör
coverage report --show-missing --include="sentinel/validators.py"
# validators.py: 45 stmts, 2 miss, 95% covered
# Missing: 34, 67
```

## Common mistakes
- `omit` olmadan coverage ölçmek — migrations, test dosyaları, entry point'ler yanlış düşük oran gösterir
- Line coverage yüksek ama branch coverage düşük olmak — `--cov-branch` ile if/else dallarını da ölç
- Coverage'ı tek bir sayıda değerlendirmek — kritik modüller için ayrı minimum eşik belirle
- `# pragma: no cover` kötüye kullanmak — sadece gerçekten test edilemez kod için (platform-specific, debug only)

## References
- `skills/test-mutation`
- `skills/test-matrix-tox`
