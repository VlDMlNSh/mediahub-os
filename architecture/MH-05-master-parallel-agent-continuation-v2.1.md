# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER PARALLEL AGENT CONTINUATION PROMPT v2.2

**FULL HISTORY PRESERVATION / ZERO ARCHITECTURAL DRIFT / PARALLEL QUALIFICATION SWARM / GITHUB MODEL ORCHESTRATION**

Date: 2026-09-07
Repository: `VlDMlNSh/mediahub-os`
Current remediation branch: `remediation/mh05-r3-event-evidence`
Current control-point rule: actual branch HEAD is authoritative; this document must never be treated as a frozen SHA source.
Immutable forensic target: `25f7e3e50708d4bcad37fa712a5000dd2a7dea06`
Base: `recovery/full-functional-spec`
Base SHA: `0adb60e35d8822c927b6dd5a5a34643115c4d068`
Historical PR merge: `27ce528f1ce25b5676b676f2dd7bccd28eb4055c`

## 0. PRIMARY COMMAND

CONTINUE FROM ACTUAL CURRENT REMEDIATION HEAD.

Do not return to PASS 0. Do not repeat forensic recovery. Do not change the immutable forensic target. Do not force-push. Do not rewrite history. Do not expand scope beyond MH-05. Maximize safe parallelism without architectural drift.

At the start of every major cycle query the actual branch HEAD. Never assume prompt metadata or an older ledger SHA is current.

Every claim must be classified as one of: `IMPLEMENTED`, `STATIC_SUPPORT`, `IMPLEMENTED_NOT_EXECUTED`, `EXECUTED`, `INDEPENDENTLY_REVIEWED`, `QUALIFIED`, `PRODUCTION_AUTHORIZED`.

## 1. AUTHORITY MODEL

The immutable forensic target is never modified. All remediation occurs on `remediation/mh05-r3-event-evidence`.

Git SHA, exact-SHA executable evidence, test results, and explicit qualification gates are authoritative. Model output and model consensus are supporting analysis only.

## 2. ARCHITECTURAL INVARIANTS

Canonical path:

INPUT → CONSUMER BOUNDARY → AUTHORIZATION/POLICY → COMMAND → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE

Protected invariants:

1. exactly one canonical State Authority;
2. ConsumerBoundary is not canonical state owner;
3. ConsumerBoundary is not persistence authority;
4. ConsumerBoundary is not event authority;
5. ConsumerBoundary is not authorization authority;
6. source identity is explicit;
7. correlation identity is explicit;
8. authorization is explicit;
9. fail closed;
10. malformed input cannot mutate state;
11. readiness/health/liveness/presence/network reachability are not authorization;
12. event-triggered mutation must re-enter the governed command path;
13. UI/AI/plugin/device/cloud/automation/recovery cannot directly mutate canonical state.

## 3. SCOPE LOCK

Until MH-05 is independently qualified, forbidden: MH-06; durable persistence; HA/cluster; production release; production authorization; recovery redesign; changing frozen MH-04 Event semantics; changing canonical authority; unrelated capability implementation.

Allowed: MH-05 remediation, tests, evidence, security verification, exact-SHA reconciliation, minimal scope-local fixes, qualification documentation.

## 4. CURRENT QUALIFICATION STATE

MH-05 = NOT QUALIFIED.
Qualification = BLOCKED / OPEN.
Production = NOT AUTHORIZED.
MH-06 = LOCKED.

Do not change these states without every mandatory gate.

## 5. PARALLEL AGENT ORGANIZATION

Operate logically as these specialists:

- AGENT 0 ORCHESTRATOR — HEAD, dependencies, conflicts, scope, status.
- AGENT 1 ARCHITECT — frozen MH-04 semantics, authority model, drift prevention.
- AGENT 2 R3-EVIDENCE — Runtime Event, canonical projection, provenance, causation, Event→Evidence.
- AGENT 3 IMMUTABILITY — recursive immutability, nested payload/metadata, serialization isolation.
- AGENT 4 SCHEMA — exact Event/Evidence schemas and validation.
- AGENT 5 R4-RESTORE — checkpoint/restore callers, reachability and security; no redesign before reachability proof.
- AGENT 6 COMPOSITION — exact production composition root and construction graph.
- AGENT 7 BYPASS RED TEAM — system-wide negative inventory across UI, AI, plugin, device, cloud, automation, event reaction, telemetry, health, readiness, liveness, cache, persistence, recovery.
- AGENT 8 TEST — MH-05 qualification matrix.
- AGENT 9 CI-EVIDENCE — exact workflow, checkout SHA, event SHA, branch, runtime and conclusion.
- AGENT 10 FORENSICS — exact-SHA tree, files, metadata and history.
- AGENT 11 EVIDENCE RECONCILIATION — current evidence packet; historical evidence retained.
- AGENT 12 INDEPENDENT REVIEW — adversarial review independent of implementation/test/orchestrator conclusions.
- AGENT 13 RELEASE GATE — qualification decision only; no implementation authority.

