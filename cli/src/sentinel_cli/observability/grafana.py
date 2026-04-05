"""Grafana HTTP connectivity checks used by `doctor`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from sentinel_cli.config.models import GrafanaSettings


@dataclass(slots=True)
class GrafanaCheckResult:
    """Secret-safe result for doctor output."""

    configured: bool
    attempted: bool
    ok: bool
    status: str
    message: str
    http_status: int | None = None
    health_path: str | None = None
    token_present: bool = False
    base_url_present: bool = False
    verify_ssl: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "configured": self.configured,
            "attempted": self.attempted,
            "ok": self.ok,
            "status": self.status,
            "message": self.message,
            "http_status": self.http_status,
            "health_path": self.health_path,
            "token_present": self.token_present,
            "base_url_present": self.base_url_present,
            "verify_ssl": self.verify_ssl,
            "troubleshoot_skill": "skills/agentic-troubleshoot-grafana/SKILL.md",
        }


def _join_url(base_url: str, path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{base_url.rstrip('/')}{normalized_path}"


def check_grafana_connection(
    settings: GrafanaSettings,
    *,
    env: dict[str, str],
    transport: httpx.BaseTransport | None = None,
) -> GrafanaCheckResult:
    """Probe the configured Grafana endpoint with a short HTTP request."""

    configured = settings.enabled or bool(settings.base_url)
    token = env.get(settings.token_env)
    if not settings.base_url:
        return GrafanaCheckResult(
            configured=configured,
            attempted=False,
            ok=False,
            status="skipped",
            message="Grafana baglantisi ayarli degil; SENTINEL_GRAFANA_BASE_URL ekleyin.",
            health_path=settings.health_path,
            token_present=bool(token),
            base_url_present=False,
            verify_ssl=settings.verify_ssl,
        )

    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    timeout = httpx.Timeout(settings.timeout_sec)
    url = _join_url(settings.base_url, settings.health_path)
    try:
        with httpx.Client(
            timeout=timeout,
            verify=settings.verify_ssl,
            transport=transport,
        ) as client:
            response = client.get(url, headers=headers, follow_redirects=True)
    except httpx.TimeoutException:
        return GrafanaCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="timeout",
            message=(
                "Grafana yanit vermedi; base URL, TLS ve ag erisimini dogrulayin. "
                "Gerekirse skills/agentic-troubleshoot-grafana/SKILL.md akisini izleyin."
            ),
            health_path=settings.health_path,
            token_present=bool(token),
            base_url_present=True,
            verify_ssl=settings.verify_ssl,
        )
    except httpx.HTTPError as exc:
        return GrafanaCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="error",
            message=f"Grafana istegi basarisiz: {exc.__class__.__name__}.",
            health_path=settings.health_path,
            token_present=bool(token),
            base_url_present=True,
            verify_ssl=settings.verify_ssl,
        )

    if response.status_code == 200:
        return GrafanaCheckResult(
            configured=True,
            attempted=True,
            ok=True,
            status="ok",
            message="Grafana baglantisi dogrulandi.",
            http_status=response.status_code,
            health_path=settings.health_path,
            token_present=bool(token),
            base_url_present=True,
            verify_ssl=settings.verify_ssl,
        )

    if response.status_code in {401, 403}:
        return GrafanaCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="unauthorized",
            message=(
                "Grafana erisiyor ancak kimlik dogrulama reddedildi; token/env eslesmesini "
                "ve gerekirse skills/agentic-troubleshoot-grafana/SKILL.md akisini kontrol edin."
            ),
            http_status=response.status_code,
            health_path=settings.health_path,
            token_present=bool(token),
            base_url_present=True,
            verify_ssl=settings.verify_ssl,
        )

    return GrafanaCheckResult(
        configured=True,
        attempted=True,
        ok=False,
        status="http_error",
        message=f"Grafana beklenmeyen HTTP durumu dondurdu: {response.status_code}.",
        http_status=response.status_code,
        health_path=settings.health_path,
        token_present=bool(token),
        base_url_present=True,
        verify_ssl=settings.verify_ssl,
    )
