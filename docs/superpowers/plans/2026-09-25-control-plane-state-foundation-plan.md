# MediaHub Control Plane State Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the first testable Control Plane vertical slice for durable orchestration state, without changing MH-04 product-state authority.

**Architecture:** Add an orchestration-only domain model and repository boundary around Node, Agent, Task, Lease, Execution, Event and AuditRecord. Keep domain transitions deterministic and isolate persistence behind an adapter so the existing in-memory MH-04 authority remains untouched. Durable production implementation is gated by the repository's existing persistence authorization.

**Tech Stack:** Python 3, existing MediaHub runtime conventions, pytest, typed dataclasses/enums/protocols; persistence adapter selected only after governance acceptance.

**Spec:** `docs/superpowers/specs/2026-09-25-mediahub-control-plane-design.md`

## Global Constraints

- Control Plane state is orchestration state only; MH-04 remains canonical for MediaHub product/domain state.
- No durable persistence implementation may bypass `architecture/PERSISTENCE-IMPLEMENTATION-GATE-v1.0.md`.
- No worker may mutate authoritative state except through the governed Control Plane contract.
- Claim plus lease creation must be atomic at the persistence boundary.
- Stale lease generations must be rejected.
- Ambiguous ownership must fail closed.
- Every accepted transition must be machine-readable and auditable.

## Review Focus

- Duplicate claim under concurrent workers → task-owned test must prove one owner/generation.
- Stale completion after lease loss → lease-owned test must reject an old generation.
- Restart/replay identity collisions → event/idempotency tests must make repeated identities harmless.
- Product-state authority leakage → boundary tests must prove orchestration modules cannot replace MH-04 mutation authority.
- Invalid transition injection → state-machine tests must reject illegal edges without mutation.

---

### Task 1: Freeze the orchestration state contract

**Files:**
- Create: `runtime/mediahub_control_plane/__init__.py`
- Create: `runtime/mediahub_control_plane/model.py`
- Test: `tests/control_plane/test_model.py`

**Interfaces:**
- Produces enums `AgentStatus`, `TaskStatus`, `LeaseStatus`.
- Produces immutable records `Node`, `Agent`, `Task`, `Lease`, `Execution`, `Checkpoint`, `Event`, `AuditRecord`.
- Produces `validate_task_transition(current, target)`, `validate_agent_transition(current, target)`, and `validate_lease_transition(current, target)`.

- [ ] **Step 1: Write failing transition tests**

```python
def test_task_rejects_running_to_ready():
    with pytest.raises(ValueError):
        validate_task_transition(TaskStatus.RUNNING, TaskStatus.READY)

def test_lease_rejects_released_to_active():
    with pytest.raises(ValueError):
        validate_lease_transition(LeaseStatus.RELEASED, LeaseStatus.ACTIVE)
```

- [ ] **Step 2: Run `pytest tests/control_plane/test_model.py -q` and verify the missing module/type failure.**
- [ ] **Step 3: Implement enums, immutable records and explicit transition tables; reject unknown edges before mutation.**
- [ ] **Step 4: Run the focused tests and then the existing runtime authority tests.**
- [ ] **Step 5: Commit `feat(control-plane): add orchestration state contract`.**

### Task 2: Define the persistence-independent repository boundary

**Files:**
- Create: `runtime/mediahub_control_plane/repository.py`
- Test: `tests/control_plane/test_repository_contract.py`

**Interfaces:**
- `ControlPlaneRepository.create_task(task) -> Task`
- `ControlPlaneRepository.get_task(task_id) -> Task | None`
- `ControlPlaneRepository.claim_task(task_id, agent_id, generation) -> Lease`
- `ControlPlaneRepository.renew_lease(lease_id, agent_id, generation, expires_at) -> Lease`
- `ControlPlaneRepository.record_execution(execution) -> Execution`
- `ControlPlaneRepository.append_event(event) -> Event`
- `ControlPlaneRepository.append_audit(record) -> AuditRecord`

- [ ] **Step 1: Write contract tests for duplicate task identity, single-owner claim, generation matching and append-only event/audit semantics.**
- [ ] **Step 2: Run the focused contract tests and verify they fail because no repository implementation exists.**
- [ ] **Step 3: Implement an in-memory reference repository strictly for deterministic tests; it must not be presented as durable production persistence.**
- [ ] **Step 4: Verify concurrent claim behavior with two independent repository callers and assert exactly one accepted owner.**
- [ ] **Step 5: Commit `feat(control-plane): define repository contract`.**

### Task 3: Add task dependency and idempotency semantics

**Files:**
- Modify: `runtime/mediahub_control_plane/model.py`
- Create: `runtime/mediahub_control_plane/dependencies.py`
- Test: `tests/control_plane/test_dependencies.py`

**Interfaces:**
- `dependencies_satisfied(task, completed_ids) -> bool`
- `validate_dependency_graph(tasks) -> None`
- `idempotency_identity(task) -> str`

