# ASTRA GOLD — REFERENCE ARCHITECTURE

Status: CANONICAL REFERENCE ARCHITECTURE
Version: 1.1
Date: 2026-10-02
System: MediaHub OS / MediaHub iOS

## 0. Purpose

This document is the normative reference scheme for ASTRA GOLD.
It defines authority, control, execution, transport, provider, model, candidate, evidence,
qualification, recovery and launch boundaries.

The complete component inventory remains in:
`architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md`

Machine-readable gate ids, numeric thresholds, the invariant registry, the
credential lifecycle, the human approval record and executor classes live in:
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`

This reference architecture does not grant qualification to any component.
Runtime qualification requires fresh evidence at the exact source SHA.

## 1. Non-negotiable authority model

Human is the final authority for architecture, production, security and launch.

A0-ASTRA is the single MediaHub coordination and state authority.

A1 owns architecture and contracts.
A2 performs bounded implementation.
A3 performs independent verification.

Executors execute. Providers provide inference. Models infer. Transports transport.
Gateways route. Candidates remain candidates until independently qualified.

No registration, credential, successful request, model discovery result or historical
execution result creates authority.

## 2. Reference topology

    HUMAN / FINAL AUTHORITY
             |
             v
        A0 — ASTRA
             |
      +------+------+
      |      |      |
     A1     A2     A3
      |      |      |
      +------+------+
             |
       CONTROL PLANE
             |
   +---------+----------+
   |                    |
 EXECUTION FABRIC    EVIDENCE FABRIC
   |                    |
   v                    v
Executors          Evidence Store
   |
   +-----------------------------+
   |             |               |
Transport      Gateway         Local Runtime
   |             |               |
   +-------------+---------------+
                 |
          Provider / Model Fabric

Candidate systems, browser tools, discovery tools and security tools connect only
through explicit bounded admission contracts.

## 3. Planes

### 3.1 Authority plane

Components:
- Human
- A0-ASTRA
- A1
- A2
- A3

Invariant:
No lower plane may elevate itself into an authority plane.

### 3.2 Control plane

Responsibilities:
- command ingestion;
- mission decomposition;
- dependency ordering;
- queue management;
- claim and lease management;
- heartbeat and liveness;
- duplicate-controller rejection;
- stale-claim detection;
- conflict detection;
- result publication;
- integration;
- architecture reconciliation;
- state transitions.

### 3.3 Execution plane

**Current qualification harness (temporary test-lab mapping, not final hardware topology):**
- mh-dev-01 -> Claude;
- mh-dev-02 -> Claude;
- Voktors-Mac-mini.local -> Claude (the M2 is the first MediaHub product prototype and must not remain a permanent developer lane after target commissioning).

The current queue code and G-5 configuration permit three test claims. This reflects the existing lab harness only. The target plan approved on 2026-10-12 has two development hosts: the purchased Mac Pro (developer host #1 / primary MediaHub target) and a Mac mini Mid-2011 running Linux with a planned 16 GB RAM configuration (developer host #2). At target commissioning, node IDs, queue bindings, governance/schema thresholds and topology tests must be reconciled to this hardware. The initial target concurrency ceiling is two physical hosts; raising it requires separately verified isolated logical lanes and capacity evidence. The M2 remains a product prototype, not a target ASTRA developer server. The future GPU/video server is a separate optional compute pool and does not automatically become an executor lane.

Broader executor/transport combinations may remain in qualification catalogs, but they are not a statement that the target hardware has already been acquired or deployed.

Any contradiction between this mapping and a task, workflow, claim or evidence record is RECONCILIATION_REQUIRED -> BLOCKED.

Cloud executors are an admitted extension of the execution fabric, not a new
authority plane. A cloud executor path (for example Gemini, DeepSeek or an
OpenRouter gateway) is subject to the same admission ladder, credential
boundary, provider-identity preservation and 23 fresh rounds, and carries only
executor authority. Gateway success never substitutes for native-provider
qualification. Candidate cloud executor paths are enumerated in
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`.

### 3.4 Transport plane

- GitHub Transport;
- FCC;
- OmniRoute.

Transport has no MediaHub State Authority.

### 3.5 Provider plane

Registered provider identities and provider candidates are subject to explicit
authentication, model discovery, non-mutating probe, execution and result validation.

