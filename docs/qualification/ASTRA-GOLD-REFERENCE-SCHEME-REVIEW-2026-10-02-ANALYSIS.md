# ASTRA GOLD — Reference Scheme Review (Hybrid Distributed Development)

Status: ANALYTICAL REVIEW / NO GATE PROMOTED
Date: 2026-10-02
Scope: canonical reference scheme of the hybrid distributed development system
Repository: VlDMlNSh/mediahub-os
Author: repository analysis pass (repository-local; no live evidence produced)

## 0. Method and boundaries

This review is analytical. It reads the canonical architecture documents and
compares them against what actually exists in the repository. It does **not**
advance any qualification gate. Provider authentication, the G4 115-round
matrix, integrated A3 verification and the 24h soak are live, credentialed,
exact-SHA operations and are explicitly out of scope.

Sources inspected:

- `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md` (canonical reference, v1.1)
- `architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md` (unified model, v1.0)
- `architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md` (component inventory)
- `docs/checkpoints/2026-10-02-astra-gold-qualification-launch-reference.md`
- `docs/checkpoints/2026-10-02-astra-gold-hybrid-component-reconciliation.md`
- `docs/checkpoints/mh-25-two-node-autonomous-topology-1.0.md`
- `docs/checkpoints/mh-25-dual-local-executor-qualification-checkpoint-2026-10-02.md`
- `docs/qualification/ASTRA-GOLD-PROJECT-AUDIT-2026-10-02.md`
- `docs/qualification/ASTRA-GOLD-LOCAL-QUALIFICATION-RESULT-2026-10-02.md`
- `docs/qualification/ASTRA-GOLD-24H-RUNBOOK.md`
- Actual repository tree: `control/`, `ops/`, `runtime/mediahub_runtime/`,
  `.github/` (27 workflows), `tests/`, 123 Python files.

## 1. What the reference scheme is (summary)

ASTRA GOLD is the **complete distributed autonomous development system**, not a
name for the Astra coordinator alone. It is the integrated control, execution,
verification, transport, provider, evidence, recovery, queue, security and
observability fabric used to develop MediaHub autonomously.

Core elements:

- **Authority model:** `Human > A0 (Astra) > {A1, A2, A3}`; executors, providers,
  models, transports, gateways and candidates never gain MediaHub authority by
  registration or use.
- **Planes:** authority, control, execution, transport, provider, local model,
  auxiliary, candidate.
- **Canonical lifecycle:** `DISCOVER → PREFLIGHT → ADMIT → QUALIFY → EXECUTE →
  VERIFY → INTEGRATE → RECONCILE → PRE_SOAK → SOAK_24H → LAUNCH_READY →
  HUMAN_LAUNCH`; failure path `BLOCKED → DIAGNOSE → REPAIR → PREFLIGHT`.
- **Gates:** G0–G11 (G11 is HUMAN_ONLY).
- **Promotion ladder:** `REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS →
  MODEL_DISCOVERY_PASS → PROBE_PASS → EXECUTION_PASS → RESULT_VALIDATION_PASS →
  A3_VERIFIED → ASTRA_GOLD_ELIGIBLE → LAUNCH_READY → LAUNCHED`.
- **Topology:** mh-dev-02 (16 GiB) = A0 GitHub Transport controller;
  mh-dev-01 (8 GiB) = execution node; Voktors-Mini.Dlink (macOS) = discovery/control.
- **Mandatory executor matrix:** Codex+FCC, Claude Code+FCC, Codex+OmniRoute,
  Claude Code+OmniRoute, Claude Code direct/native = 23 rounds each = 115 rounds.
- **17 admission items** (identity, provenance, SHA, dependency integrity,
  runtime identity, authority boundary, workspace isolation, credential
  boundary, non-mutating probe, functional execution, result validation,
  timeout, failure, recovery, replay idempotency, concurrency, fresh waves,
  independent A3).
- **16 absolute invariants** (no credentials in Git, no secrets in evidence, no
  provider/transport State Authority, no model authority by implication, no
  executor architecture authority, no candidate self-qualification, no A2
  self-verification, no launch without independent A3 / recovery / current 24H
  SOAK, no qualification from historical evidence, no silent transition after
  contradictory evidence, missing evidence means BLOCKED).

