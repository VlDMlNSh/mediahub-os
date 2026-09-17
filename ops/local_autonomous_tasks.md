# Wave 10 priority: bounded Execution Adapter boundary

Current checkpoint: 9ac6fb5527ed6d27137249174d9821b6387a9f81
R4: 471f709f5633feab7aeb62dd3ea52effad6d2bc4

Primary task: implement the smallest provider-neutral ExecutionProposal contract inside the existing execution boundary. The proposal must carry request identity, workload identity, source provenance and provider identity; validate all fields; and be incapable of network access, credential retrieval, State Authority mutation, Home Assistant access, or real execution.

Acceptance gates:
1. Existing tracked file only for each autonomous increment.
2. Deterministic negative tests for missing proposal identity/provenance/provider.
3. No network/provider execution side effects.
4. No direct State Authority or Home Assistant access.
5. R4 ancestry preserved and worktree clean after each committed increment.
6. Full regression plus ruff/mypy/bandit/pip-audit/semgrep/diff-check.
7. Commit each verified increment; never force-push or rewrite history.
8. Preserve provenance and stop on ambiguity.

Follow-up priority: add focused tests for the ExecutionProposal contract, then connect proposal admission to existing cluster recovery evidence without performing arbitrary real execution.

# Initial priority: controlled Cloud Development adapter and isolated cloud-development sandbox

Before adding any external cloud AI provider, implement and qualify a provider-neutral Cloud Development Adapter and an isolated Cloud Development Sandbox. The adapter MUST be deny-by-default, non-authoritative, policy-gated, auditable, provenance-bound, and incapable of direct access to MediaHub State Authority, Home Assistant authority, production devices, secrets, or unrestricted local filesystem/network.

Required first-wave scope:
1. Define provider-neutral adapter contract: request classification, capability declaration, authorization, data minimization, egress policy, residency/policy checks, timeout/retry, response provenance, audit events, metering, revocation and fail-closed behavior.
2. Define isolated sandbox boundary for cloud-development workloads: separate identity, filesystem/worktree, network egress boundary, credentials broker boundary, resource limits, secret scanning/DLP hook points, artifact/result quarantine and deterministic teardown.
3. Implement only the smallest repository-native contract/adapter/sandbox skeleton justified by the existing architecture; do not add provider-specific bypasses or credentials.
4. Add deterministic unit/negative-path tests for denied authority escalation, denied secret exposure, denied unrestricted egress, denied production access, malformed provider responses, timeout/retry, revocation and sandbox teardown.
5. Record provenance/evidence and preserve R4 ancestry. No release/production authorization.

Second wave is explicitly gated on first-wave tests and security checks: integrate Claude, Codex and other approved available models ONLY through the same Cloud Development Adapter and Sandbox. No direct provider integration into core/runtime authority. Provider access must remain replaceable and policy-controlled.

# Local autonomous engineering queue — canonical passport aligned

The approved MediaHub OS passport is the sole functional baseline. Do not introduce requirements that contradict it.

1. Reconcile AI escalation path: Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI; Mobile Access Layer is access layer, not AI compute tier.
2. Preserve two-app Mobile Access Layer: MediaHub Core and separate Remote Mobile Application; do not collapse them or invent a Mobile AI tier.
3. Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.
4. Preserve Cloud Development AI as corporate-only infrastructure; ordinary users have no direct access. Escalation requires authorization, data minimization, egress/residency, audit and metering.
5. Preserve AI Human Clone as a separate Cloud Development AI subsystem with consent/authorization, provenance, scope, audit and revocation.
6. Preserve Trusted Sources Intelligence Engine as a first-class Cloud Development AI subsystem for discovery, retrieval, verification, provenance, evidence and knowledge.
7. Preserve Home Assistant Core as Smart Home source of truth; MediaHub UI must not bypass HA Core; MediaHub State Authority remains canonical platform authority.
8. Before dependencies: demonstrated capability gap → mature component → license/security/provenance → adapter → benchmark → adoption.
9. Continue contracts, invariants, negative tests, recovery/evidence, adapter boundaries and deterministic validation for AI, cluster, Smart Home and mobile.
10. Independent review remains external evidence. Autonomous agents may prepare evidence but must not self-qualify, unlock release or authorize production.
11. Each downstream change must be small, reproducible, testable, security-checked and provenance-bound. Stop on architectural ambiguity or a hard governance gate.


