from __future__ import annotations

from threading import Lock

_HTTPX_READY = False
_REDIS_READY = False
_SQLALCHEMY_ENGINES: set[int] = set()
_LOCK = Lock()


def instrument_httpx() -> None:
    global _HTTPX_READY
    with _LOCK:
        if _HTTPX_READY:
            return
        from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

        HTTPXClientInstrumentor().instrument()
        _HTTPX_READY = True


def instrument_redis() -> None:
    global _REDIS_READY
    with _LOCK:
        if _REDIS_READY:
            return
        from opentelemetry.instrumentation.redis import RedisInstrumentor

        RedisInstrumentor().instrument()
        _REDIS_READY = True


def instrument_sqlalchemy(engine: object) -> None:
    with _LOCK:
        engine_id = id(engine)
        if engine_id in _SQLALCHEMY_ENGINES:
            return
        from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

        sync_engine = getattr(engine, "sync_engine", engine)
        SQLAlchemyInstrumentor().instrument(engine=sync_engine)
        _SQLALCHEMY_ENGINES.add(engine_id)