---

## 2. What is done well

### 2.1 Authority model is genuinely strict

`Human > A0 > {A1, A2, A3}` is stated explicitly and the invariant "no lower
plane may elevate itself into an authority plane" is repeated without
contradiction across Reference, Unified and Component-Scheme documents. This is
rare: authority normally erodes as a system grows. Here it is defended at every
layer (executor, transport, provider, model, candidate).

### 2.2 Fail-closed by default

"Missing evidence means BLOCKED" and "There is no implicit PASS." A gate cannot
be satisfied by documentation text, registration, credential presence, process
visibility or historical evidence. This is the correct defence against the
dominant risk of autonomous systems: green-by-inertia.

### 2.3 Test / qualification / A3 / launch are separated

"A successful test is not qualification; qualification is not launch
authorization." Independent A3 verification, pre-soak, 24h soak and the separate
human G11 decision are distinct stages. This removes the classic
"CI passed → ship to production" failure.

### 2.4 Strong evidence contract

Every result is traceable to `command_id / node_id / component_id / executor_id /
provider_or_model_id / transport_id / source_sha / round / timestamp /
exit_status / timeout / workspace / verification_status / evidence_digest`.
Secrets are prohibited in evidence; completed-round evidence is immutable and
corrections create a new linked record rather than rewriting history. This is a
sound, audit-grade evidence model.

### 2.5 Freshness discipline

"Historical evidence cannot satisfy a fresh qualification gate" plus "no later
gate may inherit PASS from an earlier or historical SHA." This directly treats
the stale-green problem: a gate is a *current-state* claim, not a historical
certification.

### 2.6 Machine-readable core

Gates are not only prose: there is a machine-readable contract plus
deterministic implementations — `ops/qualification/qualification_launch_gate.py`,
`verify_pre_soak_bundle.py`, `verify_integrated_a3.py`,
`capture_pre_soak_evidence.py`, `build_g4_115_manifest.py`. The G4 manifest
(115 rounds = 23 × 5 paths) is a generated artifact, not a hand-maintained list.

### 2.7 Node role separation and fencing

The A0 controller is placed on the higher-memory node and execution on the
lower; concurrency is capped at 2 autonomous claims; "claims disjoint, shared
surfaces serialized, one writer owns one mutable surface at a time"; duplicate
controllers are rejected; stale leases are recoverable; replay must be
idempotent. This is mature multi-node discipline.

### 2.8 Category-specific admission contracts

Distinct requirements exist for local model (variant/checkpoint provenance,
resource profile, reasoning/code/tool/multimodal probes), gateway/router
(upstream inventory, routing transparency, credential isolation, failover,
provider-identity preservation, no hidden state), browser bridge (session and
cookie/token isolation, prompt-injection resistance, account/session recovery),
coding harness/IDE (workspace isolation, subprocess boundary, tool allowlist,
cancellation, timeout, review integrity, worker recovery) and security tool
(explicit target scope, dry-run, rate limit, audit trail, destructive-action
prohibition). Precise and on point.

### 2.9 Repository-level anti-regression guards already exist

Live guard tests are in place: `tests/test_astra_gold_architecture_drift.py`,
`tests/test_astra_gold_soak_pin.py`, `tests/test_repo_hygiene.py` (D1 dormant
register), `tests/static/test_cross_contract.py` (D2 anti-regression). The scheme
actively defends itself against silent drift.

### 2.10 Honest status reporting

Documents do not inflate state: "Architecture: READY; qualification:
NOT_PROVEN; Launch: BLOCKED." The status vocabulary is disciplined —
`PASS / BLOCKED / FAILED / RECONCILIATION_REQUIRED / NOT_APPLICABLE` — with no
implicit promotion.

### 2.11 Reconciliation contract

Any contradiction (architecture vs implementation, registry vs identity, claimed
vs evidence state, tested vs source SHA, qualification vs gate state) produces
`RECONCILIATION_REQUIRED → BLOCKED`, and no component may resolve a contradiction
by changing its own authority or evidence. This closes a subtle but important
loop.