# Agent queue — 2026-09-18

Queue status: ACTIVE. These are bounded preparation/verification tasks; no release or production authority.

12. **QA/Evidence agent — native execution boundary**
    - Add focused negative tests for `NativeExecutionContract.prepare_headers` malformed credential inputs: wrong types, empty string, bool, and provider mismatch.
    - Verify no network/subprocess/secret retrieval side effects.
    - Work only in an isolated worktree; return evidence and a reviewable commit.

13. **Security/Red-Team agent — execution admission**
    - Review `ops/mediahub_native_execution.py` and its tests for authority escalation, credential leakage, unrestricted egress, malformed provider identity, and provenance bypass.
    - Produce deterministic negative cases only; do not modify State Authority or production paths.

14. **Recovery agent — hybrid lifecycle**
    - Review session/delivery/conversation checkpoint restoration for stale-session, generation-mismatch, duplicate-task, and unknown-result reconciliation cases.
    - Add only isolated tests where a real coverage gap exists; preserve fail-closed semantics.

15. **Cloud adapter agent — readiness audit**
    - Audit Codex/Claude native launcher, cloud development adapter, sandbox, egress gate, and credential broker interfaces.
    - Identify exact blockers to operational cloud-agent activation without requesting or exposing credentials.
    - Produce an activation checklist and negative-test gaps; no provider bypass.

16. **Architecture/Evidence agent — PR #80 reconciliation**
    - Reconcile the local ECC integration state against PR #80's remote head and identify commits/evidence not represented remotely.
    - Do not push, merge, mark ready, or authorize release.

17. **Local performance agent — bounded model lane**
    - Measure the local Qwen autonomous generation latency under the existing timeout and identify safe performance improvements.
    - Do not weaken timeouts, sandboxing, validation, or fail-closed behavior.

Queue execution rule: agents may claim only one item at a time, must work in isolated branches/worktrees, run relevant verification, and emit `PASS`, `FAIL`, `BLOCKED`, or `NO_PROGRESS` evidence. No agent may self-authorize merge, release, production, secrets, VPN, or State Authority mutation.

# MASTER DELIVERY QUEUE — MediaHub OS end-to-end development

Status: ACTIVE / continuous until product-completion gates are satisfied.
Purpose: keep every engineering lane supplied with bounded, non-overlapping, reviewable work from the current baseline through Release Candidate and independent review. This queue is a plan/control artifact; it does not grant release or production authority.

## Operating model

- Control plane: `mediahub-local-autonomous.service` + watchdog + provenance journal.
- Local AI lane: `mediahub-local-ai.service`; local model is advisory and proposal-generating only.
- Hybrid control plane: `mediahub-hybrid-development.service`; session, delivery, conversation, recovery and egress admission are fail-closed.
- Native cloud lanes: Codex/Claude only through the repository-native adapter, sandbox, egress gate, credential broker and provenance boundary. If authentication is absent, lane state is BLOCKED rather than simulated.
- GitHub lane: Actions/PR evidence only; no agent may merge, mark ready, release or authorize production.
- ECC lane: bounded advisory engineering/review roles; never State Authority, release authority or production authority.
- QA/security/recovery lanes: may block downstream work and may add deterministic tests/evidence, but may not bypass gates.
- Human authority: independent review, release authorization and production authorization remain human decisions.

## Permanent scheduler policy

1. Select the highest-priority unblocked item whose prerequisites are satisfied.
2. Claim exactly one bounded item per agent/worktree.
3. Prefer parallel work only when file ownership and dependency graphs do not overlap.
4. Every increment must have a clear acceptance test and provenance.
5. A failing or ambiguous gate creates BLOCKED state and a remediation item; it does not trigger a bypass.
6. After every verified increment: focused tests → regression → security/static checks → diff-check → commit.
7. Reconciliation is mandatory after unknown cloud/agent outcomes; never resend blindly.
8. Re-plan automatically after each committed increment using current HEAD, current tests and current evidence.
9. Do not manufacture cloud-agent activity, CI PASS, review approval, credentials, VPN state or production state.
10. When no code change is justified, produce evidence/coverage work rather than speculative implementation.

