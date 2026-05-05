"""Memory extraction, dream consolidation, and magic docs helpers."""

from sentinel_cli.memory.dream import maybe_run_dream
from sentinel_cli.memory.extract import append_extract
from sentinel_cli.memory.magic_docs import apply_magic_docs
from sentinel_cli.memory.paths import resolve_memory_root

__all__ = ["append_extract", "apply_magic_docs", "maybe_run_dream", "resolve_memory_root"]
