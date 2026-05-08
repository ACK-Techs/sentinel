---
name: python-secrets-runtime
description: "Runtime'da secret güvenli okuma ve maskeleme — Sentinel servislerinde credential yönetimi ve log sızıntısı önleme"
---

## Purpose
Secret'ların runtime'da güvenli okunması, log çıktılarında maskelenmesi ve belleğe alındıktan sonra gereksiz kopyaların temizlenmesi kritik güvenlik gereksinimleridir. Sentinel'de Kubernetes Secret + environment variable yöntemi kullanılır; Vault entegrasyonu opsiyoneldir.

## Workflow

### 1. Pydantic Settings ile secret okuma

```python
# config.py
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class SentinelSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SENTINEL_",
        env_file=".env",
        env_file_encoding="utf-8",
        secrets_dir="/run/secrets",  # K8s volumeMount
    )

    # SecretStr: .get_secret_value() çağrılana kadar maskelenir
    database_url: SecretStr
    api_key: SecretStr
    jwt_secret: SecretStr

    prometheus_url: str = "http://prometheus:9090"
    log_level: str = "INFO"

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid:
            raise ValueError(f"log_level {v!r} geçersiz. Geçerliler: {valid}")
        return v.upper()

# Tek instance — dependency injection ile dağıt
settings = SentinelSettings()  # type: ignore[call-arg]
```

### 2. Güvenli kullanım ve maskeleme

```python
# Kötü — secret string olarak log'a düşer
logger.info("DB bağlantısı", url=settings.database_url)

# İyi — SecretStr repr'ı maskeler
logger.info("DB bağlantısı", url=repr(settings.database_url))
# Çıktı: url='**********'

# Gerçek değere erişim — yalnızca ihtiyaç anında
async def create_db_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        dsn=settings.database_url.get_secret_value()
    )
```

### 3. Kubernetes Secret → Pod ortam değişkeni

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: sentinel-gateway
        env:
        - name: SENTINEL_API_KEY
          valueFrom:
            secretKeyRef:
              name: sentinel-secrets
              key: api-key
        - name: SENTINEL_DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: sentinel-secrets
              key: database-url
        volumeMounts:
        - name: jwt-secret
          mountPath: /run/secrets
          readOnly: true
      volumes:
      - name: jwt-secret
        secret:
          secretName: sentinel-jwt
```

### 4. Log maskeleme middleware

```python
import re

SENSITIVE_PATTERNS = [
    re.compile(r'(?i)(password|token|secret|key|authorization)\s*[=:]\s*\S+'),
    re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]+=*'),
]

def mask_sensitive(text: str) -> str:
    for pattern in SENSITIVE_PATTERNS:
        text = pattern.sub(lambda m: m.group(0).split("=")[0] + "=***MASKED***", text)
    return text
```

### 5. Vault dinamik secret (opsiyonel)

```python
import hvac

def get_db_credentials() -> tuple[str, str]:
    client = hvac.Client(url=os.environ["VAULT_ADDR"], token=os.environ["VAULT_TOKEN"])
    secret = client.secrets.database.generate_credentials(name="sentinel-postgres")
    return secret["data"]["username"], secret["data"]["password"]
```

## Common mistakes

- `str` yerine `SecretStr` kullanmamak — `repr()` veya log'da düz metin görünür
- `.env` dosyasını git'e commit etmek — pre-commit detect-secrets hook ekle
- Secret'ı global değişkene atayıp tüm modülden erişmek — dependency injection ile geçir
- K8s Secret'ı base64 encode ederken `echo -n` unutmak — trailing newline şifreyi bozar

## References
- `skills/python-pre-commit`
- `skills/python-dependency-pinning`
- `skills/fastapi-security-apikey`