## Lane allocation

A. **Architecture / Contract** — contracts, schemas, invariants, compatibility, provenance.
B. **Core / State Authority** — platform authority, persistence, HA, recovery, authorization.
C. **AI / ECC** — provider registry, model routing, adapters, ECC integration and bounded orchestration.
D. **Hybrid / Cloud Development** — session, delivery, egress, sandbox, native Codex/Claude integration.
E. **Mobile** — MediaHub Core mobile access surface + separate Remote Mobile Application.
F. **Smart Home / HA** — Home Assistant integration and source-of-truth boundaries.
G. **Media** — media ingestion, indexing, playback/control and lifecycle contracts.
H. **Documents / Intelligence** — documents, Trusted Sources Intelligence Engine, provenance/evidence.
I. **Voice** — Google Assistant → Яндекс Алиса → Apple Siri integration order and authorization boundaries.
J. **Security / Red Team** — threat modeling, negative tests, secret/DLP checks, egress and authority boundaries.
K. **QA / Verification** — unit/integration/system/recovery/acceptance evidence and reproducibility.
L. **Performance / Reliability** — latency, resource limits, watchdogs, degradation and soak evidence.
M. **Release / Independent Evidence** — RC packaging, SBOM/provenance, reproducible build, external review package; no self-authorization.
N. **Operations / Recovery** — service health, restart semantics, backup/restore, migration and disaster recovery.

## Phase P0 — Baseline and control-plane stabilization

Goal: establish one authoritative work graph and remove autonomous NO_PROGRESS loops caused by missing bounded work.

P0.1 Reconcile current local HEAD, R4 ancestry, functional baseline and active worktrees.
P0.2 Persist this master queue and generate machine-readable ownership/provenance only if justified by existing architecture.
P0.3 Verify supervisor/watchdog restart, lock, checkpoint, rollback and journal semantics.
P0.4 Close current Native Execution Contract test gaps.
P0.5 Close hybrid session/delivery/conversation recovery gaps.
P0.6 Reconcile PR #80 remote/local evidence without push or merge.
P0.7 Audit cloud-agent readiness; if credentials are absent, maintain BLOCKED with exact evidence.
Exit: no unresolved control-plane ambiguity; queue scheduler can continuously select bounded work.

## Phase P1 — Execution and AI foundations

P1.1 Complete provider-neutral `ExecutionProposal` contract and negative tests.
P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.
P1.3 Complete AI model/provider/capability registry verification.
P1.4 Complete provider selector and fallback semantics, including offline/degraded behavior.
P1.5 Complete ECC adapter/dispatcher policy, provenance, permissions and negative tests.
P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.
P1.7 Qualify native Codex and Claude launch specifications without bypasses.
P1.8 Add metering/audit/revocation evidence for cloud-development workloads.
Exit: AI and cloud-development lanes are policy-bounded and testable; operational cloud use remains gated by real credentials/authorization.

## Phase P2 — Core platform authority and HA

P2.1 Inventory State Authority contracts and identify every mutation path.
P2.2 Enforce single-authority mutation boundaries.
P2.3 Complete persistence/versioning/migration/recovery contracts.
P2.4 Complete cluster membership, leader/source-of-truth and failover evidence.
P2.5 Test stale leader, split-brain, duplicate command, replay and recovery scenarios.
P2.6 Verify Home Assistant Core remains Smart Home source of truth and cannot be bypassed.
P2.7 Verify all AI/cloud agents are non-authoritative with respect to State Authority.
Exit: deterministic authority/recovery evidence across normal and degraded operation.

## Phase P3 — Media subsystem

