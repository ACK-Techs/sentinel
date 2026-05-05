"""Resolve Sentinel memory root under policy and optional explicit directory."""

from __future__ import annotations

import hashlib
from pathlib import Path

from sentinel_cli.config import MemorySettings


def resolve_project_key(cwd: str) -> str:
    absolute = str(Path(cwd).resolve())
    return hashlib.sha256(absolute.encode("utf-8")).hexdigest()[:12]


def resolve_memory_root(settings: MemorySettings, *, cwd: str) -> Path:
    """Return absolute memory directory path (mkdir not implied here)."""

    if settings.directory is not None:
        return Path(settings.directory).expanduser().resolve()

    base_cwd = Path(cwd).resolve()
    if settings.policy == "project":
        return base_cwd / ".sentinel" / "memory"

    key = resolve_project_key(cwd)
    return Path.home() / ".sentinel" / "projects" / key / "memory"


def ensure_within_memory_root(memory_root: Path, target: Path) -> Path:
    """Raise PermissionError if target escapes memory_root."""

    root = memory_root.resolve()
    resolved = target.resolve()
    if not str(resolved).startswith(str(root)):
        raise PermissionError("Path escapes Sentinel memory root.")
    return resolved