## 6. GITHUB-CONTROLLED MODEL ORCHESTRATION

GitHub is the repository and audit control plane. Where an external model execution layer is actually configured, specialist jobs may be dispatched through GitHub-controlled automation using repository workflow inputs and secret-backed environment variables.

Model routing:

- high-reasoning model: ARCHITECT, ORCHESTRATOR, INDEPENDENT REVIEW, RELEASE GATE;
- fast models: inventory, static search, repetitive contract comparison, test-matrix assistance, documentation reconciliation;
- multiple independent models: red-team, bypass, restore reachability, adversarial review.

Each model task must receive a bounded task contract, exact commit/ref, scope lock, expected output schema, and no authority to merge/qualify by itself.

Model output must be stored only as auditable, non-secret evidence when appropriate. A model may propose a finding or patch; repository review, tests, exact-SHA execution and qualification governance remain authoritative.

If the external execution layer is unavailable, explicitly report:

`EXTERNAL MODEL EXECUTION NOT AVAILABLE IN CURRENT RUNTIME`

Do not claim background agents or external-model execution unless an actual execution result exists.

## 7. SECRET SAFETY

API keys for Google, Groq, OpenAI, or other providers are secrets. Supply them only through the configured secret/environment layer. Never paste keys into prompts, commits, issues, evidence, logs, generated artifacts, source code, or chat. Never expose them in workflow output.

Repository connectivity does not by itself prove that a provider API key is available to a model runner.

## 8. SAFE PARALLEL EXECUTION

Independent passes may run concurrently. Writes to the same file or architectural surface are serialized. No parallel agent may redesign the same authority surface independently.

Dependency graph:

HEAD
├── R3
├── IMMUTABILITY
├── SCHEMA
├── R4
├── COMPOSITION
├── BYPASS
└── FORENSICS

R3 + IMMUTABILITY + SCHEMA → TEST
R4 + COMPOSITION + BYPASS → SECURITY REVIEW
All → EVIDENCE RECONCILIATION → RELEASE GATE

## 9. CODE CHANGE RULE

Every code change must be minimal, scope-local, regression-tested, architecturally compatible, traceable to a finding, and associated with a commit SHA.

Required chain:

FINDING → CLASSIFICATION → REMEDIATION DECISION → IMPLEMENTATION → TEST → EXACT-SHA EXECUTION → EVIDENCE → REVIEW

No speculative refactoring.

## 10. EVENT RULE

Frozen MH-04 semantics remain:

Command → Validation → Authorization/Policy → Consumer Contract → State Authority → Canonical Mutation → Event → Observers

Event is observational, not mutation authority. Event-triggered mutation re-enters the governed command path.

## 11. EVIDENCE RULE

Evidence must preserve actual command_id, correlation_id, source_identity, authorization_context, target, operation, pre_state, post_state, authorization_result, validation_result, mutation_result, emitted_events, artifact_hash, reproducibility_reference, reviewer, review_basis, unknowns, contradictions and blockers.

Never synthesize authorization context or placeholders such as `observed-at-execution`.

## 12. FINGERPRINT RULE

Event fingerprint is an integrity/evidence mechanism only. It is not authentication, authorization, permission or mutation authority.

## 13. REQUIRED TEST MATRIX

Causation: first event with null causation succeeds; referenced causation succeeds; unknown causation rejected; rejection does not mutate state; rejection emits no event.

Provenance: ConsumerBoundary source→Command; Command source→Runtime Event; Runtime Event source→Canonical Event; projection cannot override source, causation or timestamp.

Immutability: top-level, nested payload, nested metadata and serialized-representation mutation attempts fail without changing the Event.

Schema: missing required field, extra field, invalid severity, invalid priority and invalid timestamp are rejected.

Evidence: real authorization context, source, correlation, causation, exact Event ID and fingerprint are preserved; Evidence remains observational and cannot become mutation authority.

Restore: dedicated authorization, checkpoint integrity, malformed/forged input rejection, unavailable fail-closed behavior, governed ConsumerBoundary reachability, coherent checkpoint-prefix history, and no normal mutation authorization bypass after restore.

Composition: exactly one canonical StateAuthority constructed by composition root; ConsumerBoundary is bound to that authority; no secondary canonical storage.

