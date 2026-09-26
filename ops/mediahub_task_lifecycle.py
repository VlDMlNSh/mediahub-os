"""Machine-verifiable autonomous task lifecycle and Definition of Done."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class TaskStage(str, Enum):
    DISCOVER = "DISCOVER"
    PLAN = "PLAN"
    READY = "READY"
    SELECT = "SELECT"
    CLAIM = "CLAIM"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    RECORD = "RECORD"
    COMMIT = "COMMIT"
    PUSH = "PUSH"
    QUALIFY = "QUALIFY"
    CLOSE = "CLOSE"
    GENERATE_NEXT = "GENERATE_NEXT"


STAGE_ORDER = tuple(TaskStage)


@dataclass(frozen=True)
class Evidence:
    task_id: str
    requirement: str
    agent_id: str
    execution_id: str
    model: str
    host: str
    lease_id: str
    generation: int
    changed_files: tuple[str, ...]
    tests: tuple[str, ...]
    test_results: tuple[str, ...]
    qualification_evidence: tuple[str, ...]
    commit: str | None
    push: str | None
    post_verification: str | None
    stage: TaskStage
    status: str

    def validate(self) -> None:
        required = {
            "task_id": self.task_id, "requirement": self.requirement,
            "agent_id": self.agent_id, "execution_id": self.execution_id,
            "model": self.model, "host": self.host, "lease_id": self.lease_id,
        }
        missing = [key for key, value in required.items() if not value]
        if missing or self.generation < 1:
            raise ValueError(f"incomplete task evidence: {missing}")
        if self.stage is TaskStage.CLOSE and not self.done:
            raise ValueError("CLOSE requires a complete Definition of Done")

    @property
    def done(self) -> bool:
        return all((self.changed_files, self.tests, self.test_results,
                    self.qualification_evidence, self.commit, self.push,
                    self.post_verification)) and self.status == "SUCCEEDED"


def validate_stage_transition(current: TaskStage, target: TaskStage) -> None:
    if not isinstance(current, TaskStage) or not isinstance(target, TaskStage):
        raise TypeError("invalid lifecycle stage")
    if target is not current and STAGE_ORDER.index(target) != STAGE_ORDER.index(current) + 1:
        raise ValueError(f"invalid lifecycle transition: {current.value} -> {target.value}")


def verify_done(evidence: Evidence) -> Evidence:
    evidence.validate()
    if evidence.stage is not TaskStage.CLOSE or not evidence.done:
        raise ValueError("task cannot be marked DONE without complete evidence")
    return evidence


def evidence_dict(evidence: Evidence) -> Mapping[str, object]:
    evidence.validate()
    return {
        "task_id": evidence.task_id,
        "requirement": evidence.requirement,
        "agent_id": evidence.agent_id,
        "execution_id": evidence.execution_id,
        "model": evidence.model,
        "host": evidence.host,
        "lease_id": evidence.lease_id,
        "generation": evidence.generation,
        "changed_files": list(evidence.changed_files),
        "tests": list(evidence.tests),
        "test_results": list(evidence.test_results),
        "qualification_evidence": list(evidence.qualification_evidence),
        "commit": evidence.commit,
        "push": evidence.push,
        "post_verification": evidence.post_verification,
        "stage": evidence.stage.value,
        "status": evidence.status,
        "done": evidence.done,
    }
