"""Shared secret-safe text redaction for trajectory, memory, and logs."""

from __future__ import annotations

import re


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# OpenAI-style and generic long tokens
TOKEN_RE = re.compile(r"\b(?:sk|api|token|key|auth)[-_]?[A-Za-z0-9._-]{12,}\b", re.IGNORECASE)
BEARER_RE = re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{8,}")
EXPORT_SECRET_RE = re.compile(
    r"(?i)(export\s+[A-Z0-9_]+\s*=\s*)([^\s\n\"']+|\"[^\"\n]{3,}\"|'[^'\n]{3,}')"
)
ASSIGNMENT_SECRET_RE = re.compile(
    r"(?i)(password|secret|token|api[_-]?key|authorization)\s*[:=]\s*([^\s\n]+)"
)
KUBECONFIG_USER_RE = re.compile(r"(client-key-data|client-certificate-data):\s*\S+")

# PEM blocks
PEM_RE = re.compile(
    r"-----BEGIN [^-]+-----[\s\S]*?-----END [^-]+-----",
    re.MULTILINE,
)


def redact_text(value: str) -> str:
    """Redact common secret patterns; deterministic for tests."""

    value = EMAIL_RE.sub("[redacted-email]", value)
    value = TOKEN_RE.sub("[redacted-token]", value)
    value = BEARER_RE.sub("bearer [redacted]", value)
    value = EXPORT_SECRET_RE.sub(r"\1[redacted-env]", value)
    value = ASSIGNMENT_SECRET_RE.sub(r"\1[redacted]", value)
    value = KUBECONFIG_USER_RE.sub(r"\1: [redacted]", value)
    value = PEM_RE.sub("[redacted-pem]", value)
    return value
