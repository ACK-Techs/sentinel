from __future__ import annotations

import asyncio
import logging
import random
import threading
import time
from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter, Depends, Header, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine

from sentinel_obs.bootstrap import get_tracer

LOGGER = logging.getLogger("sentinel_obs.chaos")
TRACER = get_tracer("sentinel_obs.chaos")
LEAK_BUCKET: list[bytes] = []
LEAK_LIMIT_BLOCKS = 256


class ChaosState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: str = "healthy"
    error_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    error_status: int = Field(default=503, ge=400, le=599)
    latency_p50_ms: int = Field(default=0, ge=0)
    latency_p99_ms: int = Field(default=0, ge=0)
    cpu_burn: bool = False
    downstream_block: list[str] = Field(default_factory=list)
    memory_leak_kb_per_req: int = Field(default=0, ge=0)
    db_slow: int = Field(default=0, ge=0)
    downstream_timeout_ms: int = Field(default=0, ge=0)
    source: str = "default"


class ChaosPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    profile: str | None = None
    error_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    error_status: int | None = Field(default=None, ge=400, le=599)
    latency_p50_ms: int | None = Field(default=None, ge=0)
    latency_p99_ms: int | None = Field(default=None, ge=0)
    cpu_burn: bool | None = None
    downstream_block: list[str] | None = None
    memory_leak_kb_per_req: int | None = Field(default=None, ge=0)
    db_slow: int | None = Field(default=None, ge=0)
    downstream_timeout_ms: int | None = Field(default=None, ge=0)


class ChaosProfileRequest(BaseModel):
    name: str


class ChaosProfileResponse(BaseModel):
    applied: ChaosState
    version: int
    source: str


class ChaosSettings(BaseModel):
    profile_path: Path = Path("/etc/chaos/profile.yaml")
    token: str = "sentinel-chaos-token"


class ChaosManager:
    def __init__(self, settings: ChaosSettings) -> None:
        self.settings = settings
        self._lock = threading.Lock()
        self._state = ChaosState()
        self._version = 0

    def snapshot(self) -> tuple[ChaosState, int]:
        with self._lock:
            return self._state.model_copy(deep=True), self._version

    def replace(self, state: ChaosState, source: str) -> ChaosProfileResponse:
        with self._lock:
            self._state = state.model_copy(update={"source": source})
            self._version += 1
            self._reset_leak_if_healthy()
            self._add_event("chaos.state.replaced", self._state)
            return ChaosProfileResponse(
                applied=self._state.model_copy(deep=True),
                version=self._version,
                source=source,
            )

    def patch(self, patch: ChaosPatch, source: str) -> ChaosProfileResponse:
        with self._lock:
            values = patch.model_dump(exclude_none=True)
            self._state = self._state.model_copy(update=values | {"source": source})
            self._version += 1
            self._reset_leak_if_healthy()
            self._add_event("chaos.state.patched", self._state)
            return ChaosProfileResponse(
                applied=self._state.model_copy(deep=True),
                version=self._version,
                source=source,
            )

    def set_profile(self, name: str, source: str) -> ChaosProfileResponse:
        data = self._read_profile(name)
        data["profile"] = name
        return self.replace(ChaosState.model_validate(data), source=source)

    def reload(self) -> ChaosProfileResponse:
        state = ChaosState.model_validate(self._load_profile_file())
        return self.replace(state, source="configmap")

    def _load_profile_file(self) -> dict[str, Any]:
        path = self.settings.profile_path
        if not path.exists():
            raise HTTPException(status_code=404, detail=f"profile file not found: {path}")
        raw = yaml.safe_load(path.read_text()) or {}
        if not isinstance(raw, dict):
            raise HTTPException(status_code=400, detail="profile file must be a mapping")
        return raw

    def _read_profile(self, name: str) -> dict[str, Any]:
        candidate = self.settings.profile_path.parent.parent / "profiles" / f"{name}.yaml"
        if candidate.exists():
            raw = yaml.safe_load(candidate.read_text()) or {}
            if isinstance(raw, dict):
                return raw
        return self._load_profile_file() if name == "configmap" else _default_profiles()[name]

    def _add_event(self, event_name: str, state: ChaosState) -> None:
        span = TRACER.start_span(event_name)
        try:
            span.add_event(
                "chaos.profile.changed",
                attributes={
                    "chaos.profile": state.profile,
                    "chaos.error_rate": state.error_rate,
                    "chaos.latency_p50_ms": state.latency_p50_ms,
                    "chaos.latency_p99_ms": state.latency_p99_ms,
                    "chaos.cpu_burn": state.cpu_burn,
                },
            )
        finally:
            span.end()

    def _reset_leak_if_healthy(self) -> None:
        if self._state.profile == "healthy" or self._state.memory_leak_kb_per_req == 0:
            LEAK_BUCKET.clear()


_MANAGERS: dict[str, ChaosManager] = {}
_MANAGER_LOCK = threading.Lock()


def chaos_settings(
    token: str | None = None,
    profile_path: str | Path | None = None,
) -> ChaosSettings:
    return ChaosSettings(
        token=token or "sentinel-chaos-token",
        profile_path=Path(profile_path) if profile_path else Path("/etc/chaos/profile.yaml"),
    )


