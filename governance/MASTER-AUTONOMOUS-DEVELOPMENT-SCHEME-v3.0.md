# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER AUTONOMOUS DEVELOPMENT SCHEME v3.0

Date: 2026-09-07
Repository: VlDMlNSh/mediahub-os
Frozen forensic baseline: 25f7e3e50708d4bcad37fa712a5000dd2a7dea06
R4 executable checkpoint: 471f709f5633feab7aeb62dd3ea52effad6d2bc4

## 1. Mission

Develop and qualify MediaHub with maximum safe parallelism, zero architectural drift, exact-SHA evidence, fail-closed governance and explicit separation of implementation, verification, independent review, release and production authority.

GitHub is the repository/audit control plane. Actual executable results outrank model claims, prompt metadata and historical assumptions.

## 2. Non-negotiable authority chain

INPUT -> CONSUMER BOUNDARY -> AUTHORIZATION/POLICY -> COMMAND -> STATE AUTHORITY -> CANONICAL STATE -> EVENT -> OBSERVATION -> EVIDENCE

Exactly one canonical State Authority exists. UI, AI, plugins, devices, cloud, automation, telemetry, health/readiness, caches and recovery helpers cannot directly mutate canonical state.

Fail closed. Readiness, health, liveness, presence and network reachability are never authorization.

## 3. Agent and component allocation

A0 ORCHESTRATOR: current HEAD, dependency graph, work allocation, conflict control, evidence index.
A1 ARCHITECT: frozen MH-04 semantics, protected invariants, scope and architectural drift.
A2 EVIDENCE/PROVENANCE: source, correlation, causation, Event projection and Evidence binding.
A3 IMMUTABILITY: deep payload/metadata immutability and serialization isolation.
A4 SCHEMA: Event/Evidence schema and validation contracts.
A5 RESTORE: checkpoint integrity, authorization, reachability and fail-closed restore behavior.
A6 COMPOSITION: construction graph and exactly-one StateAuthority proof.
A7 RED TEAM: system-wide negative inventory and bypass challenges.
A8 TEST: deterministic unit/integration/security/qualification matrix.
A9 CI-EVIDENCE: exact checkout SHA, workflow/run identity and reproducibility.
A10 FORENSICS: exact tree, refs, files, history and stale-SHA detection.
A11 RECONCILIATION: current-vs-historical evidence packet and ledger consistency.
A12 INDEPENDENT REVIEW: adversarial review performed by an identity/operator independent of implementation; never satisfied by model consensus.
A13 RELEASE GATE: qualification decision only; no implementation authority.

## 4. Local services and their fixed responsibilities

MH-DEV-01 / Desktop Commander: controlled local filesystem, terminal, tests and toolchain execution. Never treat local execution as independent qualification.
Codex local app-server: primary engineering agent/runtime for implementation, analysis and orchestration; no qualification, merge or production authority.
ALAMO local adapter: engineering/orchestration and parallel task execution only; supporting evidence only.
GitHub Actions/self-hosted runner: reproducible CI execution and exact-SHA evidence emission.
GitHub connector: repository, PR, issue, branch, commit, workflow and evidence control plane.
ArmorCodex: policy guardrail and intent-plan layer; fail-closed restrictions on production, merge, release and qualification authority.

## 5. Model routing

High-reasoning lane: architecture, orchestration, difficult root-cause analysis and adversarial review preparation.
Fast lane: inventory, search, repetitive contract comparison, documentation reconciliation and test-matrix assistance.
Independent-model lane: red-team challenge generation, bypass enumeration, restore reachability and contradiction hunting.

DeepSeek: adversarial challenge generator only. Its output is never independent qualification.
Other configured local/free/public models: advisory analysis only unless an actual controlled execution result exists.

If an external model adapter is not configured, emit NO_ADAPTER/NOT_EXECUTED. Never simulate a model call.

## 6. Plugin allocation

GitHub: canonical code/PR/CI/audit integration; installed and primary.
Codex Security: security scanning/investigation lane; findings are evidence, not approval.
ArmorCodex: governance policy and pre-tool intent control.
CodeWords: optional workflow automation/build/deploy lane; never receives qualification authority.
Atlassian Rovo: optional Jira/Confluence planning and documentation lane; never repository authority.
Make: optional cloud automation/AI-agent orchestration lane; use only for non-authoritative task automation.
Git Diff Patcher Bridge: optional patch diagnosis/proposal lane; changes remain under controlled repository review.
Tavily AI: optional fresh external research lane; no authority over code or qualification.
Codex Replay: optional replay/adversarial reproduction lane.
Plugin Management: installation, connection and permission control only.

