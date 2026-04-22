"""Observability gateway health checks and client helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from sentinel_cli.config.models import ObservabilityGatewaySettings


@dataclass(slots=True)
class GatewayCheckResult:
    """Secret-safe result for gateway health checks."""

    configured: bool
    attempted: bool
    ok: bool
    status: str
    message: str
    http_status: int | None = None
    token_present: bool = False
    base_url_present: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "configured": self.configured,
            "attempted": self.attempted,
            "ok": self.ok,
            "status": self.status,
            "message": self.message,
            "http_status": self.http_status,
            "token_present": self.token_present,
            "base_url_present": self.base_url_present,
        }


class GatewayClientError(Exception):
    """Secret-safe gateway client failure."""

    def __init__(self, message: str, *, detail: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail


def _join_url(base_url: str, path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{base_url.rstrip('/')}{normalized_path}"


def check_gateway_connection(
    settings: ObservabilityGatewaySettings,
    *,
    env: dict[str, str],
    transport: httpx.BaseTransport | None = None,
) -> GatewayCheckResult:
    """Probe the configured gateway with a short HTTP request."""

    configured = settings.enabled or bool(settings.base_url)
    token = env.get(settings.token_env) if settings.token_env else None
    if not settings.base_url:
        return GatewayCheckResult(
            configured=configured,
            attempted=False,
            ok=False,
            status="skipped",
            message=(
                "Observability gateway ayarli degil; "
                "SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL ekleyin."
            ),
            token_present=bool(token),
            base_url_present=False,
        )

    headers = _auth_headers(settings, env)
    try:
        with httpx.Client(
            timeout=httpx.Timeout(settings.timeout_sec),
            transport=transport,
        ) as client:
            response = client.get(
                _join_url(settings.base_url, "/health"),
                headers=headers,
                follow_redirects=True,
            )
    except httpx.TimeoutException:
        return GatewayCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="timeout",
            message="Observability gateway yanit vermedi.",
            token_present=bool(token),
            base_url_present=True,
        )
    except httpx.HTTPError as exc:
        return GatewayCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="error",
            message=f"Observability gateway istegi basarisiz: {exc.__class__.__name__}.",
            token_present=bool(token),
            base_url_present=True,
        )

    if response.status_code == 200:
        return GatewayCheckResult(
            configured=True,
            attempted=True,
            ok=True,
            status="ok",
            message="Observability gateway baglantisi dogrulandi.",
            http_status=200,
            token_present=bool(token),
            base_url_present=True,
        )

    if response.status_code in {401, 403}:
        return GatewayCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="unauthorized",
            message="Observability gateway kimlik dogrulamasi reddedildi.",
            http_status=response.status_code,
            token_present=bool(token),
            base_url_present=True,
        )

    return GatewayCheckResult(
        configured=True,
        attempted=True,
        ok=False,
        status="http_error",
        message=f"Observability gateway beklenmeyen HTTP durumu dondurdu: {response.status_code}.",
        http_status=response.status_code,
        token_present=bool(token),
        base_url_present=True,
    )


class GatewayClient:
    """Thin HTTP client for the observability gateway API."""

    def __init__(
        self,
        settings: ObservabilityGatewaySettings,
        *,
        env: dict[str, str],
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._settings = settings
        self._env = env
        self._transport = transport

    def query_metric(self, query: str) -> dict[str, Any]:
        return self._request("POST", "/api/v1/metrics/query", json={"query": query})

    def query_logs(
        self,
        *,
        service: str | None = None,
        query: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        resolved_query = query or (f'{{job="{service}"}}' if service else None)
        if not resolved_query:
            raise GatewayClientError("Log sorgusu icin --query veya --service gerekli.")
        return self._request(
            "POST",
            "/api/v1/logs/query_range",
            json={"query": resolved_query, "limit": limit},
        )

    def search_traces(
        self,
        *,
        service: str | None = None,
        query: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"limit": limit}
        if query:
            payload["query"] = query
        if service:
            payload["tags"] = {"service.name": service}
        if "query" not in payload and "tags" not in payload:
            raise GatewayClientError("Trace sorgusu icin --query veya --service gerekli.")
        return self._request("POST", "/api/v1/traces/search", json=payload)

    def _request(self, method: str, path: str, *, json: dict[str, Any]) -> dict[str, Any]:
        if not self._settings.base_url:
            raise GatewayClientError(
                "Observability gateway ayarli degil. Config veya env icinde base_url ekleyin."
            )

        try:
            with httpx.Client(
                timeout=httpx.Timeout(self._settings.timeout_sec),
                transport=self._transport,
            ) as client:
                response = client.request(
                    method,
                    _join_url(self._settings.base_url, path),
                    headers=_auth_headers(self._settings, self._env),
                    json=json,
                )
        except httpx.TimeoutException as exc:
            raise GatewayClientError(
                "Observability gateway zaman asimina ugradi.",
                detail=exc.__class__.__name__,
            ) from exc
        except httpx.HTTPError as exc:
            raise GatewayClientError(
                "Observability gateway istegi basarisiz oldu.",
                detail=exc.__class__.__name__,
            ) from exc

        if response.status_code >= 400:
            message, detail = _error_from_response(response)
            raise GatewayClientError(message, detail=detail)

        try:
            return response.json()
        except ValueError as exc:
            raise GatewayClientError(
                "Observability gateway gecersiz JSON dondurdu.",
                detail="invalid_json",
            ) from exc


def _auth_headers(settings: ObservabilityGatewaySettings, env: dict[str, str]) -> dict[str, str]:
    if not settings.token_env:
        return {}
    token = env.get(settings.token_env)
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _error_from_response(response: httpx.Response) -> tuple[str, str | None]:
    try:
        payload = response.json()
    except ValueError:
        return (
            f"Observability gateway HTTP {response.status_code} dondu.",
            f"http_status={response.status_code}",
        )

    error = payload.get("error", {})
    backend = error.get("backend")
    message = error.get("message")
    retryable = error.get("retryable")
    parts = []
    if backend:
        parts.append(f"backend={backend}")
    parts.append(f"http_status={response.status_code}")
    if retryable is not None:
        parts.append(f"retryable={retryable}")
    detail = ", ".join(parts) or None
    if isinstance(message, str) and message:
        return (message, detail)
    return (f"Observability gateway HTTP {response.status_code} dondu.", detail)