Provider gateways such as OpenRouter, UniRouter, ZeroRouter, NaraRouter and
OrcaRouter are routing surfaces, not MediaHub authorities.

### 3.6 Local model plane

Current reference components:
- Ollama;
- Kimi K3 In-C;
- Gemma 4;
- MiniCPM-V 4.5 8B 1MK.

Model qualification is variant/checkpoint specific.

### 3.7 Auxiliary plane

- ECC;
- Delx Memory Bun.

Auxiliary components may provide context, analysis or diagnostics but cannot own
state, select providers, create credentials or define architecture.

### 3.8 Candidate plane

Candidate components include:
- OpenOPC;
- OpenFlux;
- SoL-Pi;
- Colibri;
- WebTool-DeepSeek;
- DeepSeek Harness;
- Stagewise;
- free-coding-models;
- FreeLLMAPI;
- unlazy;
- naabu;
- codex-chatgpt-web.

Candidates are execution/tooling surfaces only until independently qualified.

## 4. Canonical lifecycle

    DISCOVER
       |
    PREFLIGHT
       |
      ADMIT
       |
    QUALIFY
       |
    EXECUTE
       |
    VERIFY
       |
    INTEGRATE
       |
   RECONCILE
       |
   PRE_SOAK
       |
   SOAK_24H
       |
 LAUNCH_READY
       |
 HUMAN_LAUNCH

Failure path:

    BLOCKED -> DIAGNOSE -> REPAIR -> PREFLIGHT

## 5. Component admission contract

Every component entering runtime qualification must establish:

1. exact identity;
2. source/release/checkpoint provenance;
3. exact source SHA where applicable;
4. dependency integrity;
5. runtime identity;
6. authority boundary;
7. workspace/process isolation;
8. credential boundary;
9. non-mutating probe;
10. functional execution;
11. result validation;
12. timeout behavior;
13. failure behavior;
14. recovery behavior;
15. replay idempotency;
16. concurrency behavior;
17. fresh qualification waves;
18. independent A3 verification.

Identity unresolved means runtime admission is blocked.

## 6. Universal promotion ladder

    REGISTERED
       |
    CREDENTIAL_PRESENT
       |
    AUTH_SUCCESS
       |
    MODEL_DISCOVERY_PASS
       |
    PROBE_PASS
       |
    EXECUTION_PASS
       |
    RESULT_VALIDATION_PASS
       |
    A3_VERIFIED
       |
    ASTRA_GOLD_ELIGIBLE
       |
    LAUNCH_READY
       |
    LAUNCHED

There are no implicit transitions.

## 7. Evidence plane

Each execution result must be traceable to:

- command_id;
- node_id;
- component_id;
- executor_id;
- provider_or_model_id;
- transport_id where applicable;
- source_sha;
- round;
- timestamp;
- exit_status;
- timeout;
- workspace;
- verification_status;
- evidence_digest.

Secrets, tokens, private keys and session credentials are prohibited in evidence.

Historical evidence cannot satisfy a fresh qualification gate.

Evidence for a completed round is immutable. Corrections create a new linked evidence record; prior evidence is never silently rewritten.

## 8. Reconciliation Contract

A0 reconciles architecture vs implementation, registry vs actual identity, claimed state vs evidence state, tested SHA vs source SHA, provider/model identity vs execution evidence, qualification state vs gate state, candidate inventory vs runtime admission, control-plane state vs worker state, and evidence completeness vs required metadata.

Any contradiction produces RECONCILIATION_REQUIRED → BLOCKED. A component may not resolve a contradiction by changing its own authority or evidence.

## 9. Concurrency contract

Maximum autonomous claims: 3. One active claim per permanent executor lane.

Rules:
- claims must be disjoint;
- shared surfaces are serialized;
- one writer owns one mutable surface at a time;
- duplicate controllers are rejected;
- stale leases are recoverable;
- replay must be idempotent.

Parallelism is an execution optimization, never an authority mechanism.

## 10. Recovery contract

Mandatory scenarios:

- executor timeout;
- executor failure;
- transport interruption;
- stale claim;
- worker restart;
- duplicate controller;
- replay;
- result publication failure;
- partial integration;
- reconciliation conflict.

Recovery must return the system to a deterministic state or to BLOCKED.
Silent continuation is prohibited.

## 11. Verification contract

A3 independently checks:

- focused behavior;
- regression;
- contracts;
- architecture conformance;
- security;
- concurrency;
- failure;
- recovery;
- exact-SHA evidence;
- authority boundaries.

