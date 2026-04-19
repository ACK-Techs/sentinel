from __future__ import annotations

import asyncio
import logging
from datetime import UTC, datetime

from app.config import settings
from redis.asyncio import Redis
from redis.exceptions import ResponseError
from sentinel_obs import get_meter, get_tracer, init_telemetry, instrument_redis

init_telemetry(settings.service_name, settings.service_version, settings.deployment_env)

logger = logging.getLogger("worker")
tracer = get_tracer("worker")
meter = get_meter("worker")
processed_counter = meter.create_counter("app.worker.processed", unit="1")
lag_histogram = meter.create_histogram("app.worker.stream_lag_ms", unit="ms")
pending_histogram = meter.create_histogram("app.worker.stream_pending", unit="1")


async def ensure_group(redis: Redis) -> None:
    try:
        await redis.xgroup_create(
            settings.orders_stream,
            settings.consumer_group,
            id="0",
            mkstream=True,
        )
    except ResponseError as exc:
        if "BUSYGROUP" not in str(exc):
            raise



async def current_pending(redis: Redis) -> int:
    summary = await redis.xpending(settings.orders_stream, settings.consumer_group)
    if isinstance(summary, dict):
        return int(summary.get("pending", 0))
    if isinstance(summary, (list, tuple)) and summary:
        return int(summary[0])
    return 0


async def process_record(redis: Redis, record_id: str, payload: dict[str, str]) -> None:
    with tracer.start_as_current_span("worker.process") as span:
        span.set_attribute("messaging.system", "redis")
        span.set_attribute("messaging.destination.name", settings.orders_stream)
        span.set_attribute("messaging.operation", "process")
        span.set_attribute("messaging.message.id", record_id)
        span.set_attribute("messaging.consumer.group", settings.consumer_group)
        created_at_raw = payload.get("created_at")
        if created_at_raw:
            created_at = datetime.fromisoformat(created_at_raw)
            lag_ms = (datetime.now(UTC) - created_at).total_seconds() * 1000
            lag_histogram.record(lag_ms, {"stream": settings.orders_stream})
        await asyncio.sleep(0.2)
        processed_counter.add(1, {"event_type": payload.get("event_type", "unknown")})
        await redis.xack(settings.orders_stream, settings.consumer_group, record_id)
        span.set_attribute("worker.result", "acked")


async def run() -> None:
    redis = Redis.from_url(settings.redis_url, decode_responses=True)
    instrument_redis()
    await ensure_group(redis)
    while True:
        logger.info("worker heartbeat")
        pending_histogram.record(await current_pending(redis), {"stream": settings.orders_stream})
        records = await redis.xreadgroup(
            settings.consumer_group,
            settings.consumer_name,
            {settings.orders_stream: ">"},
            count=10,
            block=5000,
        )
        for _stream_name, items in records:
            for record_id, payload in items:
                await process_record(redis, record_id, payload)



def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