- [ ] **Step 1: Write tests for satisfied dependencies, missing dependencies, cycles and repeated idempotency keys.**
- [ ] **Step 2: Run the focused tests and confirm failure.**
- [ ] **Step 3: Implement graph validation and deterministic dependency evaluation without scheduler side effects.**
- [ ] **Step 4: Run focused tests plus the model suite.**
- [ ] **Step 5: Commit `feat(control-plane): add dependency and idempotency contracts`.**

### Task 4: Add lease fencing and stale-worker protection

**Files:**
- Create: `runtime/mediahub_control_plane/lease.py`
- Modify: `runtime/mediahub_control_plane/repository.py`
- Test: `tests/control_plane/test_lease_fencing.py`

**Interfaces:**
- `LeaseManager.issue(task_id, agent_id, now, ttl) -> Lease`
- `LeaseManager.renew(lease, agent_id, generation, now, ttl) -> Lease`
- `LeaseManager.expire(lease, now) -> Lease`
- `LeaseManager.assert_owner(lease, agent_id, generation, now) -> None`

- [ ] **Step 1: Write tests for valid renewal, expired renewal, wrong agent, stale generation and release.**
- [ ] **Step 2: Run the lease tests and verify failure.**
- [ ] **Step 3: Implement generation/fencing checks and monotonic logical ordering; do not rely on worker wall-clock time for ownership validity.**
- [ ] **Step 4: Add a test proving an old worker cannot complete a task after a newer generation owns it.**
- [ ] **Step 5: Run lease, repository and existing `tests/ai/test_task_lease.py`.**
- [ ] **Step 6: Commit `feat(control-plane): enforce lease fencing`.**

### Task 5: Integrate the existing task-lease primitive without duplicating authority

**Files:**
- Modify: `ops/ai/task_lease.py`
- Create: `tests/control_plane/test_legacy_lease_adapter.py`
- Modify: `docs/ops/control-plane/MASTER-PROMPT-SNAPSHOT-2026-09-18.md` only if the current contract reference requires correction

**Interfaces:**
- Preserve existing public APIs used by `tests/ai/test_task_lease.py`.
- Add a narrow adapter from the legacy lease primitive to the new orchestration lease model; the adapter cannot bypass repository ownership checks.

- [ ] **Step 1: Write compatibility tests that exercise existing callers and the new generation semantics.**
- [ ] **Step 2: Run existing lease tests before modifying implementation and record the baseline.**
- [ ] **Step 3: Add the adapter with no change to MH-04 State Authority.**
- [ ] **Step 4: Run old and new lease suites together.**
- [ ] **Step 5: Commit `refactor(control-plane): bridge existing lease primitive`.**

### Task 6: Qualify the durable persistence gate

**Files:**
- Modify: `architecture/PERSISTENCE-IMPLEMENTATION-GATE-v1.0.md`
- Create: `docs/ops/control-plane/P1-persistence-qualification-2026-09-25.md`
- Test: `tests/control_plane/test_persistence_recovery_contract.py`

**Interfaces:**
- No production database is introduced until the gate is accepted.
- The qualification record must define transaction ordering, crash consistency, restart source of truth, migrations, backup/restore, duplicate/replay behavior and corruption handling for orchestration state.

- [ ] **Step 1: Write failing qualification tests describing required recovery invariants: no silent task loss, no duplicate authoritative completion, stale generation rejection and deterministic replay handling.**
- [ ] **Step 2: Run the tests and document the expected blocked result while the existing gate remains unauthorized.**
- [ ] **Step 3: Produce the qualification record mapping each invariant to evidence required from the eventual durable adapter.**
- [ ] **Step 4: Do not change the gate from BLOCKED to ACCEPTED without explicit governance authorization; record the block as an intentional release gate.**
- [ ] **Step 5: Commit `docs(control-plane): qualify orchestration persistence gate`.**

### Task 7: Vertical-slice integration gate

**Files:**
- Create: `tests/control_plane/test_vertical_slice.py`
- Create: `docs/ops/control-plane/P1-state-foundation-verification-2026-09-25.md`

**Interfaces:**
- Exercise `create task → dependency ready → claim → lease → execution → verify → record → release` against the reference repository.
- Exercise `lease expiry → orphan → recovery decision` without executing a duplicate side effect.

- [ ] **Step 1: Write the complete happy-path and failure-path tests against the repository interfaces.**
- [ ] **Step 2: Run them and verify the missing orchestration service behavior is exposed.**
- [ ] **Step 3: Implement only the smallest coordinator needed for the vertical slice; keep scheduler, API and GitHub adapters out of this task.**
- [ ] **Step 4: Run the vertical slice plus the complete existing control-plane regression selection.**
- [ ] **Step 5: Record command output, commit SHA, test counts and known governance blocks in the verification record.**
- [ ] **Step 6: Commit `test(control-plane): qualify state foundation vertical slice`.**

## Self-review result

Coverage is intentionally limited to the first independently testable subsystem. Full scheduler, worker protocol, API, GitHub, observability, chaos and soak work must be separate plans after this foundation is qualified. No task authorizes bypassing the persistence gate. The plan contains no unresolved implementation placeholder.
