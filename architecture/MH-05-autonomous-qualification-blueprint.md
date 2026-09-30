# MH-05 — Autonomous Qualification Blueprint

Status: READY_FOR_AUTONOMOUS_QUALIFICATION
Target: exact commit fe06f7f0ad25d4be5a12afd8b140f97083c0f5ca on engineering/mh21-sandbox-lifecycle-20260910

## Execution rule
Use fresh evidence tied to the exact target revision. Do not transfer historical evidence. Do not self-certify. Do not mutate production or immutable historical objects.

## Waves
W0 Identity and provenance: verify repository, branch, exact commit, canonical artifact and absence of duplicate MH-05 qualification runs.

W1 Contract and authority reconciliation: reconcile MH-05 against MH-01..MH-04 authoritative contracts; confirm one logical State Authority and Home Assistant Core as Smart Home operational authority; confirm AI, cloud, UI, mobile and external ecosystems remain non-authoritative.

W2 Integration boundary: verify Discovery -> Identity -> Capability -> Trust -> Qualification -> Contract/Adapter -> Policy -> Admission; compatibility never implies authorization; adapters/plugins are capability-scoped, sandboxed, auditable and revocable.

W3 Data and cloud boundary: verify Local First, data classification, egress sequence, absent-permission => DENY, and Developer Cloud -> User Data denial.

W4 Event and state boundary: verify event authentication/validation, event != mutation permission, canonical state separation, and fail-closed handling of ambiguous critical state.

W5 Lifecycle, recovery and revocation: verify lifecycle states, revocation, recovery revalidation and policy-controlled reintegration; recovery must not restore trust automatically.

W6 Negative / forbidden-path verification: verify denial of every listed bypass class and record PASS/FAIL/INCONCLUSIVE with exact evidence.

W7 OSS/provenance and qualification: verify provenance, license/security qualification and lifecycle controls for external components; unqualified integrations remain inadmissible.

W8 Independent review and disposition: independent reviewer reconciles evidence and contradictions. Transition only: RECONCILED -> VERIFIED -> QUALIFIED. Qualification does not imply release or production authorization.

## Hard gates
Any material failure, stale evidence, identity mismatch, duplicate run, unresolved contradiction or missing negative-path evidence blocks QUALIFIED.

## Required output
One exact-SHA qualification record containing target SHA, reviewer/execution identity, environment, wave-by-wave status, exact evidence references, residual gaps/blockers and final disposition.
