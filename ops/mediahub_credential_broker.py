"""Fail-closed credential broker for MediaHub development/provider lanes."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class CredentialDenied(PermissionError):
    """Raised when credential access is not explicitly authorized."""


@dataclass(frozen=True)
class CredentialRef:
    provider: str
    name: str
    path: Path


@dataclass
class CredentialBroker:
    """Resolve provider credentials without exposing values to callers."""
    credential_dir: Path
    allowed_providers: frozenset[str]
    authorized: bool = False
    revoked: bool = False

    def authorize(self) -> None:
        if self.revoked:
            raise CredentialDenied("credential broker is revoked")
        if not self.credential_dir.is_dir():
            raise CredentialDenied("credential directory is unavailable")
        self.authorized = True

    def revoke(self) -> None:
        self.authorized = False
        self.revoked = True

    def environment(self, provider: str, variable: str) -> dict[str, str]:
        """Materialize one broker-owned credential only for child-process launch."""
        if not variable.isidentifier() or not variable.isupper():
            raise CredentialDenied("credential environment name is invalid")
        ref = self.resolve(provider)
        try:
            value = ref.path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise CredentialDenied("credential cannot be read") from exc
        if not value or "\x00" in value or len(value) > 16 * 1024:
            raise CredentialDenied("credential value is outside bounds")
        return {variable: value}

    def resolve(self, provider: str) -> CredentialRef:
        if not self.authorized or self.revoked:
            raise CredentialDenied("credential access is not authorized")
        if provider not in self.allowed_providers:
            raise CredentialDenied("provider credential is not allowlisted")
        name = f"mediahub-{provider}"
        path = self.credential_dir / name
        if path.is_symlink() or not path.is_file():
            raise CredentialDenied("credential reference is invalid")
        if path.stat().st_mode & 0o077:
            raise CredentialDenied("credential file permissions are too broad")
        if path.stat().st_size <= 0 or path.stat().st_size > 16 * 1024:
            raise CredentialDenied("credential size is outside bounds")
        return CredentialRef(provider, name, path)