---

## 3. What needs to be added

### 3.1 Live evidence — the central gap

The authoritative model exists, but runtime proof does not. G0–G11 are BLOCKED,
G4 is **0/115** rounds, integrated A3 and the 24h soak have not run. Until fresh
waves are produced at **one frozen SHA**, the system is qualification-ready but
not GOLD. This is not a defect of the scheme; it is the main thing to add.

### 3.2 A single machine-readable gate-id source

There is a real divergence in gate numbering between canonical documents:

- `REFERENCE-ARCHITECTURE` §12: G0 Identity, G1 Boundary, G2 Control Plane,
  G3 Execution Path, G4 23-Wave, G5 Concurrency, G6 Recovery, G7 Integrated A3,
  G8 Pre-Soak, G9 24H SOAK, G10 Launch Ready, G11 Human Launch.
- `UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM` §8: G0 identity, G1 control plane,
  G2 executor fabric, G3 23-wave, G4 concurrency, G5 recovery, G6 integrated
  verification, G7 pre-soak, G8 24h GOLD soak, G9 GOLD_ACTIVE.

These are two incompatible mappings of the same gate names. A single canonical
gate-id source (e.g. under `schemas/` with a generator) should render gate
references in every document, exactly as D2 made `schemas/` canonical for
contracts.

### 3.3 Numeric thresholds

"heartbeat remains fresh" and "stale lease recoverable" have no numbers.
Concrete thresholds are required to make the gates machine-checkable: heartbeat
TTL, lease TTL, max concurrent claims, per-executor timeout budgets, evidence
freshness window, retry/backoff counts.

### 3.4 One generated "current truth status"

The status (NOT_PROVEN / BLOCKED) is duplicated as prose across several
documents and can drift. A single generated artifact (`status.json` /
`CURRENT-TRUTH.md`) should be the only source of current truth, with documents
referencing it.

### 3.5 D1 technical debt — orphan subsystems

Phantom workflows (`mediahub-p0-07-verification.yml`,
`mediahub-p0-08-verification.yml`, `mediahub-bridge.yml`,
`mediahub-live-provider-qualification.yml`) reference non-existent
`runtime/mediahub_runtime/{configuration_policy*, policy_evaluator, plugin_*}.py`
and `tests/runtime/*` (the latter never existed). They are currently only
*registered as dormant*. A build-or-remove decision is required (owner:
A1/Human); otherwise the register lives forever.

### 3.6 Credential lifecycle

Credential boundaries are asserted, but there is no contract for rotation,
expiry or revocation. For 24/7 operation the scheme needs rotation + expiry +
audit, not only "no credentials in Git."

### 3.7 Rollback as an executable mechanism

The launch contract requires a rollback target, but no actual rollback drill or
mechanism exists. A rollback test with evidence is required.

### 3.8 Cost / quota governance as a gate

MH-21 documents cost governance, but admission has no live budget gate. For a
hybrid cloud fabric (OpenRouter / UnoRouter / ZeroRouter / paid APIs) this must
be a gate, not a recommendation.

### 3.9 Executable supply-chain provenance

MH-12 describes supply-chain security, but there is no automated verification
(SBOM, artifact signing, dependency pinning) as part of G1/G3.

### 3.10 Human-in-loop approval record

G11 is "HUMAN_ONLY", but it is not specified *where and how* authorization is
recorded (who, when, target SHA, rollback target, signed approval). An
approval-record contract is needed.

### 3.11 Runtime infrastructure readiness

Both registered self-hosted runners (`mh-dev-01-v2`, `Voktors-Mini-Astra-Control`)
are OFFLINE, so every `[self-hosted, mediahub-runner]` job queues indefinitely.
Resilience is required — hosted-runner fallback or an HA self-hosted scheme —
otherwise the scheme is physically unexecutable.

### 3.12 Live pre-soak bundle

`evidence/provider-model.json` is stale and lacks a top-level `status`
(blocks G8). Fresh producers for scheduler/fencing/recovery/backup-restore exist
(`produce_runtime_prereq_evidence.py`) but must run on the canonical node.

---

## 4. What could be strengthened

