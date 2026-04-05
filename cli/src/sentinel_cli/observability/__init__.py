"""Observability helpers."""

from sentinel_cli.observability.grafana import (
    GrafanaCheckResult,
    check_grafana_connection,
)

__all__ = ["GrafanaCheckResult", "check_grafana_connection"]
