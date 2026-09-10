"""Native Codex/Claude launch contract built from qualified CLI prior art.

Only the small provider-neutral launch surface is kept in MediaHub. Provider
credentials remain broker-owned and are injected only at process launch.
"""
from __future__ import annotations

import shutil
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from ops.mediahub_credential_broker import CredentialBroker, CredentialRef
from ops.mediahub_model_registry import ModelRegistry


@dataclass(frozen=True)
class NativeAgentSpec:
    agent: str
    provider: str
    executable_name: str
    credential_env: str
    endpoint_env: str


AGENTS: Mapping[str, NativeAgentSpec] = {
    "codex": NativeAgentSpec("codex", "openai", "codex", "OPENAI_API_KEY", "OPENAI_BASE_URL"),
    "claude": NativeAgentSpec("claude", "anthropic", "claude", "ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL"),
}


class NativeAgentDenied(PermissionError):
    """Raised when a native agent launch is not qualified."""


def require_spec(agent: str) -> NativeAgentSpec:
    try:
        return AGENTS[agent]
    except KeyError as exc:
        raise NativeAgentDenied("agent is not qualified") from exc


def resolve_executable(spec: NativeAgentSpec) -> Path:
    executable = shutil.which(spec.executable_name)
    if executable is None:
        raise NativeAgentDenied("qualified agent executable is unavailable")
    return Path(executable)


def build_command(agent: str, model: str, prompt: str) -> tuple[str, ...]:
    spec = require_spec(agent)
    executable = resolve_executable(spec)
    if not model or not prompt:
        raise NativeAgentDenied("model and prompt are required")
    if agent == "codex":
        return (str(executable), "exec", "--json", "--ephemeral", "--skip-git-repo-check",
                "--sandbox", "workspace-write", "--model", model, prompt)
    return (str(executable), "-p", "--output-format", "json", "--model", model, prompt)


def resolve_launch(agent: str, broker: CredentialBroker, endpoint: str,
                   model: str, registry: ModelRegistry) -> tuple[NativeAgentSpec, CredentialRef, str]:
    spec = require_spec(agent)
    if not endpoint.startswith("https://"):
        raise NativeAgentDenied("native endpoint must use HTTPS")
    registry.require(spec.provider, model)
    ref = broker.resolve(spec.provider)
    resolve_executable(spec)
    return spec, ref, endpoint
