from __future__ import annotations

from typing import Annotated

from app.db import get_session, redis_client
from app.models import Payment
from fastapi import APIRouter, Depends
from sentinel_obs import get_meter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
meter = get_meter("payments")
payment_failures = meter.create_counter("app.payments.failed", unit="1")
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("/charge")
async def charge(payload: dict, session: SessionDep) -> dict:
    order_id = str(payload["order_id"])
    amount = int(payload["amount"])
    cache_key = f"charge:{order_id}"
    if await redis_client.exists(cache_key):
        return {"order_id": order_id, "status": "approved", "idempotent": True}

    payment = Payment(order_id=order_id, amount=amount, status="approved")
    session.add(payment)
    await session.commit()
    await redis_client.set(cache_key, "approved", ex=600)
    return {"order_id": order_id, "status": "approved", "idempotent": False}
