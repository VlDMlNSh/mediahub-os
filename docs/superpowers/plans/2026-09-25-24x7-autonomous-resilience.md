# 24x7 Autonomous Resilience Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the MediaHub autonomous runtime survive controller, supervisor, command-bus, node-worker, host-reboot, stale-process, and execution-failure scenarios while preserving fail-closed behavior and an inspectable evidence trail.

**Architecture:** Keep Astra as the single resident supervisor and keep execution lanes separate. Replace fragile periodic-only recovery with a boot-managed service boundary, add machine-checkable health/recovery evidence, and exercise failure injection against the real processes without introducing an unqualified persistence layer.

**Tech Stack:** Bash, Python 3, systemd, Git, pytest, existing Astra/control-plane components.

**Spec:** `docs/ops/control-plane/ASTRA-PERSISTENCE-CONTRACT-2026-09-25.md` plus the accepted 24x7 operating requirements from the current conversation.

## Global Constraints

- Do not introduce SQLite/Postgres or claim durable persistence.
- Astra remains supervisory; it must not become a second source of truth.
- STOP may halt execution lanes but must not suppress Astra supervision.
- Arbitrary user input must never become shell input.
- Every autonomous mutation remains bounded, reviewable, and git-verifiable.
- Production/release/merge authority remains outside autonomous workers.
- Recovery must fail closed on ambiguous ownership or state.

## Review Focus

- Duplicate Astra/controller processes must be prevented by identity plus locks.
- A stale heartbeat must not cause two live controllers to overlap.
- STOP must preserve supervisory recovery while halting execution.
- Host reboot must restore the resident supervisor without relying on an interactive shell.
- A crashed worker must be fenced by lease generation and produce retry/block evidence.
- A clean empty queue must remain healthy NO_PROGRESS, not failure.

### Task 1: Resident service boundary

**Files:**
- Create: `ops/systemd/mediahub-astra.service`
- Create: `ops/systemd/mediahub-autonomy.target`
- Modify: `ops/astra_orchestrator.py`
- Modify: `ops/astra_guard.sh`
- Test: `tests/control_plane/test_resident_supervision.py`

**Interfaces:**
- The service owns Astra only; Astra reconciles execution components.
- systemd restart policy becomes the first recovery boundary.
- The existing guard remains a secondary process-identity defense.

- [ ] Write tests for service command identity, STOP semantics, and duplicate prevention.
- [ ] Verify tests fail against the current service-less deployment contract.
- [ ] Add the unit with restart-on-failure, boot enablement metadata, bounded resource limits, and explicit working directory.
- [ ] Make Astra heartbeat distinguish supervisor liveness from execution progress.
- [ ] Keep guard behavior compatible with the unit so two supervisors cannot coexist.
- [ ] Run focused tests and shell validation.
- [ ] Commit the slice.

### Task 2: Autonomous evidence journal hardening

**Files:**
- Modify: `ops/astra_orchestrator.py`
- Modify: `ops/autonomous_os_loop.sh`
- Modify: `ops/astra_command_bus.py`
- Test: `tests/control_plane/test_autonomy_evidence.py`

**Interfaces:**
- Each cycle records immutable identifiers: cycle, HEAD, tree, result, reason, and verification outcome.
- Evidence files are operational records, not authoritative task state.

- [ ] Add deterministic cycle result/reason fields.
- [ ] Ensure crash/restart leaves the last complete record readable.
- [ ] Add command-bus idempotency evidence without accepting arbitrary commands.
- [ ] Test interrupted-cycle and duplicate-command cases.
- [ ] Run focused tests and `git diff --check`.
- [ ] Commit the slice.

### Task 3: Failure-injection qualification

**Files:**
- Create: `ops/autonomy_fault_probe.py`
- Create: `tests/control_plane/test_autonomy_fault_probe.py`
- Create: `docs/ops/control-plane/24x7-resilience-qualification-2026-09-25.md`

**Interfaces:**
- Probe only repository-owned processes and bounded temporary state.
- Probe never deletes data, rotates credentials, changes production state, or bypasses STOP.

- [ ] Add probes for Astra restart, controller restart, command-bus restart, stale PID identity, STOP/RESUME, and clean idle.
- [ ] Add recovery assertions for exactly one owner per supervised component.
- [ ] Run probes on mh-dev-01 in a controlled window.
- [ ] Record command, timestamp, before/after PID identity, and recovery result.
- [ ] Classify every scenario PASS/BLOCKED/UNVERIFIED.
- [ ] Commit evidence only when fresh verification supports it.

### Task 4: Reboot/recovery qualification

**Files:**
- Modify: `ops/systemd/mediahub-astra.service`
- Create: `ops/systemd/README.md`
- Modify: `docs/ops/control-plane/24x7-resilience-qualification-2026-09-25.md`

- [ ] Verify the unit is syntactically valid without installing it.
- [ ] Install only after the host-level authorization boundary is available.
- [ ] Enable at boot and verify active/enabled state.
- [ ] Perform a controlled host reboot only when explicitly authorized by the operator.
- [ ] Verify Astra, controller, heartbeat, and evidence continuity after boot.
- [ ] Record RTO/RPO observations without claiming persistence qualification.

### Task 5: Final integrated verification

**Files:**
- Test: `tests/control_plane/test_resident_supervision.py`
- Test: `tests/control_plane/test_autonomy_evidence.py`
- Test: `tests/control_plane/test_autonomy_fault_probe.py`
- Modify: `docs/ops/control-plane/24x7-resilience-qualification-2026-09-25.md`

- [ ] Run the focused autonomy/control-plane regression suite.
- [ ] Run `bash -n` against all modified shell entry points.
- [ ] Run `git diff --check`.
- [ ] Run the full repository test suite.
- [ ] Inspect the final process tree and heartbeat directly on the host.
- [ ] Verify no duplicate supervisor/controller exists.
- [ ] Mark persistence as still BLOCKED unless its separate qualification gate is accepted.
- [ ] Commit only after all applicable evidence is fresh.

## Acceptance

The 24x7 operating mode is considered qualified only when the resident supervisor is boot-managed, duplicate ownership is prevented, supervised processes recover after bounded failure injection, STOP preserves supervision, idle is healthy, evidence survives process restart, and all unqualified persistence claims remain explicitly blocked.