def get_chaos_manager(service_name: str, settings: ChaosSettings) -> ChaosManager:
    with _MANAGER_LOCK:
        if service_name not in _MANAGERS:
            manager = ChaosManager(settings)
            _MANAGERS[service_name] = manager
            try:
                if settings.profile_path.exists():
                    manager.reload()
            except Exception as exc:  # noqa: BLE001
                LOGGER.warning("failed to preload chaos profile for %s: %s", service_name, exc)
        return _MANAGERS[service_name]


class ChaosAdminDependency:
    def __init__(self, token: str) -> None:
        self.token = token

    async def __call__(self, x_chaos_token: str | None = Header(default=None)) -> None:
        if x_chaos_token != self.token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid chaos token",
            )


class ChaosMiddleware:
    def __init__(self, app: Any, manager: ChaosManager) -> None:
        self.app = app
        self.manager = manager

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        if path.startswith("/admin") or path == "/health":
            await self.app(scope, receive, send)
            return

        state, _version = self.manager.snapshot()
        await self._apply_latency(state)
        await self._apply_cpu_burn(state)
        self._apply_memory_pressure(state)
        if random.random() < state.error_rate:
            response = Response(content="chaos:error", status_code=state.error_status)
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)

    async def _apply_latency(self, state: ChaosState) -> None:
        delay_ms = state.latency_p99_ms if random.random() < 0.01 else state.latency_p50_ms
        if delay_ms > 0:
            await asyncio.sleep(delay_ms / 1000)

    async def _apply_cpu_burn(self, state: ChaosState) -> None:
        if not state.cpu_burn:
            return
        end = time.perf_counter() + 0.05
        iterations = 0
        while time.perf_counter() < end:
            iterations += 1
            _ = iterations * iterations
            if iterations % 1000 == 0:
                await asyncio.sleep(0)

    def _apply_memory_pressure(self, state: ChaosState) -> None:
        if state.memory_leak_kb_per_req <= 0:
            return
        block = b"x" * (state.memory_leak_kb_per_req * 1024)
        LEAK_BUCKET.append(block)
        if len(LEAK_BUCKET) > LEAK_LIMIT_BLOCKS:
            del LEAK_BUCKET[: len(LEAK_BUCKET) - LEAK_LIMIT_BLOCKS]
        time.sleep(min(0.05, state.memory_leak_kb_per_req / 50000))


def build_admin_router(manager: ChaosManager, token: str) -> APIRouter:
    dependency = ChaosAdminDependency(token)
    router = APIRouter(prefix="/admin", dependencies=[Depends(dependency)])

    @router.get("/chaos", response_model=ChaosProfileResponse)
    async def get_chaos() -> ChaosProfileResponse:
        applied, version = manager.snapshot()
        return ChaosProfileResponse(applied=applied, version=version, source=applied.source)

    @router.post("/chaos", response_model=ChaosProfileResponse)
    async def set_chaos(state: ChaosState) -> ChaosProfileResponse:
        return manager.replace(state, source="api")

    @router.patch("/chaos", response_model=ChaosProfileResponse)
    async def patch_chaos(state: ChaosPatch) -> ChaosProfileResponse:
        return manager.patch(state, source="api")

    @router.post("/chaos/profile", response_model=ChaosProfileResponse)
    async def set_profile(body: ChaosProfileRequest) -> ChaosProfileResponse:
        return manager.set_profile(body.name, source="api")

    @router.post("/chaos/reload", response_model=ChaosProfileResponse)
    async def reload_profile() -> ChaosProfileResponse:
        return manager.reload()

    return router


def register_db_slow_hook(engine: AsyncEngine, manager: ChaosManager) -> None:
    sync_engine = engine.sync_engine

    @event.listens_for(sync_engine, "before_cursor_execute")
    def before_cursor_execute(*_args: Any, **_kwargs: Any) -> None:
        state, _version = manager.snapshot()
        if state.db_slow > 0:
            time.sleep(state.db_slow / 1000)


def downstream_behavior(manager: ChaosManager, target_service: str) -> tuple[bool, float | None]:
    state, _version = manager.snapshot()
    blocked = target_service in state.downstream_block
    timeout = state.downstream_timeout_ms / 1000 if state.downstream_timeout_ms > 0 else None
    return blocked, timeout


def _default_profiles() -> dict[str, dict[str, Any]]:
    return {
        "healthy": {"profile": "healthy"},
        "slow-db": {"profile": "slow-db", "db_slow": 250, "latency_p99_ms": 400, "cpu_burn": False},
        "downstream-outage": {
            "profile": "downstream-outage",
            "error_rate": 0.35,
            "error_status": 503,
            "cpu_burn": False,
            "downstream_block": ["payments"],
        },
        "memory-leak": {
            "profile": "memory-leak",
            "memory_leak_kb_per_req": 128,
            "latency_p50_ms": 20,
            "cpu_burn": False,
        },
        "cache-stampede": {
            "profile": "cache-stampede",
            "latency_p99_ms": 700,
            "db_slow": 150,
            "cpu_burn": False,
        },
        "cascading": {
            "profile": "cascading",
            "latency_p50_ms": 100,
            "latency_p99_ms": 1000,
            "error_rate": 0.15,
            "downstream_timeout_ms": 250,
            "cpu_burn": True,
        },
    }
