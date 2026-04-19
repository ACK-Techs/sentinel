from __future__ import annotations

import asyncio
import importlib.util
import os
from pathlib import Path

from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

ROOT = Path(__file__).resolve().parents[1]


def load_base(module_name: str, models_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, models_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load models module from {models_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Base


OrdersBase = load_base("orders_models", ROOT / "services" / "orders" / "app" / "models.py")
PaymentsBase = load_base("payments_models", ROOT / "services" / "payments" / "app" / "models.py")
InventoryBase = load_base("inventory_models", ROOT / "services" / "inventory" / "app" / "models.py")


async def seed_orders() -> None:
    engine = create_async_engine(os.environ["ORDERS_DB_URL"], future=True)
    async with engine.begin() as conn:
        await conn.run_sync(OrdersBase.metadata.create_all)
    await engine.dispose()


async def seed_payments() -> None:
    engine = create_async_engine(os.environ["PAYMENTS_DB_URL"], future=True)
    async with engine.begin() as conn:
        await conn.run_sync(PaymentsBase.metadata.create_all)
        await conn.execute(
            text(
                "INSERT INTO payments (order_id, amount, status) VALUES "
                "('seed-order-001', 25, 'approved'), "
                "('seed-order-002', 40, 'approved')"
            )
        )
    redis_url = os.getenv("PAYMENTS_REDIS_URL")
    if redis_url:
        redis = Redis.from_url(redis_url, decode_responses=True)
        await redis.set("charge:seed-order-001", "approved", ex=600)
        await redis.set("charge:seed-order-002", "approved", ex=600)
        await redis.aclose()
    await engine.dispose()


async def seed_inventory() -> None:
    engine = create_async_engine(os.environ["INVENTORY_DB_URL"], future=True)
    async with engine.begin() as conn:
        await conn.run_sync(InventoryBase.metadata.create_all)
        for index in range(1, 11):
            await conn.execute(
                text(
                    "INSERT INTO inventory (sku, stock) VALUES (:sku, :stock) "
                    "ON CONFLICT (sku) DO UPDATE SET stock = EXCLUDED.stock"
                ),
                {"sku": f"SKU-{index:03d}", "stock": 100 - (index * 3)},
            )
    await engine.dispose()


async def main() -> None:
    await seed_orders()
    await seed_payments()
    await seed_inventory()


if __name__ == "__main__":
    asyncio.run(main())
