from __future__ import annotations

from typing import Annotated, Any, cast

from app.db import get_inventory_item, get_session, redis_client
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/inventory/{sku}")
async def fetch_inventory(sku: str, session: SessionDep) -> dict:
    cache_key = f"inventory:{sku}"
    cached = await cast(Any, redis_client.hgetall)(cache_key)
    if cached:
        return cached
    item = await get_inventory_item(session, sku)
    if item is None:
        raise HTTPException(status_code=404, detail="sku not found")
    payload = {"sku": item.sku, "stock": item.stock}
    await cast(Any, redis_client.hset)(cache_key, mapping={k: str(v) for k, v in payload.items()})
    await cast(Any, redis_client.expire)(cache_key, 120)
    return payload


@router.post("/reserve")
async def reserve_inventory(payload: dict, session: SessionDep) -> dict:
    sku = str(payload["sku"])
    qty = int(payload["qty"])
    item = await get_inventory_item(session, sku)
    if item is None:
        raise HTTPException(status_code=404, detail="sku not found")
    if item.stock < qty:
        raise HTTPException(status_code=409, detail="insufficient stock")
    item.stock -= qty
    session.add(item)
    await session.commit()
    await redis_client.delete(f"inventory:{sku}")
    return {"sku": sku, "reserved": qty, "remaining": item.stock}
