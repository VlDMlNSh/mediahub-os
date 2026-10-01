"""Fail-closed local Codex/Claude executor control boundary."""
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping
from ops.cloud_development_adapter import CloudDevelopmentAdapter, ProviderRequest, ProviderResult, SandboxSpec
@dataclass(frozen=True)
class LocalExecutorSpec:
    provider: str
    command_env: str
    default_command: str
SPECS: Mapping[str, LocalExecutorSpec] = {"codex": LocalExecutorSpec("codex","MEDIAHUB_CODEX_EXECUTOR","codex"), "claude": LocalExecutorSpec("claude","MEDIAHUB_CLAUDE_EXECUTOR","claude")}
class LocalExecutorDenied(PermissionError): pass
def command_for(provider: str) -> str:
    if provider not in SPECS: raise LocalExecutorDenied("provider is not allowlisted")
    spec=SPECS[provider]; command=os.environ.get(spec.command_env,spec.default_command)
    if not command or "\x00" in command or any(ch in command for ch in "\n\r") or Path(command).name != spec.default_command: raise LocalExecutorDenied("executor command identity is invalid")
    return command
def build_request(task_id: str, provider: str, prompt: str, source_sha: str, *, timeout_seconds: int=900) -> ProviderRequest:
    if not all(isinstance(x,str) and x for x in (task_id,provider,prompt,source_sha)) or provider not in SPECS: raise LocalExecutorDenied("task/provider/prompt/source identity is required")
    return ProviderRequest(task_id=task_id,provider=provider,prompt=prompt,source_sha=source_sha,timeout_seconds=timeout_seconds)
def execute(adapter: CloudDevelopmentAdapter, request: ProviderRequest, sandbox: SandboxSpec) -> ProviderResult:
    command_for(request.provider)
    raise LocalExecutorDenied("qualified native launch admission is required")
