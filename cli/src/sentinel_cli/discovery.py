"""Endpoint discovery for local Sentinel installations."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from sentinel_cli.config.models import AppConfig

InstallMode = Literal["cos", "compose", "k8s"]


DEFAULT_PORTS = {
    "grafana": 3000,
    "gateway": 8091,
    "prometheus": 9090,
    "loki": 3100,
    "tempo": 3200,
}


class DiscoveredEndpoints(BaseModel):
    """Endpoint URLs discovered from the selected runtime."""

    model_config = ConfigDict(extra="forbid")

    mode: InstallMode
    grafana_url: str | None = None
    gateway_url: str | None = None
    prometheus_url: str | None = None
    loki_url: str | None = None
    tempo_url: str | None = None
    source: str = "best-effort"
    warnings: list[str] = Field(default_factory=list)


def discover_endpoints(mode: InstallMode, *, cwd: Path | None = None) -> DiscoveredEndpoints:
    """Discover observability endpoints for the given install mode."""

    root = cwd or Path.cwd()
    if mode == "compose":
        return _discover_compose(root)
    if mode == "cos":
        return _discover_cos(root)
    return _discover_k8s(root)


def write_user_config(
    endpoints: DiscoveredEndpoints,
    *,
    path: Path | None = None,
) -> Path:
    """Write ~/.sentinel/config.yaml using the existing AppConfig pydantic schema."""

    config_path = path or Path.home() / ".sentinel" / "config.yaml"
    existing = _load_existing_config(config_path)

    app_config = AppConfig.model_validate(existing)
    grafana_url = endpoints.grafana_url
    gateway_url = endpoints.gateway_url

    update = app_config.model_dump(mode="json")
    if grafana_url:
        update["grafana"]["enabled"] = True
        update["grafana"]["base_url"] = grafana_url
    if gateway_url:
        update["observability_gateway"]["enabled"] = True
        update["observability_gateway"]["base_url"] = gateway_url
        update["observability_gateway"]["token_env"] = "SENTINEL_OBSERVABILITY_GATEWAY_TOKEN"

    validated = AppConfig.model_validate(update)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.safe_dump(validated.model_dump(mode="json"), sort_keys=False),
        encoding="utf-8",
    )
    return config_path


def discover_and_write_config(
    mode: InstallMode,
    *,
    cwd: Path | None = None,
    path: Path | None = None,
) -> tuple[DiscoveredEndpoints, Path]:
    endpoints = discover_endpoints(mode, cwd=cwd)
    return endpoints, write_user_config(endpoints, path=path)


def _discover_compose(root: Path) -> DiscoveredEndpoints:
    warnings: list[str] = []
    compose_dir = _compose_dir(root)
    urls = {
        "grafana_url": _compose_port_url(compose_dir, "grafana", DEFAULT_PORTS["grafana"], warnings),
        "gateway_url": _compose_port_url(
            compose_dir, "sentinel-gateway", DEFAULT_PORTS["gateway"], warnings
        ),
        "prometheus_url": _compose_port_url(
            compose_dir, "prometheus", DEFAULT_PORTS["prometheus"], warnings
        ),
        "loki_url": _compose_port_url(compose_dir, "loki", DEFAULT_PORTS["loki"], warnings),
        "tempo_url": _compose_port_url(compose_dir, "tempo", DEFAULT_PORTS["tempo"], warnings),
    }
    return DiscoveredEndpoints(
        mode="compose",
        source=f"docker compose port ({compose_dir})",
        warnings=warnings,
        **_with_defaults(urls),
    )


def _discover_cos(root: Path) -> DiscoveredEndpoints:
    warnings: list[str] = []
    urls = _discover_k8s_services(warnings)
    juju_urls = _discover_juju_status(warnings)
    urls = {**urls, **{key: value for key, value in juju_urls.items() if value}}
    return DiscoveredEndpoints(
        mode="cos",
        source="juju status/kubectl get svc",
        warnings=warnings,
        **_with_defaults(urls),
    )


def _discover_k8s(root: Path) -> DiscoveredEndpoints:
    warnings: list[str] = []
    urls = _discover_k8s_services(warnings)
    return DiscoveredEndpoints(
        mode="k8s",
        source="kubectl get svc",
        warnings=warnings,
        **_with_defaults(urls),
    )


def _discover_k8s_services(warnings: list[str]) -> dict[str, str | None]:
    kubectl = _kubectl_command()
    if kubectl is None:
        warnings.append("kubectl veya microk8s kubectl bulunamadi.")
        return {}

    result = _run([*kubectl, "get", "svc", "-A", "-o", "json"])
    if result.returncode != 0:
        warnings.append("kubectl get svc basarisiz oldu.")
        return {}

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        warnings.append("kubectl get svc JSON parse edilemedi.")
        return {}

    urls: dict[str, str | None] = {}
    for item in payload.get("items", []):
        name = item.get("metadata", {}).get("name", "")
        service_key = _service_key(name)
        if not service_key:
            continue
        url_key = "gateway_url" if service_key == "gateway" else f"{service_key}_url"
        urls.setdefault(url_key, _service_url(item, DEFAULT_PORTS[service_key]))
    return urls


def _discover_juju_status(warnings: list[str]) -> dict[str, str | None]:
    if shutil.which("juju") is None:
        warnings.append("juju bulunamadi.")
        return {}

    model = os.environ.get("SENTINEL_JUJU_MODEL") or os.environ.get("MODEL_NAME") or "cos"
    result = _run(["juju", "status", "--model", model, "--format=json"])
    if result.returncode != 0:
        warnings.append(f"juju status basarisiz oldu: model={model}")
        return {}

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        warnings.append("juju status JSON parse edilemedi.")
        return {}

    urls: dict[str, str | None] = {}
    for name, app in payload.get("applications", {}).items():
        service_key = _service_key(name)
        if not service_key:
            continue
        address = app.get("public-address") or app.get("address")
        if not address:
            continue
        url_key = "gateway_url" if service_key == "gateway" else f"{service_key}_url"
        urls[url_key] = f"http://{address}:{DEFAULT_PORTS[service_key]}"
    return urls


def _compose_dir(root: Path) -> Path:
    env_dir = os.environ.get("SENTINEL_COMPOSE_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()
    if (root / "docker-compose.yaml").exists() or (root / "compose.yaml").exists():
        return root
    return root / "sentinel-compose"


def _compose_port_url(
    compose_dir: Path,
    service: str,
    port: int,
    warnings: list[str],
) -> str | None:
    if shutil.which("docker") is None:
        warnings.append("docker bulunamadi; compose port discovery varsayilanlara dusecek.")
        return None
    if not compose_dir.exists():
        warnings.append(f"compose dizini bulunamadi: {compose_dir}")
        return None

    result = _run(["docker", "compose", "port", service, str(port)], cwd=compose_dir)
    if result.returncode != 0 or not result.stdout.strip():
        warnings.append(f"docker compose port bulunamadi: {service}:{port}")
        return None
    return _host_port_to_url(result.stdout.strip().splitlines()[0], port)


def _host_port_to_url(value: str, default_port: int) -> str:
    host = "127.0.0.1"
    port = default_port
    match = re.search(r"(\[[^\]]+\]|[^:\s]+):(\d+)$", value)
    if match:
        host = match.group(1).strip("[]")
        port = int(match.group(2))
    if host in {"0.0.0.0", "::", ""}:
        host = "127.0.0.1"
    return f"http://{host}:{port}"


def _service_key(name: str) -> str | None:
    normalized = name.lower()
    if "sentinel-gateway" in normalized or "observability-gateway" in normalized:
        return "gateway"
    for key in ("grafana", "prometheus", "loki", "tempo"):
        if key in normalized:
            return key
    return None


def _service_url(item: dict[str, object], default_port: int) -> str | None:
    spec = item.get("spec") if isinstance(item.get("spec"), dict) else {}
    status = item.get("status") if isinstance(item.get("status"), dict) else {}
    ports = spec.get("ports") if isinstance(spec.get("ports"), list) else []
    port = _pick_service_port(ports, default_port)

    lb = status.get("loadBalancer") if isinstance(status.get("loadBalancer"), dict) else {}
    ingress = lb.get("ingress") if isinstance(lb.get("ingress"), list) else []
    if ingress:
        first = ingress[0]
        if isinstance(first, dict):
            host = first.get("ip") or first.get("hostname")
            if host:
                return f"http://{host}:{port}"

    node_port = _pick_node_port(ports, default_port)
    if node_port:
        return f"http://127.0.0.1:{node_port}"

    cluster_ip = spec.get("clusterIP")
    if isinstance(cluster_ip, str) and cluster_ip and cluster_ip != "None":
        return f"http://{cluster_ip}:{port}"
    return None


def _pick_service_port(ports: list[object], default_port: int) -> int:
    for item in ports:
        if not isinstance(item, dict):
            continue
        if item.get("port") == default_port:
            return int(item["port"])
    for item in ports:
        if isinstance(item, dict) and isinstance(item.get("port"), int):
            return int(item["port"])
    return default_port


def _pick_node_port(ports: list[object], default_port: int) -> int | None:
    for item in ports:
        if not isinstance(item, dict):
            continue
        if item.get("port") == default_port and isinstance(item.get("nodePort"), int):
            return int(item["nodePort"])
    for item in ports:
        if isinstance(item, dict) and isinstance(item.get("nodePort"), int):
            return int(item["nodePort"])
    return None


def _with_defaults(urls: dict[str, str | None]) -> dict[str, str]:
    defaults = {
        "grafana_url": f"http://127.0.0.1:{DEFAULT_PORTS['grafana']}",
        "gateway_url": f"http://127.0.0.1:{DEFAULT_PORTS['gateway']}",
        "prometheus_url": f"http://127.0.0.1:{DEFAULT_PORTS['prometheus']}",
        "loki_url": f"http://127.0.0.1:{DEFAULT_PORTS['loki']}",
        "tempo_url": f"http://127.0.0.1:{DEFAULT_PORTS['tempo']}",
    }
    return {key: urls.get(key) or value for key, value in defaults.items()}


def _kubectl_command() -> list[str] | None:
    if shutil.which("kubectl"):
        return ["kubectl"]
    if shutil.which("microk8s"):
        return ["microk8s", "kubectl"]
    return None


def _run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def _load_existing_config(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        return {}
    return loaded
