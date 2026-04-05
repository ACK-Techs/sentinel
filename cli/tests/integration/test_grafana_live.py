from __future__ import annotations

import os

import pytest

from sentinel_cli.config import load_config
from sentinel_cli.observability import check_grafana_connection


pytestmark = pytest.mark.live


@pytest.mark.skipif(
    not os.environ.get("SENTINEL_GRAFANA_BASE_URL"),
    reason="Canli Grafana testi icin SENTINEL_GRAFANA_BASE_URL gerekli.",
)
def test_grafana_live_connection_responds() -> None:
    config = load_config(env=dict(os.environ))

    result = check_grafana_connection(config.grafana, env=dict(os.environ))

    assert result.attempted is True
    assert result.http_status in {200, 401, 403} or result.status in {"ok", "unauthorized"}