A2, executor, provider, model or candidate cannot certify its own qualification.

## 12. Category-specific controls

### Local model

Require:
- exact variant;
- checkpoint provenance;
- runtime backend;
- memory/resource profile;
- reasoning/code probe;
- tool probe;
- multimodal probe when applicable;
- latency and recovery evidence.

### Gateway/router

Require:
- upstream inventory;
- routing transparency;
- credential isolation;
- failover behavior;
- provider identity preservation;
- no hidden MediaHub state.

### Browser bridge

Require:
- browser-session isolation;
- cookie/token boundary;
- tool permission boundary;
- prompt-injection resistance;
- account/session recovery;
- auditability.

### Coding harness / IDE

Require:
- workspace isolation;
- subprocess boundary;
- plugin/extension boundary;
- tool allowlist;
- bounded execution;
- cancellation;
- timeout;
- review/rework integrity;
- worker recovery.

### Security tool

Require:
- explicit target scope;
- permission boundary;
- safe probe/dry-run;
- rate limit;
- audit trail;
- destructive-action prohibition.

### Unresolved identity

No runtime admission.
Exact upstream identity must be resolved first.

## 13. Qualification gates

The canonical gate ids, names and numeric thresholds are defined in
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` and are mirrored by
`architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`.

G0 — Identity
G1 — Boundary
G2 — Control Plane
G3 — Execution Path
G4 — 23-Wave Qualification
G5 — Concurrency
G6 — Recovery
G7 — Integrated A3
G8 — Pre-Soak
G9 — 24H SOAK
G10 — Launch Ready
G11 — Human Launch

Missing, contradictory, stale or failed mandatory evidence produces BLOCKED.

## 14. Pre-soak

Required before 24h soak:
- all mandatory execution paths;
- recovery suite;
- integrated A3;
- fresh evidence;
- clean worktree;
- architecture reconciliation;
- no unresolved qualification blocker.

## 15. 24H SOAK

Required observations:
- continuous heartbeat;
- no unexplained restart;
- no duplicate-claim corruption;
- no unresolved execution failure;
- evidence integrity;
- no authority-boundary violation;
- deterministic recovery behavior.

24H SOAK is a current-state gate, not a historical certification.

## 16. Launch contract

Launch requires:
- G0-G10 PASS;
- exact release SHA;
- complete evidence bundle;
- A3 verification record;
- 24h soak record;
- rollback target;
- Human authorization.

Human launch authorization is required before G11.\n\nG11 is HUMAN_ONLY.

ASTRA may prepare LAUNCH_READY.
ASTRA does not self-authorize production launch.

## 17. Absolute invariants

- No credentials in Git.
- No secrets in evidence.
- No provider State Authority.
- No transport State Authority.
- No model authority by implication.
- No executor architecture authority.
- No candidate self-qualification.
- No candidate self-promotion.
- No A2 self-verification.
- No hidden provider selection.
- No credential creation by auxiliary tooling.
- No launch without independent A3.
- No launch without recovery.
- No launch without current 24H SOAK.
- No qualification from historical evidence.
- No silent transition after contradictory evidence.
- Missing evidence means BLOCKED.

## 18. Reference status semantics

DESIGNED:
architecture exists but runtime admission has not started.

PREFLIGHT:
environment and identity checks are executing.

ADMITTED:
component satisfies admission boundary.

QUALIFICATION:
fresh runtime qualification is active.

VERIFICATION:
independent verification is active.

INTEGRATION:
verified work is being integrated.

RECONCILIATION:
architecture/state/evidence consistency is being checked.

SOAK:
24h observation is active.

GOLD_ACTIVE:
only after current qualification, A3, pre-soak, 24H SOAK and Human launch
requirements are satisfied.

BLOCKED:
a mandatory gate lacks valid evidence or contains a failure/conflict.

## 19. Canonical relationship to existing ASTRA GOLD documents

This document is the reference architecture.

- COMPLETE-COMPONENT-SCHEME = exhaustive component inventory.
- QUALIFICATION-LAUNCH-SCHEMA = executable qualification/launch gate contract.
- UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM = machine-oriented unified system model.
- qualification_launch_gate.py = deterministic gate implementation.
- executor qualification evidence = runtime proof.

No document can override the Human authority rule or the fail-closed invariant.
