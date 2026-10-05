# Astra Controller Hardening and Distributed Verification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the verified controller/queue contradictions, add a real fail-closed distributed-verification producer, and make autonomous execution evidence-complete without falsely promoting pre-soak checks to GOLD.

**Architecture:** Keep `mh-dev-01` as the sole canonical Astra qualification node and retain HMAC/command/SHA/node binding. Insert a dedicated distributed-verification producer between strict pre-soak verification and queue admission; make it evidence-producing rather than a filename-existence gate. Preserve the separate explicit 24-hour GOLD soak. Harden autonomous queue branch publication so it never rewrites a remote task branch.

**Tech Stack:** Python 3, unittest/pytest, GitHub Actions, Git worktrees, existing MediaHub mesh registry/heartbeat contracts.

**Spec:** `docs/superpowers/specs/2026-10-05-autonomous-distributed-verification-design.md`

## Global Constraints

- Canonical execution node: `mh-dev-01`.
- Runner identity: `mediahub-runner`.
- No manual queue execution.
- No stale/replayed evidence acceptance.
- Every accepted result binds `command_id`, `target_sha`, `node_id`, phase, status, and return code.
- GitHub Actions success is not qualification evidence.
- Existing HMAC authority boundary remains mandatory.
- No duplicate GOLD worker launch.
- No force-push, rebase, reset, or history rewrite on task branches.
- Missing or mismatched evidence => BLOCKED.

## Review Focus

- Distributed producer must reject missing/mismatched command, node, or target SHA instead of synthesizing PASS.
- Pre-soak readiness must not be reported as GOLD qualification.
- Task branch publication must fail closed rather than rewrite an existing remote branch.
- Worker selection must remain bounded and deterministic.
- Queue evidence must expose branch/worktree/head SHA and complete lifecycle.

### Task 1: Add deterministic distributed verification producer

**Files:**
- Create: `ops/qualification/produce_distributed_verification_evidence.py`
- Test: `tests/test_distributed_verification.py`

**Interfaces:**
- Consumes: environment `ASTRA_COMMAND_ID`, `ASTRA_NODE_ID`, `ASTRA_TARGET_SHA`; current git HEAD; existing mesh node/heartbeat contracts.
- Produces: JSON with schema, command_id, node_id, target_sha, producer_identity, phase, status, returncode, captured_at, checks, blocked_reasons.

- [ ] **Step 1: Write the failing tests**
  - Verify missing authority context returns BLOCKED/non-zero.
  - Verify mismatched current HEAD/target SHA returns BLOCKED/non-zero.
  - Verify a valid local canonical observation can produce PASS only when all required node observations are present and independently attributable.
  - Verify no PASS is produced from stale historical evidence.
- [ ] **Step 2: Run the focused tests and confirm they fail for the missing producer contract.**
- [ ] **Step 3: Implement the minimal producer.**
  - Read only non-secret mesh metadata and fresh evidence.
  - Require exact command/node/target SHA.
  - Require node identity `mh-dev-01` and fresh canonical heartbeat/registry observations.
  - Never synthesize remote-node PASS from absent evidence.
- [ ] **Step 4: Run focused tests; expect PASS.**
- [ ] **Step 5: Run the full Python test suite.**
- [ ] **Step 6: Commit the producer and tests.**

### Task 2: Correct controller phase semantics

**Files:**
- Modify: `astra_github_agent.py`
- Test: `tests/test_astra_github_agent.py` or nearest existing controller test module.

**Interfaces:**
- Consumes: producer from Task 1.
- Produces: controller result that reports distributed_verification before queue; never reports pre-soak readiness as GOLD.

- [ ] **Step 1: Write failing regression tests for the current false-GOLD behavior and missing producer binding.**
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Replace filename-presence discovery with explicit producer invocation and authority environment binding.**
- [ ] **Step 4: Remove pre-queue use of `astra_gold_executor.py` as a GOLD authority; use it only where its contract is explicitly pre-soak/test validation.**
- [ ] **Step 5: Require producer JSON PASS with exact command_id/node_id/target_sha before entering the queue.**
- [ ] **Step 6: Verify GREEN with focused and full tests.**
- [ ] **Step 7: Commit.**

### Task 3: Harden autonomous queue branch publication

**Files:**
- Modify: `runtime/mediahub_runtime/autonomous_queue.py`
- Test: `tests/test_autonomous_queue.py`

**Interfaces:**
- Consumes: READY tasks and current main SHA.
- Produces: isolated task branch, normal non-force push, evidence with branch/worktree/head SHA.

- [ ] **Step 1: Write failing tests proving bounded worker selection, deterministic task worktree paths, and no force-push argument.**
- [ ] **Step 2: Verify RED.**
- [ ] **Step 3: Implement normal push semantics using a unique attempt-scoped branch derived from task ID and base SHA, without remote history rewrite.**
- [ ] **Step 4: Make worker count explicitly bounded by `MAX_WORKERS` and expose selected task IDs in queue evidence.**
- [ ] **Step 5: Verify GREEN and run the full suite.**
- [ ] **Step 6: Commit.**

### Task 4: Fix canonical runner routing contract

**Files:**
- Modify: `.github/workflows/astra-autonomous-supervisor.yml`
- Modify: `.github/workflows/astra-gold-24h-soak.yml`
- Test: existing workflow/config verification tests where applicable.

**Interfaces:**
- Consumes: repository-side runner label contract.
- Produces: jobs targeted by a unique canonical runner label plus retained hostname/user fail-closed checks.

- [ ] **Step 1: Add a repository contract test requiring the unique canonical runner label in the authoritative workflows.**
- [ ] **Step 2: Verify RED against the current generic `self-hosted/linux/x64` and stale `mediahub-runner` forms.**
- [ ] **Step 3: Update workflows to a single canonical label constant documented in the repository.**
- [ ] **Step 4: Verify YAML/test checks.**
- [ ] **Step 5: Commit.**
- Note: physical runner registration must separately carry that label; repository changes cannot create a GitHub self-hosted runner label.

### Task 5: End-to-end autonomous verification wave

**Files:** no production source changes unless a fresh failure identifies a new root cause.

- [ ] Run focused tests.
- [ ] Run full suite.
- [ ] Verify canonical runner admission.
- [ ] Trigger one normal supervisor execution through GitHub.
- [ ] Verify fresh distributed evidence.
- [ ] Verify exact command/node/SHA binding.
- [ ] Verify queue lifecycle and `MH25-QUEUE-002` evidence.
- [ ] Verify A2/A3/commit/push/VERIFIED evidence.
- [ ] Verify final supervisor gate.
- [ ] Keep GOLD 24h soak separate and explicit.

## Completion Contract

The project is not called GOLD or error-free unless fresh execution evidence proves every applicable acceptance criterion. Any unavailable runner label, disabled node, unavailable executor, or missing fresh 3-node evidence remains explicitly BLOCKED.