Suggested plugins are not equivalent to installed/connected components. Never claim execution through a plugin without an actual result.

## 7. Parallel execution protocol

Read-only passes run in parallel. Writes to the same file, branch or authority surface are serialized.

Dependency graph:
HEAD -> FORENSICS + ARCHITECT + INVENTORY
ARCHITECT + EVIDENCE + IMMUTABILITY + SCHEMA + RESTORE + COMPOSITION -> TEST
RED TEAM + SECURITY -> INDEPENDENT REVIEW
All verified evidence -> RECONCILIATION -> RELEASE GATE

Every task contract contains exact SHA/ref, scope, objective, expected output schema and forbidden actions.

## 8. Exact-SHA discipline

Every meaningful claim records exact commit SHA, tree where relevant, branch/ref, command, environment, result and evidence reference.

Historical evidence never transfers automatically to a later SHA.
A documentation commit after executable testing creates a new control point and requires fresh execution if that new SHA is to qualify.
Default-branch search is never proof of absence at an exact SHA.
No force-push, amend, reset or history rewrite on frozen targets.

## 9. Security and secret rules

Secrets exist only in approved secret/environment stores. Never put provider keys in prompts, source, issues, artifacts, logs, commits or chat.

Security tooling may report findings and propose fixes. It cannot approve qualification.

Production commands, production credentials and release operations are blocked until explicit governance gates are satisfied.

## 10. Change protocol

FINDING -> CLASSIFICATION -> REMEDIATION DECISION -> MINIMAL PATCH -> TEST -> EXACT-SHA CI -> EVIDENCE -> INDEPENDENT REVIEW -> QUALIFICATION DECISION

No speculative refactoring. No scope expansion to eliminate an evidence blocker. If the blocker is evidence, improve evidence rather than inventing implementation.

## 11. Qualification state machine

IMPLEMENTED -> IMPLEMENTED_NOT_EXECUTED -> EXECUTED -> INDEPENDENTLY_REVIEWED -> QUALIFIED -> PRODUCTION_AUTHORIZED

A model response, test file, CI configuration, agent agreement or self-review cannot skip a state.

UNKNOWN, NOT EXECUTED, INDEPENDENCE NOT ESTABLISHED and INCONCLUSIVE remain explicit blockers.

## 12. MH-05 current lock

MH-05 qualification remains QUALIFICATION_OPEN / NOT QUALIFIED until all mandatory gates are independently evidenced.
Production remains NOT AUTHORIZED.
Persistence remains NOT AUTHORIZED.
HA remains NOT AUTHORIZED.
MH-06 remains LOCKED.

R4 exact-SHA executable evidence is supporting execution evidence, not independent approval.

## 13. Mandatory qualification gates

- canonical State Authority and governed Consumer Boundary;
- source/correlation/causation provenance;
- canonical Event projection and schema;
- deep immutability;
- Evidence bound to real AuthorizationContext and exact Event identity;
- governed restore and fail-closed behavior;
- composition-root exactly-one-authority proof;
- system-wide negative verification;
- exact-SHA runtime and security execution;
- independent security review;
- independent system-wide negative verification;
- final evidence reconciliation;
- Release Gate decision.

Only after all gates are explicitly PASS may qualification be considered. Production authorization is a separate decision.

## 14. Operating rule for every continuation prompt

Start from the actual current HEAD. Preserve all accepted history. Inspect before changing. Parallelize independent analysis. Serialize shared writes. Test every patch. Re-run exact-SHA evidence after any qualification-target change. Never transfer reviews across SHAs. Never claim independent review when reviewer/operator is the implementation author.

## 15. Continuation command

CONTINUE AUTONOMOUSLY FROM ACTUAL CURRENT HEAD. EXECUTE ALL SAFE PARALLEL PASSES. MAXIMIZE ENGINEERING THROUGHPUT WITHOUT ARCHITECTURAL DRIFT. KEEP QUALIFICATION FAIL-CLOSED. REPORT ONLY OBSERVED RESULTS. DO NOT MERGE, RELEASE, AUTHORIZE PRODUCTION OR UNLOCK MH-06 WITHOUT THE EXPLICIT GOVERNANCE GATE.
