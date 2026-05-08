---
name: test-snapshot
description: "Pytest snapshot testi (syrupy) ile Sentinel CLI çıktısı ve API yanıt regresyon kontrolü; snapshot güncelleme iş akışı ve CI entegrasyonu"
---

## Purpose
CLI çıktısı veya API yanıtı gibi karmaşık string/dict çıktıların beklenmeyen şekilde değişmediğini snapshot testlerle tespit etmek; ilk koşumda snapshot oluştur, sonraki koşumlarda karşılaştır.

## Workflow

### Kurulum
```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--snapshot-update"  # sadece snapshot oluştururken ekle, sonra kaldır

[project.optional-dependencies]
test = ["syrupy>=4.0"]
```

### CLI Çıktısı Snapshot Testi
```python
# tests/snapshot/test_cli_output.py
import subprocess
import pytest
from syrupy.assertion import SnapshotAssertion

def run_sentinel(*args) -> str:
    result = subprocess.run(
        ["python", "-m", "sentinel.cli", *args],
        capture_output=True, text=True, env={"TEST_MODE": "1"}
    )
    return result.stdout.strip()

def test_version_output_snapshot(snapshot: SnapshotAssertion):
    output = run_sentinel("--version")
    # İlk çalıştırmada snapshot oluşturur, sonrakinde karşılaştırır
    assert output == snapshot

def test_help_output_snapshot(snapshot: SnapshotAssertion):
    output = run_sentinel("--help")
    assert output == snapshot

def test_config_validate_output_snapshot(snapshot: SnapshotAssertion, sample_config):
    output = run_sentinel("config", "validate", "--config", str(sample_config))
    assert output == snapshot
```

### API Yanıt Snapshot Testi
```python
# tests/snapshot/test_api_responses.py
import pytest
from httpx import AsyncClient, ASGITransport
from sentinel.app import create_app
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.json import JSONSnapshotExtension

@pytest.fixture
def snapshot(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension)

@pytest.mark.asyncio
async def test_metrics_response_structure_snapshot(snapshot: SnapshotAssertion):
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/metrics", params={"query": "up"})
    
    data = response.json()
    # Timestamp gibi değişken alanları çıkar
    data.pop("timestamp", None)
    if "data" in data and "result" in data["data"]:
        for r in data["data"]["result"]:
            if "value" in r:
                r["value"][0] = "<timestamp>"
    
    assert data == snapshot

def test_error_response_structure_snapshot(snapshot: SnapshotAssertion):
    # Hata yanıt formatı değişmesin
    error = {
        "detail": "Sorgu geçersiz",
        "code": "INVALID_QUERY",
        "status": 422
    }
    assert error == snapshot
```

### Snapshot Dizin Yapısı
```
tests/
└── snapshot/
    ├── test_cli_output.py
    ├── test_api_responses.py
    └── __snapshots__/
        ├── test_cli_output/
        │   ├── test_version_output_snapshot.ambr
        │   └── test_help_output_snapshot.ambr
        └── test_api_responses/
            └── test_metrics_response_structure_snapshot.json
```

### Snapshot Güncelleme İş Akışı
```bash
# Kasıtlı değişiklik sonrası snapshot'ları güncelle
pytest tests/snapshot/ --snapshot-update

# Değişen snapshot'ları kontrol et
git diff tests/snapshot/__snapshots__/

# CI'da snapshot uyuşmazlığı başarısız sayılır
pytest tests/snapshot/ --tb=short
# Output: AssertionError: snapshot does not match
```

### .ambr Snapshot Formatı Örneği
```
# serializer version: 1
# name: test_version_output_snapshot
  '''
  sentinel version 1.2.0
  '''
```

## Common mistakes
- Timestamp, request ID gibi değişken alanları snapshot'a dahil etmek — her testte farklı, sürekli fail
- Snapshot'ları git'e commit etmemek — CI'da her seferinde yeniden oluşturulur, karşılaştırma yapılamaz
- `--snapshot-update` bayrağını CI'da bırakmak — regresyonlar sessizce geçer
- Çok büyük API yanıtı snapshot'lamak — değişiklik diff'i okunamaz hale gelir; önemli alanları seç

## References
- `skills/test-e2e-cli`
- `skills/test-golden-dataset`
