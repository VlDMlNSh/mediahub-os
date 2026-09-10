"""Provider-neutral, fail-closed bridge for isolated development harnesses."""
from __future__ import annotations

import hashlib
import json
import os
import selectors
import signal
import subprocess  # nosec B404 - argv is validated and shell execution is forbidden
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ops.mediahub_credential_broker import CredentialBroker
from ops.mediahub_model_registry import ModelRegistry
from ops.mediahub_native_agent_launcher import build_command, resolve_launch

FORBIDDEN = frozenset({"production", "secrets", "state-authority", "host-filesystem"})
PROVIDERS = frozenset({"codex", "claude"})
ADAPTER_ID = "mediahub.cloud-development-adapter.v1"


class AdapterDenied(PermissionError):
    """Raised when a request is not safe to execute."""


class ProviderProtocolError(RuntimeError):
    """Raised when a provider violates the neutral response contract."""


@dataclass(frozen=True)
class ProviderRequest:
    task_id: str
    provider: str
    prompt: str
    capabilities: frozenset[str] = frozenset()
    egress: frozenset[str] = frozenset()
    timeout_seconds: int = 60
    source_sha: str = ""
    data_class: str = "non-sensitive"


@dataclass(frozen=True)
class SandboxSpec:
    root: Path
    worktree: Path
    max_output_bytes: int = 1_048_576
    max_timeout_seconds: int = 900
    allowed_env: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ProviderResult:
    provider: str
    task_id: str
    status: str
    output: str
    exit_code: int
    provenance: Mapping[str, str]


