---
name: docs-api-reference-auto
description: "Sentinel test FastAPI uygulamalarının OpenAPI şemasından otomatik API referans dokümantasyonu üretir ve yayınlar"
---

## Purpose
Sentinel'in target servislerindeki FastAPI endpoint'leri manuel dokümantasyon olmadan OpenAPI/Swagger şeması üretir. Bu skill, o şemayı alıp Sphinx, MkDocs veya static HTML formatında kapsamlı bir API referansına dönüştürür ve `documentations/api/` dizininde yayınlar.

## Workflow

### 1. FastAPI OpenAPI şemasını zenginleştir
```python
# services/orders/app/routes/orders.py
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["Orders"])

class OrderRequest(BaseModel):
    product_id: str = Field(..., example="sku-123", description="Ürün kataloğu ID'si")
    quantity: int = Field(..., ge=1, le=100, example=2)
    user_id: str = Field(..., example="u-456")

class OrderResponse(BaseModel):
    order_id: str = Field(..., example="ord-789")
    status: str = Field(..., example="confirmed")
    total_price: float

@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni sipariş oluştur",
    description="""
    Stok kontrolü ve ödeme onayı sonrasında yeni sipariş oluşturur.
    
    **Saga akışı**: orders → payments → inventory
    
    Başarısız ödeme durumunda otomatik stok iadesi yapılır.
    """,
    responses={
        402: {"description": "Ödeme başarısız"},
        409: {"description": "Yetersiz stok"},
    }
)
async def create_order(request: OrderRequest) -> OrderResponse:
    ...
```

### 2. OpenAPI JSON'u dışa aktar
```bash
# Çalışan servisten çek
curl -s http://orders.sentinel-target.svc/openapi.json -o docs/openapi/orders.json

# Veya Python script ile statik üret
python -c "
from app.main import app
import json
with open('docs/openapi/orders.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
"
```

### 3. Tüm servisleri birleştir
```python
# scripts/merge_openapi.py
import json, glob

merged = {
    "openapi": "3.1.0",
    "info": {"title": "Sentinel Target Services API", "version": "1.0.0"},
    "paths": {},
    "components": {"schemas": {}}
}

for schema_file in glob.glob("docs/openapi/*.json"):
    service = schema_file.split("/")[-1].replace(".json", "")
    schema = json.load(open(schema_file))
    
    for path, methods in schema.get("paths", {}).items():
        merged["paths"][f"/{service}{path}"] = methods
    
    for name, schema_def in schema.get("components", {}).get("schemas", {}).items():
        merged["components"]["schemas"][f"{service.title()}{name}"] = schema_def

json.dump(merged, open("docs/openapi/merged.json", "w"), indent=2)
```

### 4. MkDocs ile yayınla
```yaml
# mkdocs.yml
site_name: Sentinel API Reference
docs_dir: documentations
plugins:
  - openapi-docs:
      config:
        - id: sentinel-api
          spec_path: api/merged.json
          output_path: api/reference.md
```

### 5. CI'da otomatik güncelle
```yaml
# .github/workflows/docs.yml
- name: Generate API docs
  run: |
    for svc in orders payments gateway inventory; do
      kubectl exec -n sentinel-target deploy/$svc -- \
        python -c "from app.main import app; import json; print(json.dumps(app.openapi()))" \
        > documentations/api/$svc.json
    done
    python scripts/merge_openapi.py
    mkdocs build
```

### 6. Deprecation anotasyonu
```python
@router.get("/orders/{order_id}/legacy",
    deprecated=True,
    description="**Deprecated**: `/orders/{id}` kullanın. Bu endpoint v2.0'da kaldırılacak."
)
async def get_order_legacy(order_id: str):
    ...
```

## Common mistakes
1. `Field(description=...)` yerine yalnızca type hint kullanmak — OpenAPI şeması anlamsız kalır.
2. Error response şemalarını tanımlamamak — `responses={4xx: ...}` olmadan hata dokümantasyonu eksik.
3. `example` değerlerini gerçekçi olmayan değerlerle doldurmak — `"string"` yerine gerçek bir örnek yaz.
4. Merged OpenAPI dosyasını repoya commit etmek — üretilmiş artifact, CI'da dinamik oluşturulmalı.

## References
- `skills/target-app-health-endpoint`
- `skills/target-app-versioned-api`
- `skills/docs-readme-structure`