### 4.1 Invariants → enforced registry

The 16 invariants are currently theses. Some are already guarded by drift tests;
coverage should extend until **every invariant maps to an automated test**, so an
invariant cannot be violated without a red CI.

### 4.2 Chaos / fault-injection as code

Recovery scenarios are enumerated (timeout, executor failure, transport
interruption, stale claim, worker restart, duplicate controller, replay, result
publication failure, partial integration, reconciliation conflict). A generated
fault-injection harness — not a checklist — would strengthen G6 materially.

### 4.3 Property-based idempotency tests

Replay/idempotency is critical; cover it with property-based and mutation tests
rather than example-only cases.

### 4.4 Gate observability rollup

Produce a machine-readable rollup of G0–G11 + invariants + blockers with a
dashboard view, so "current truth" is read from an artifact rather than prose.

### 4.5 JSON-Schema validation of gate outputs

Each gate should emit JSON validated against a schema under `schemas/`, removing
the risk of incompatible formats between producers.

### 4.6 Canonical document hygiene

`REFERENCE-ARCHITECTURE` has out-of-order and duplicated numbering: after §7 the
document jumps to §10, then §8, §9, and **§10 appears twice**. Normalize section
numbering and lock it with a test.

### 4.7 Identity-resolution tooling

Candidates with ambiguous identity (`Colibri`, OpenFlux name variants) require
exact-upstream resolution. This should be a tool, not a manual decision. A bare
github.com reference is not a component identity and cannot enter runtime
qualification.

### 4.8 A canonical minimum path per plane

The candidate inventory is broad; define an explicit reference minimum (one
executor path, one provider, one model) so the 23×5 matrix does not grow
unbounded.

### 4.9 Unified terminology / single normative document

Three documents (Reference v1.1 / Unified v1.0 / Scheme) duplicate the same
content and can drift. Keep Reference as the sole normative document and demote
the others to indices/pointers, so drift becomes structurally impossible — the
same move that resolved D2 for contracts.

### 4.10 Explicit degraded-mode and rollback states

The lifecycle already includes `BLOCKED → DIAGNOSE → REPAIR → PREFLIGHT` and a
`LAUNCHED → ROLLBACK → REQUALIFY` path in the launch reference; wire these into
executable state-machine transitions with evidence, not only prose.

---

## 5. Overall assessment

| Area | Assessment |
|---|---|
| Authority model and invariants | **Strong** — strict, consistent, fail-closed |
| Evidence model and freshness | **Strong** — digest, immutable, SHA/round binding |
| Gates and pipeline | **Good, but gate numbering drifts** (two incompatible mappings) |
| Implementation / guard tests | **Good** — drift/pin/hygiene/cross-contract guards active |
| Live evidence (G0–G11, G4 115, A3, soak) | **Absent** — 0/115, all BLOCKED |
| Operational infrastructure (runners, credentials, canonical node) | **Not ready** — runners offline, no credentials |
| Technical debt | **Manageable** — D2/D3 closed, D1 awaiting decision |

**Conclusion.** The reference scheme is a strong and unusually rigorous
architectural model. Its weakness is not design but the **gap between
"qualification-ready" and "actually proven."** Repository-fixable defects
(F1–F7, D2, D3) are resolved; D1 is tracked and guarded. The critical path to
GOLD is three operational conditions: (1) bring the canonical node and runners
online, (2) supply provider credentials, (3) execute fresh 23×5 waves and the
soak at **one frozen SHA**. In addition, three systemic strengthenings are
recommended: a single gate-id source, numeric thresholds, and a generated
current-truth artifact. No gate is promoted by this document.

## 6. Truth status (unchanged)

- Architecture: READY
- Qualification schema: CANONICAL
- Local repository regression: PASS
- Local execution-fabric qualification: NOT_PROVEN
- Cloud provider qualification: NOT_PROVEN
- G4 23-wave: BLOCKED (0/115)
- Integrated A3: BLOCKED
- 24h soak: NOT_STARTED
- Launch: BLOCKED

`ASTRA_GOLD_ELIGIBLE` is not asserted. No gate was promoted from documentation
or local probes.