@dataclass
class CloudDevelopmentAdapter:
    """Policy gate plus provider-neutral subprocess execution boundary.

    The adapter never receives provider credentials. Harness CLIs are invoked
    with an explicit argv, a minimal environment and a sandbox working tree.
    Network access is an infrastructure policy, not something this class may
    widen or bypass.
    """

    authorized: bool = False
    revoked: bool = False
    allowed_egress: frozenset[str] = frozenset()
    allowed_providers: frozenset[str] = PROVIDERS
    audit_events: list[dict[str, str]] = field(default_factory=list)

    def authorize(self, allowed_egress: frozenset[str] = frozenset()) -> None:
        if self.revoked:
            raise AdapterDenied("adapter is revoked")
        self.allowed_egress = frozenset(allowed_egress)
        self.authorized = True
        self._audit("authorized", egress=sorted(self.allowed_egress))

    def revoke(self) -> None:
        self.revoked = True
        self.authorized = False
        self._audit("revoked")

    def admit(self, request: ProviderRequest) -> None:
        if not self.authorized or self.revoked or not request.task_id:
            raise AdapterDenied("request is not authorized")
        if request.provider not in self.allowed_providers:
            raise AdapterDenied("provider is not allowlisted")
        if request.capabilities & FORBIDDEN:
            raise AdapterDenied("forbidden capability")
        if request.egress - self.allowed_egress:
            raise AdapterDenied("egress is not allowlisted")
        if not 1 <= request.timeout_seconds <= 900:
            raise AdapterDenied("timeout is outside the bounded policy")
        if request.data_class in {"secret", "credential", "production"}:
            raise AdapterDenied("data class is not exportable")
        if not request.source_sha:
            raise AdapterDenied("source provenance is required")
        if not request.prompt or len(request.prompt.encode()) > 64 * 1024:
            raise AdapterDenied("prompt is empty or exceeds the bounded size")
        self._audit("admitted", task_id=request.task_id, provider=request.provider)

    def provenance(self, request: ProviderRequest) -> dict[str, str]:
        self.admit(request)
        return {
            "adapter_id": ADAPTER_ID,
            "task_id": request.task_id,
            "source_sha": request.source_sha,
            "provider": request.provider,
            "request_sha256": hashlib.sha256(request.prompt.encode()).hexdigest(),
        }

    def execute(self, request: ProviderRequest, sandbox: SandboxSpec,
                command: Sequence[str], extra_env: Mapping[str, str] | None = None) -> ProviderResult:
        self.admit(request)
        self._validate_sandbox(sandbox)
        argv = tuple(command)
        if not argv or any(not isinstance(x, str) or not x for x in argv):
            raise AdapterDenied("provider command must be a non-empty argv")
        if any(x in {"--dangerously-skip-permissions", "--full-auto", "--yolo"} for x in argv):
            raise AdapterDenied("unsafe provider mode is forbidden")

        env = {k: os.environ[k] for k in sandbox.allowed_env if k in os.environ}
        if extra_env:
            env.update(extra_env)
        env.update({"MEDIAHUB_ADAPTER_ID": ADAPTER_ID, "MEDIAHUB_TASK_ID": request.task_id})
        started = time.monotonic()
        proc = subprocess.Popen(  # nosec B603 - argv is explicit, shell=False, sandbox cwd
            argv,
            cwd=sandbox.worktree,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=False,
            start_new_session=True,
        )
        try:
            output = self._collect_bounded(
                proc, min(request.timeout_seconds, sandbox.max_timeout_seconds), sandbox.max_output_bytes
            )
        except subprocess.TimeoutExpired as exc:
            self._audit("timeout", task_id=request.task_id, provider=request.provider)
            self._terminate_process_group(proc)
            raise AdapterDenied("provider execution timed out") from exc
        except ProviderProtocolError:
            self._terminate_process_group(proc)
            self._audit("output_rejected", task_id=request.task_id)
            raise
        if proc.returncode != 0:
            self._audit("provider_failed", task_id=request.task_id, exit_code=str(proc.returncode))
        else:
            self._audit("provider_completed", task_id=request.task_id,
                        duration_ms=str(int((time.monotonic() - started) * 1000)))
        return ProviderResult(request.provider, request.task_id, "ok" if proc.returncode == 0 else "failed",
                              output, proc.returncode, self.provenance(request))

    @staticmethod
    def _terminate_process_group(proc: subprocess.Popen[bytes]) -> None:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait(timeout=5)

    @staticmethod
    def _collect_bounded(proc: subprocess.Popen[bytes], timeout: int, max_bytes: int) -> str:
        if proc.stdout is None:
            raise ProviderProtocolError("provider stdout is unavailable")
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)
        chunks: list[bytes] = []
        total = 0
        deadline = time.monotonic() + timeout
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(proc.args, timeout)
                events = selector.select(remaining)
                if not events:
                    raise subprocess.TimeoutExpired(proc.args, timeout)
                chunk = os.read(proc.stdout.fileno(), min(65536, max_bytes - total + 1))
                if chunk:
                    total += len(chunk)
                    if total > max_bytes:
                        raise ProviderProtocolError("provider output exceeds bounded size")
                    chunks.append(chunk)
                    continue
                if proc.poll() is not None:
                    break
            proc.wait(timeout=max(1, int(max(0, deadline - time.monotonic()))))
        finally:
            selector.close()
        try:
            return b"".join(chunks).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ProviderProtocolError("provider output is not valid UTF-8") from exc

    def _validate_sandbox(self, sandbox: SandboxSpec) -> None:
        if sandbox.root.is_symlink() or sandbox.worktree.is_symlink():
            raise AdapterDenied("sandbox paths must not be symlinks")
        root = sandbox.root.resolve()
        worktree = sandbox.worktree.resolve()
        if root == Path("/") or worktree == Path("/"):
            raise AdapterDenied("invalid sandbox root")
        if root not in worktree.parents and worktree != root:
            raise AdapterDenied("worktree escapes sandbox root")
        if not root.is_dir() or not worktree.is_dir():
            raise AdapterDenied("sandbox/worktree must exist")
        if sandbox.max_output_bytes <= 0 or sandbox.max_timeout_seconds <= 0:
            raise AdapterDenied("sandbox limits must be positive")

    def _audit(self, event: str, **fields: object) -> None:
        record = {"event": event}
        record.update({k: json.dumps(v, sort_keys=True) if isinstance(v, (list, dict)) else str(v)
                       for k, v in fields.items()})
        self.audit_events.append(record)

    def execute_native_agent(self, request: ProviderRequest, sandbox: SandboxSpec,
                             broker: CredentialBroker, registry: ModelRegistry,
                             model: str, endpoint: str, streaming: bool = False) -> ProviderResult:
        """Launch a qualified native Codex/Claude CLI through the adapter boundary."""
        self.admit(request)
        if endpoint not in request.egress or endpoint not in self.allowed_egress:
            raise AdapterDenied("native endpoint is not allowlisted for this request")
        spec, _ref, _endpoint = resolve_launch(request.provider, broker, endpoint, model, registry)
        command = build_command(request.provider, model, request.prompt, streaming=streaming)
        env = broker.environment(spec.provider, spec.credential_env)
        env[spec.endpoint_env] = endpoint
        return self.execute(request, sandbox, command, extra_env=env)

    def execute_provider(self, request: ProviderRequest, sandbox: SandboxSpec) -> ProviderResult:
        """Execute only the allowlisted provider wrapper inside the sandbox."""
        command = ENTRYPOINTS.get(request.provider)
        if command is None or not command.is_file() or not os.access(command, os.X_OK):
            raise AdapterDenied("provider entrypoint is unavailable")
        return self.execute(
            request,
            sandbox,
            (str(command), request.prompt, str(sandbox.worktree)),
        )


# Legacy wrappers are retained only for compatibility tests. Native execution
# must use mediahub_native_agent_launcher and never an OpenRouter-bound wrapper.
ENTRYPOINTS: dict[str, Path] = {}
