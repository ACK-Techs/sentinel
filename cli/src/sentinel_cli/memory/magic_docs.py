"""Update MAGIC DOC markers with redacted session summaries."""

from __future__ import annotations

from pathlib import Path

from sentinel_cli.config import AppConfig
from sentinel_cli.redaction import redact_text


def _find_markdown_files(root: Path, *, max_files: int) -> list[Path]:
    if not root.exists():
        return []
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if path.is_file():
            files.append(path)
        if len(files) >= max_files:
            break
    return files


def apply_magic_docs(
    config: AppConfig,
    *,
    cwd: str,
    summary: str,
) -> list[str]:
    """Replace Sentinel marker blocks when MAGIC DOC title is present."""

    if not config.magic_docs.enabled:
        return []

    base = Path(cwd).resolve()
    updated: list[str] = []
    safe_summary = redact_text(summary)[:4000]

    for relative in config.magic_docs.roots:
        root = (base / relative).resolve()
        if not str(root).startswith(str(base)):
            continue
        for path in _find_markdown_files(root, max_files=config.magic_docs.max_files):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if config.magic_docs.title_marker not in text:
                continue
            if config.magic_docs.begin_marker not in text or config.magic_docs.end_marker not in text:
                continue
            before, rest = text.split(config.magic_docs.begin_marker, 1)
            _, after = rest.split(config.magic_docs.end_marker, 1)
            middle = f"\n{safe_summary}\n"
            new_text = (
                before
                + config.magic_docs.begin_marker
                + middle
                + config.magic_docs.end_marker
                + after
            )
            try:
                path.write_text(new_text, encoding="utf-8")
                updated.append(str(path))
            except OSError:
                continue
    return updated