P3.1 Inventory media domain contracts and lifecycle states.
P3.2 Implement/qualify ingestion and metadata/index contracts.
P3.3 Implement/qualify playback/control contracts.
P3.4 Validate authorization, storage, retention and recovery semantics.
P3.5 Add integration and failure-injection tests.
P3.6 Benchmark bounded media operations and resource limits.
Exit: media subsystem has reproducible functional and recovery evidence.

## Phase P4 — Documents and intelligence

P4.1 Complete document ingestion/index/search contracts.
P4.2 Complete Trusted Sources Intelligence Engine boundaries: discovery, retrieval, verification, provenance, evidence and knowledge.
P4.3 Add source trust/verification and stale-data handling.
P4.4 Ensure external retrieval cannot mutate State Authority directly.
P4.5 Add audit/revocation and offline/degraded behavior.
Exit: document/intelligence workflows are provenance-bound and fail-closed.

## Phase P5 — Mobile Access Layer

P5.1 Preserve two-app model: MediaHub Core + separate Remote Mobile Application.
P5.2 Implement authenticated session and authorization contracts.
P5.3 Implement API/client compatibility and offline/degraded states.
P5.4 Add remote-control and state synchronization tests.
P5.5 Validate that Mobile Access Layer is not an AI compute tier.
P5.6 Add iOS integration, lifecycle, accessibility and security qualification.
Exit: mobile access is operationally bounded and consistent with platform authority.

## Phase P6 — Voice and smart-home integration

P6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.
P6.2 Implement each provider through bounded adapters.
P6.3 Enforce consent, authorization, command provenance and replay protection.
P6.4 Route Smart Home mutations through Home Assistant Core.
P6.5 Add provider outage/fallback tests without changing authority semantics.
Exit: voice/smart-home paths are qualified without authority bypass.

## Phase P7 — AI Human Clone and corporate cloud-development subsystems

P7.1 Define Human Clone contract as separate Cloud Development AI subsystem.
P7.2 Enforce consent, scope, provenance, audit and revocation.
P7.3 Implement Trusted Sources/knowledge workflows required by the subsystem.
P7.4 Ensure ordinary users have no direct corporate Cloud Development AI access.
P7.5 Add data minimization, residency/policy and egress tests.
P7.6 Add degraded/offline behavior and recovery evidence.
Exit: cloud AI subsystems are isolated, auditable and authorization-bound.

## Phase P8 — Cross-system integration

P8.1 Validate escalation path: Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI.
P8.2 Validate all contracts across Core, AI, HA, Media, Documents, Mobile and Voice.
P8.3 Run end-to-end scenarios for normal, degraded, recovery and revoked authorization states.
P8.4 Verify no hidden persistence/network egress/subprocess or State Authority mutation in bounded agents.
P8.5 Verify provenance chain from request to artifact/result/evidence.
Exit: integrated system behavior is deterministic across supported scenarios.

## Phase P9 — Security qualification

P9.1 Full threat-model refresh against current architecture.
P9.2 Static secret scanning and dependency/license/provenance review.
P9.3 Egress and endpoint allowlist audit.
P9.4 Sandbox escape/authority escalation negative tests.
P9.5 Credential broker isolation and revocation tests.
P9.6 Fuzz/malformed-input tests for public contracts where justified.
P9.7 Recovery and tamper-evidence tests.
Exit: security blockers are closed or explicitly documented as release blockers.

## Phase P10 — Performance, reliability and soak

P10.1 Establish baseline latency/resource metrics for Core, AI, Media, Mobile and HA.
P10.2 Optimize only where measurements identify a real bottleneck.
P10.3 Long-running supervisor/daemon soak with checkpoint/restart cycles.
P10.4 Cluster failover and recovery soak.
P10.5 Media/document workload soak within resource limits.
P10.6 Local model lane benchmark; do not weaken safety timeouts.
P10.7 Cloud-agent lane benchmark only when legitimately authenticated.
Exit: reliability evidence exists for sustained operation and controlled degradation.

## Phase P11 — Release Candidate hardening

