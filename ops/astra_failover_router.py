from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable

@dataclass(frozen=True)
class RouteCandidate:
    executor_id: str
    capabilities: frozenset[str]
    healthy: bool
    lease_available: bool
    trust_boundary: str
    transport: str

@dataclass(frozen=True)
class RouteDecision:
    task_id: str
    capability: str
    executor_id: str | None
    reason: str

class FailoverRouter:
    def __init__(self, lease_owner: Callable[[str, str], bool] | None = None):
        self._lease_owner = lease_owner or (lambda _task, _executor: True)

    def select(self, task_id: str, capability: str, candidates: Iterable[RouteCandidate]) -> RouteDecision:
        eligible = [c for c in candidates if capability in c.capabilities and c.healthy and c.lease_available and c.trust_boundary in {"LOCAL_TRUSTED", "ISOLATED_PROXY"} and self._lease_owner(task_id, c.executor_id)]
        eligible.sort(key=lambda c: (c.transport != "local-cli", c.executor_id))
        if not eligible:
            return RouteDecision(task_id, capability, None, "BLOCKED_NO_QUALIFIED_EXECUTOR")
        return RouteDecision(task_id, capability, eligible[0].executor_id, "SELECTED")

    def failover(self, task_id: str, capability: str, candidates: Iterable[RouteCandidate], failed_executor: str) -> RouteDecision:
        return self.select(task_id, capability, [c for c in candidates if c.executor_id != failed_executor])

    def select_inventory(self, task_id: str, capability: str, inventory: dict, external_pr: bool = False) -> RouteDecision:
        candidates = []
        for row in inventory.get("executors", []):
            if row.get("qualification") != "QUALIFIED" or row.get("status") != "HEALTHY":
                continue
            candidate = RouteCandidate(
                str(row["name"]), frozenset(row.get("capabilities", ())), True,
                bool(row.get("lease_available", True)),
                str(row.get("trust_boundary", "LOCAL_TRUSTED")),
                str(row.get("transport", "local-cli")),
            )
            if proxy_policy(candidate, external_pr) == "ALLOW":
                candidates.append(candidate)
        return self.select(task_id, capability, candidates)

def proxy_policy(candidate: RouteCandidate, external_pr: bool) -> str:
    if external_pr and candidate.transport != "local-proxy":
        return "BLOCKED_UNTRUSTED_DIRECT_CREDENTIAL_ACCESS"
    return "ALLOW"
