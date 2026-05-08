---
name: test-e2e-cli
description: "Sentinel CLI'yı subprocess olarak çağırarak uçtan uca senaryo testi; çıktı doğrulama, exit code kontrolü ve gerçek config dosyalarıyla end-to-end akış"
---

## Purpose
`sentinel` CLI komutlarını gerçek bir kullanıcı gibi subprocess üzerinden çağırıp çıktıyı ve exit code'u doğrulamak; refactoring'in CLI davranışını bozmadığını garanti etmek.

## Workflow

### CLI Test Yardımcısı
```python
# tests/e2e/cli_runner.py
import subprocess
import json
import shlex
from pathlib import Path
from dataclasses import dataclass

@dataclass
class CLIResult:
    returncode: int
    stdout: str
    stderr: str
    
    def assert_success(self):
        assert self.returncode == 0, (
            f"CLI başarısız (exit {self.returncode}):\n"
            f"STDOUT: {self.stdout}\n"
            f"STDERR: {self.stderr}"
        )
    
    def assert_failure(self, expected_code: int = 1):
        assert self.returncode == expected_code, (
            f"Beklenen exit {expected_code}, alınan {self.returncode}"
        )
    
    def json(self) -> dict:
        return json.loads(self.stdout)

def run_cli(*args: str, env: dict = None, cwd: str = None, timeout: int = 30) -> CLIResult:
    import os
    full_env = {**os.environ, **(env or {})}
    
    result = subprocess.run(
        ["python", "-m", "sentinel.cli", *args],
        capture_output=True,
        text=True,
        env=full_env,
        cwd=cwd,
        timeout=timeout
    )
    return CLIResult(result.returncode, result.stdout, result.stderr)
```

### E2E Test Senaryoları
```python
# tests/e2e/test_sentinel_cli.py
import pytest
import tempfile
import os
from tests.e2e.cli_runner import run_cli

@pytest.fixture
def config_dir(tmp_path):
    """Geçici config dizini"""
    config = tmp_path / "sentinel.yml"
    config.write_text("""
prometheus:
  url: http://localhost:9090
  timeout: 10s
loki:
  url: http://localhost:3100
alerts:
  rules_path: ./rules/
""")
    return tmp_path

def test_version_command():
    result = run_cli("--version")
    result.assert_success()
    assert "sentinel" in result.stdout.lower()
    # Semantic versiyon formatı
    import re
    assert re.search(r'\d+\.\d+\.\d+', result.stdout)

def test_help_command():
    result = run_cli("--help")
    result.assert_success()
    # Temel komutlar help'te görünmeli
    for cmd in ["query", "alert", "config", "validate"]:
        assert cmd in result.stdout, f"'{cmd}' komutu help'te yok"

def test_config_validate_valid(config_dir):
    result = run_cli("config", "validate", "--config", str(config_dir / "sentinel.yml"))
    result.assert_success()
    assert "geçerli" in result.stdout.lower() or "valid" in result.stdout.lower()

def test_config_validate_invalid(tmp_path):
    bad_config = tmp_path / "bad.yml"
    bad_config.write_text("prometheus:\n  url: not-a-url")
    
    result = run_cli("config", "validate", "--config", str(bad_config))
    result.assert_failure()
    assert "url" in result.stderr.lower() or "url" in result.stdout.lower()

def test_query_output_json_format(config_dir):
    result = run_cli(
        "query", "metrics",
        "--config", str(config_dir / "sentinel.yml"),
        "--query", "up",
        "--output", "json",
        env={"TEST_MODE": "1"}  # mock backend kullan
    )
    result.assert_success()
    data = result.json()
    assert "status" in data

def test_missing_required_flag():
    result = run_cli("query", "metrics")  # --query eksik
    result.assert_failure(code=2)  # argparse exit 2
    assert "--query" in result.stderr or "required" in result.stderr.lower()
```

### Timeout ve Temizlik
```python
def test_long_running_command_timeout(config_dir):
    """CLI uzun süreli işlem için timeout ile durmalı"""
    import pytest
    with pytest.raises(subprocess.TimeoutExpired):
        run_cli("stream", "logs", "--follow",
                config=str(config_dir / "sentinel.yml"),
                timeout=3)  # 3 saniye sonra kes
```

## Common mistakes
- `subprocess.run` çıktısını `text=False` çalıştırmak — bytes decode etmek zahmetli; `text=True` + `encoding="utf-8"` kullan
- Exit code 0 olduğunu varsaymak — her test `assert_success()` veya `assert result.returncode == 0` yapmalı
- `env={}` geçmek — `os.environ` miras alınmaz, PATH kaybolur; `{**os.environ, **custom}` kullan
- Geçici dosyaları `tmp_path` yerine `/tmp/hardcoded` konuma yazmak — paralel test koşumunda çakışır

## References
- `skills/test-unit-fastapi`
- `skills/test-snapshot`