System-wide negative audit: exact-SHA AST/static checks for constructor duplication, canonical storage duplication, restore reachability, direct boundary mutation, and aliases/import paths where repository structure permits.

## 14. CI-EVIDENCE RULE

For every meaningful remediation commit record workflow run, workflow SHA, checked-out SHA, event SHA, branch, Python version, test command and conclusion.

`workflow_runs=[]` = EXECUTION EVIDENCE ABSENT, never PASS.
`in_progress` = EXECUTION IN PROGRESS.
`success` = EXECUTED.
`failure` = EXECUTED / FAILED.

The available GitHub workflow query may expose only pull-request-triggered runs. Absence from that view must not be interpreted as proof that push-triggered execution never occurred; use observable workflow/run records only.

## 15. EXACT-SHA FORENSICS

Use exact branch/ref/commit/tree/files/metadata. Do not use default-branch Code Search as proof of absence at an exact SHA. Do not repeat closed findings unless new evidence changes classification.

## 16. EVIDENCE RECONCILIATION

Current evidence identity must contain immutable target, remediation branch and actual remediation HEAD. Historical evidence remains HISTORICAL / SUPPORTING. Current evidence must be CURRENT / EXACT-SHA.

If a documentation commit changes the control-point SHA after executable code was last run, classify the executable ancestor separately and do not falsely claim current-HEAD execution. Prefer a fresh CI run on the final control-point tree before Release Gate.

Never delete historical evidence merely to clean the repository.

## 17. INDEPENDENT REVIEW

The reviewer must not simply trust implementation agents, tests, workflows or orchestrator conclusions. Review for false provenance, synthetic authorization, authority duplication, bypasses, evidence fabrication, stale SHAs, implementation-only tests and unsupported system claims.

## 18. FINAL MH-05 GATES

MH-05 can become QUALIFIED only when all are demonstrated:

[ ] canonical authority
[ ] boundary governance
[ ] source provenance
[ ] correlation provenance
[ ] causation provenance
[ ] canonical Event projection
[ ] canonical schema
[ ] deep immutability
[ ] Event → Evidence linkage
[ ] real authorization context
[ ] evidence reproducibility
[ ] restore security/reachability
[ ] composition root
[ ] system-wide negative verification
[ ] UI negative verification
[ ] AI negative verification
[ ] plugin negative verification
[ ] device negative verification
[ ] cloud negative verification
[ ] automation/event-reaction negative verification
[ ] health/readiness negative verification
[ ] persistence/cache negative verification
[ ] recovery negative verification
[ ] exact-SHA execution evidence
[ ] independent security review
[ ] evidence revision reconciliation

Any unchecked mandatory item means MH-05 NOT QUALIFIED, Production NOT AUTHORIZED, MH-06 LOCKED.

## 19. CURRENT PRIORITY

P0: actual HEAD reconciliation; workflow reconciliation; R3 validation; R4 reachability; F-02 composition; F-03 system-wide negative inventory; F-04 evidence packet.

P1: independent security review; independent bypass verification; final qualification reconciliation.

P2: documentation cleanup and release decision preparation.

No unrelated work.

## 20. GITHUB AUDIT TRAIL

For every meaningful action record branch, parent SHA, resulting SHA, changed files, reason, tests, workflow result and evidence classification. Never claim an unobserved SHA or workflow result.

## 21. RESPONSE CONTRACT

Every major cycle reports: (1) Выполнено; (2) parallel agent results; (3) new findings; (4) changed SHAs; (5) execution evidence; (6) qualification matrix; (7) remaining blockers; (8) next parallel passes; (9) remaining effort.

## 22. NO BACKGROUND CLAIMS

Never claim hidden agents are running, background work continues, external models are active, CI passed without a run, or independent review occurred without an independent reviewer.

## 23. FINAL PRINCIPLE

MAXIMUM VELOCITY without sacrificing ARCHITECTURAL INTEGRITY, SECURITY, TRACEABILITY, REPRODUCIBILITY, EXACT-SHA EVIDENCE or QUALIFICATION DISCIPLINE.

Fastest correct path:

PARALLEL ANALYSIS → MINIMAL REMEDIATION → PARALLEL TESTING → EXACT-SHA EXECUTION → INDEPENDENT REVIEW → EVIDENCE RECONCILIATION → QUALIFICATION GATE

PRIMARY COMMAND: CONTINUE FROM ACTUAL CURRENT REMEDIATION HEAD. EXECUTE MAXIMUM SAFE PASSES. PRESERVE ALL HISTORY. ZERO ARCHITECTURAL DRIFT. MH-05 FIRST. MH-06 REMAINS LOCKED UNTIL MH-05 IS QUALIFIED.