P11.1 Freeze functional baseline for RC.
P11.2 Reconcile all open tasks, worktrees, branches and generated artifacts.
P11.3 Full test matrix: unit, integration, system, recovery, security, performance.
P11.4 Reproducibility/build/package verification.
P11.5 SBOM/license/provenance inventory.
P11.6 Documentation/operator/recovery runbooks.
P11.7 Independent review package assembled from immutable evidence.
Exit: Release Candidate is reviewable; still no production authorization.

## Phase P12 — Independent review and release authorization

P12.1 External/independent reviewer evaluates architecture, security, recovery, AI governance and release evidence.
P12.2 Resolve every blocker through a new bounded queue item.
P12.3 Re-run affected verification after each remediation.
P12.4 Establish exact release commit and evidence set.
P12.5 Human release authorization only.
Exit: release authorization is explicitly granted by the authorized human; agents do not grant it.

## Phase P13 — Production readiness and controlled production authorization

P13.1 Production environment parity and configuration audit.
P13.2 Backup/restore and rollback rehearsal.
P13.3 Monitoring/alerting/runbook qualification.
P13.4 Security and credential rotation/revocation rehearsal.
P13.5 HA failover and disaster-recovery rehearsal.
P13.6 Human production authorization only.
Exit: production authorization is a human-controlled state transition with evidence.

## Phase P14 — Post-release continuous engineering

P14.1 Monitor incidents, regressions, dependency/security advisories and performance.
P14.2 Every issue becomes a bounded queue item with owner, evidence and acceptance criteria.
P14.3 Maintain compatibility/migration contracts.
P14.4 Periodically re-run security, recovery and provenance audits.
P14.5 Keep ECC/cloud-agent integrations replaceable and policy-bounded.
P14.6 Never allow post-release automation to self-authorize a production change.

## Completion definition

The autonomous program remains active until all applicable P0–P13 exit criteria are evidenced. “Product complete” means: functional baseline implemented, integrated, tested, security-qualified, recovery-qualified, performance/soak-qualified, reproducibly packaged, independently reviewed, and explicitly authorized for release by the human authority. If production authorization is not granted, the system may reach a fully qualified Release Candidate but must remain release-blocked.

## Agent routing matrix

| Lane | Primary work | Secondary work | Blocks |
|---|---|---|---|
| Architecture/Contract | P0–P2, P8 | all contract regressions | downstream contract consumers |
| Core/State Authority | P2 | P8–P10 | platform mutation/recovery |
| AI/ECC | P1, P7 | P8 | AI/cloud integration |
| Hybrid/Cloud | P0, P1, P8 | P10 | cloud-agent activation |
| Mobile | P5 | P8, P10 | mobile RC |
| Smart Home/HA | P2, P6 | P8 | HA/voice RC |
| Media | P3 | P8, P10 | media RC |
| Documents/Intelligence | P4, P7 | P8 | intelligence RC |
| Voice | P6 | P8 | voice RC |
| Security/Red Team | all phases | P9 | security qualification |
| QA/Verification | all phases | P11–P12 | evidence/RC |
| Performance/Reliability | P0, P10 | P11 | soak/RC |
| Release/Independent Evidence | P11–P13 | P14 | release authorization |
| Operations/Recovery | P0, P2, P10, P13 | P14 | production readiness |

## Autonomous controller loop

Every cycle: `observe → reconcile → select → isolate → execute → verify → record → commit → replan`.

If a cloud agent is unavailable: continue local contract/test/security/recovery work and record BLOCKED for cloud-specific work. If local AI times out: continue deterministic bounded engineering where acceptance criteria are already explicit; do not invent architectural intent. If CI/review evidence is unavailable: continue local verification but do not claim remote PASS. If a gate is ambiguous: stop the affected lane and create a clarification/remediation task. If all current implementation tasks are blocked: run evidence/coverage/reproducibility/security work rather than idle.

## Terminal gate order

FUNCTIONAL BASELINE → CONTRACTS → INTEGRATION → RECOVERY → SECURITY → PERFORMANCE/SOAK → RELEASE CANDIDATE → INDEPENDENT REVIEW → RELEASE AUTHORIZATION (HUMAN) → PRODUCTION READINESS → PRODUCTION AUTHORIZATION (HUMAN).
