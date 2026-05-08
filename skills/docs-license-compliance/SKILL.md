---
name: docs-license-compliance
description: "Sentinel monoreposunun bağımlılık lisanslarını tarar, uyumluluk raporları üretir ve NOTICE dosyasını yönetir"
---

## Purpose
Sentinel, FastAPI, Prometheus client, OpenTelemetry SDK gibi onlarca açık kaynak bağımlılık kullanır. Bu bağımlılıkların lisansları projenin dağıtım şekliyle uyumlu olmalı. Bu skill, lisans taramasını otomatize eder, uyumsuzluk risklerini işaretler ve zorunlu NOTICE dosyasını günceller.

## Workflow

### 1. Python bağımlılıklarını tara
```bash
# pip-licenses ile tüm bağımlılık lisanslarını listele
pip install pip-licenses
pip-licenses --format=json --output-file=documentations/licenses/python-deps.json

# Sorunlu lisansları işaretle
pip-licenses --fail-on="GPL;LGPL;AGPL" --allow-only="MIT;Apache;BSD;ISC;PSF"
```

### 2. Node/npm bağımlılıkları (CI scripts)
```bash
# license-checker ile tarama
npx license-checker --json --out documentations/licenses/node-deps.json

# Copyleft lisansları engelle
npx license-checker --failOn "GPL-2.0;GPL-3.0;LGPL-2.1;AGPL-3.0"
```

### 3. Docker base image lisansları
```bash
# trivy ile container lisans taraması
trivy image --format json --output documentations/licenses/container-licenses.json \
  sentinel/orders:latest

# Kritik lisans bulgularını filtrele
trivy image --license-full sentinel/orders:latest 2>&1 | grep -E "GPL|AGPL|SSPL"
```

### 4. Lisans uyumluluk matrisi
```markdown
## Onaylanan Lisanslar
| Lisans | Kullanım | Kopyasol | Dağıtım Gereksinimi |
|--------|----------|----------|---------------------|
| MIT | Ticari | Hayır | Lisans metni dahil et |
| Apache 2.0 | Ticari | Hayır | NOTICE dosyası + lisans |
| BSD-2/3 | Ticari | Hayır | Lisans metni dahil et |
| ISC | Ticari | Hayır | Lisans metni |
| GPL-2.0 | Risk | EVET | Kaynak kodu yayınla |
| AGPL-3.0 | Yasak | EVET | SaaS'ta da yayın zorunlu |
```

### 5. NOTICE dosyası üretimi
```python
# scripts/generate_notice.py
import json

deps = json.load(open("documentations/licenses/python-deps.json"))
notice_lines = [
    "Sentinel - Observability Platform Test Tool",
    "Copyright 2024 Sentinel Contributors",
    "Licensed under Apache License 2.0",
    "",
    "This product includes software developed by:",
    ""
]

for dep in sorted(deps, key=lambda x: x["Name"]):
    notice_lines.append(f"  {dep['Name']} {dep['Version']}")
    notice_lines.append(f"  License: {dep['License']}")
    if dep.get('URL'):
        notice_lines.append(f"  URL: {dep['URL']}")
    notice_lines.append("")

with open("NOTICE", "w") as f:
    f.write("\n".join(notice_lines))
```

### 6. CI entegrasyonu
```yaml
# .github/workflows/license-check.yml
name: License Compliance
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check Python licenses
        run: |
          pip install pip-licenses
          pip install -r requirements.txt
          pip-licenses --fail-on="GPL;AGPL" --allow-only="MIT;Apache;BSD;ISC;PSF;Python"
      - name: Update NOTICE
        run: python scripts/generate_notice.py
      - name: Verify NOTICE committed
        run: git diff --exit-code NOTICE
```

## Common mistakes
1. Lisans taramasını yalnızca doğrudan bağımlılıklara uygulamak — transitif bağımlılıklar da taranmalı.
2. LGPL bağımlılığını "safe" saymak — dynamic linking kuralları karmaşık, hukuki danışman gerekebilir.
3. NOTICE dosyasını elle güncellemek — yeni bağımlılık eklenince unutulur, otomatize et.
4. Lisans bulgusunu "later" olarak işaretleyip commit'e devam etmek — CI'da blocking olmalı.

## References
- `skills/docs-security-policy`
- `skills/ci-pr-gate`
