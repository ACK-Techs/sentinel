---
name: fastapi-security-oauth2
description: "FastAPI OAuth2 password flow ve JWT entegrasyonu — Sentinel kullanıcı kimlik doğrulama sistemi"
---

## Purpose
Sentinel'in gateway'i hem insan kullanıcılar (Swagger UI, CLI) hem de servis hesapları için JWT tabanlı kimlik doğrulama yapar. OAuth2 password flow geliştirme/test ortamı için pratik; production'da OIDC (Keycloak) tercih edilir.

## Workflow

### 1. JWT üretim ve doğrulama

```python
# app/auth/jwt.py
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from app.config import settings

ALGORITHM = "HS256"

def create_access_token(subject: str, roles: list[str], expires_minutes: int = 30) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": subject,
        "roles": roles,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "iss": "sentinel-gateway",
    }
    return jwt.encode(payload, settings.jwt_secret.get_secret_value(), algorithm=ALGORITHM)

def decode_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub", "roles"]},
        )
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except jwt.InvalidTokenError:
        return None
```

### 2. OAuth2 password flow endpoint

```python
# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt import create_access_token
from app.services.user_service import authenticate_user

router = APIRouter(tags=["Auth"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800

@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Kullanıcı adı veya parola hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.id, roles=user.roles)
    return TokenResponse(access_token=token)
```

### 3. Bearer token dependency

```python
# app/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt import decode_token
from app.models.auth import CurrentUser

security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(401, "Token gerekli", headers={"WWW-Authenticate": "Bearer"})

    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(401, "Geçersiz token", headers={"WWW-Authenticate": "Bearer"})

    return CurrentUser(id=payload["sub"], roles=payload["roles"])

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> CurrentUser | None:
    if credentials is None:
        return None
    payload = decode_token(credentials.credentials)
    if payload is None:
        return None
    return CurrentUser(id=payload["sub"], roles=payload["roles"])
```

### 4. OIDC (Keycloak) production entegrasyonu

```python
from fastapi.security import OpenIdConnect

oidc_scheme = OpenIdConnect(
    openIdConnectUrl="https://keycloak.example.com/realms/sentinel/.well-known/openid-configuration"
)

async def get_current_user_oidc(token: str = Depends(oidc_scheme)) -> CurrentUser:
    from joserfc import jwt as jose_jwt
    # JWKS ile doğrulama
    ...
```

## Common mistakes

- `auto_error=True` ile opsiyonel endpoint'lerde HTTPBearer kullanmak — token yoksa 403 fırlatır
- JWT secret'ı `str` olarak config'de tutmak — `SecretStr` kullan, loglara düşmez
- `roles` claim'ini token'da döndürmeyip her istekte DB sorgulamak — stateless JWT avantajı kaybolur
- Token refresh endpoint yazmamak — `expires_in` kısa tutulursa kullanıcı sık sık login olmak zorunda

## References
- `skills/fastapi-security-apikey`
- `skills/fastapi-dependency-injection`
- `skills/python-secrets-runtime`
