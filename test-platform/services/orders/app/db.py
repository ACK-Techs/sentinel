from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any, cast

from app.config import settings
from app.models import Order
from redis.asyncio import Redis
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(settings.db_url, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


async def verify_schema() -> bool:
    async with engine.begin() as conn:
        return await conn.run_sync(lambda sync_conn: inspect(sync_conn).has_table("orders"))


async def get_order(session: AsyncSession, order_id: str) -> Order | None:
    result = await session.execute(select(Order).where(Order.id == order_id))
    return result.scalar_one_or_none()


async def cache_order(order: Order) -> None:
    await cast(Any, redis_client.hset)(
        f"order:{order.id}",
        mapping={
            "id": order.id,
            "sku": order.sku,
            "qty": order.qty,
            "amount": order.amount,
            "status": order.status,
        },
    )
    await cast(Any, redis_client.expire)(f"order:{order.id}", 300)


async def get_cached_order(order_id: str) -> dict[str, str] | None:
    data = await cast(Any, redis_client.hgetall)(f"order:{order_id}")
    return data or None
