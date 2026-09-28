"""Security boundary for Astra durable memory.

Secret-like values are rejected before persistence and redacted again at
context-export boundaries as defense in depth.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(?:api[_ -]?key|access[_ -]?token|secret|password)\s*[:=]\s*[^\s,;]+", re.I),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.I),
    re.compile(r"\bx-api-key\s*:\s*[^\s,;]+", re.I),
)

_REDACTION = "[REDACTED_SECRET]"


@dataclass(frozen=True)
class SecretScan:
    detected: bool
    redacted: str


def scan_secret(value: str | None) -> SecretScan:
    text = "" if value is None else str(value)
    redacted = text
    detected = False
    for pattern in _SECRET_PATTERNS:
        redacted, count = pattern.subn(_REDACTION, redacted)
        detected = detected or count > 0
    return SecretScan(detected, redacted)


def require_safe(value: str | None, field: str) -> str | None:
    scan = scan_secret(value)
    if scan.detected:
        raise ValueError(f"secret_like_value_rejected:{field}")
    return None if value is None else str(value)


def redact(value: str | None) -> str:
    return scan_secret(value).redacted


__all__ = ["SecretScan", "redact", "require_safe", "scan_secret"]
