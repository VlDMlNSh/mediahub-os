# MH-7 — Autonomous Qualification Blueprint

Status: QUEUED / NOT QUALIFIED
Date: 2026-09-30
Target: engineering/mh07-configuration-policy-20260930
Baseline: engineering/mh21-sandbox-lifecycle-20260910 @ ea7177ed099d3f0f436993571aac88b36f0a4cbc
Current target HEAD at queue creation: 1996a0dc3b3abee187f8d4dd5440987373809a78
R4: 471f709f5633feab7aeb62dd3ea52effad6d2bc4

## Objective

Bring MH-7 to independently evidenced architectural qualification. This blueprint is a queue/control artifact; it grants no merge, release, production, State Authority, credential, network, or external-agent authority.

## Hippodrome plan / waves

### Wave 0 — Reconciliation and hygiene
- Reconcile MH-7 branch, PR #118, baseline and R4 ancestry.
- Verify obsolete MH-7 PR #81 remains closed and unmerged.
- Detect duplicate/open MH-7 requests before creating new work.
- Preserve one canonical active MH-7 PR and one qualification queue.
- No history rewrite, force-push, or deletion of historical evidence.

Exit: one canonical active MH-7 path, no erroneous open request.

### Wave 1 — Contract completeness
Qualify:
- ConfigurationVersion schema and invariants.
- PolicyVersion schema and invariants.
- Scope/precedence model.
- Authorization vs policy separation.
- Configuration != Policy != Canonical State != Runtime State.
- deterministic conflict resolution.
- security/safety precedence and fail-closed behavior.

Required evidence: focused positive/negative tests plus independent review of semantics.

### Wave 2 — Lifecycle and qualification
Qualify:
- Request → Identity → Authorization → Scope → Schema → Policy → Conflict → Qualification → Commit → Version → Audit → Distribution → Activation → Verification.
- candidate/pending/current/degraded/stale/incompatible/quarantined states.
- last-known-good and integrity requirements.
- stale version rejection.
- compatibility and dependency checks.
- explicit rollback semantics.

No hidden retry, LWW, rebase, merge, or permissive fallback.

### Wave 3 — Distribution / Local First / offline
Qualify:
- logical central authority with distributed execution.
- local qualified replica/cache is non-authoritative.
- TTL/expiry behavior.
- expired critical policy becomes safe degraded/fail-closed.
- node trust/capability/platform/security/cluster applicability checks.
- distribution failure does not create a permissive state.

### Wave 4 — Audit / provenance / secrets
Qualify:
- actor, identity, source, previous/new version, reason, authorization, policy decision, target, result, timestamp, provenance.
- immutable provenance chain for material changes.
- secret separation.
- no credentials in ordinary configuration/policy/audit payloads.
- no hidden external transfer.

### Wave 5 — Export/import / portability / policy-as-code
Qualify:
- classification and secret separation on export/import.
- schema/capability/security/compatibility validation.
- rollback on failed import.
- portability only after qualification.
- declarative representation is provenance/input, not runtime authority.
- policy-as-code remains versioned, tested, simulated and controlled.

### Wave 6 — Cross-domain authority
Qualify:
- State Authority remains sole canonical platform mutation authority.
- Home Assistant Core remains Smart Home operational authority.
- AI/ECC/cloud/plugins remain advisory/non-authoritative.
- Mobile remains access layer, not AI compute tier.
- no configuration/policy path bypasses Consumer Boundary or State Authority.

### Wave 7 — Security / negative / recovery
Execute deterministic negative tests for:
- malformed/unsupported schemas;
- critical conflicts;
- stale versions;
- unauthorized changes;
- capability mismatch;
- expired policy;
- unavailable authority;
- degraded/offline operation;
- rollback integrity failure;
- secret leakage;
- attempted authority escalation;
- hidden network/subprocess/persistence paths.

### Wave 8 — Independent verification
Run, where repository support exists:
- focused tests;
- full regression;
- lint/type checks;
- security/static checks;
- diff/provenance checks;
- recovery tests.

Each result must be classified PASS / FAIL / BLOCKED / INCONCLUSIVE with fresh evidence. No self-qualification.

### Wave 9 — Final reconciliation
- Reconcile all MH-7 artifacts against MH-1…MH-6 invariants.
- Reconcile PR #118 with actual HEAD and evidence.
- Confirm no duplicate active MH-7 request.
- Confirm R4 ancestry.
- Confirm no production/release authorization was exercised.
- Produce qualification record.

## Qualification gate

MH-7 may be marked QUALIFIED only when:
1. all mandatory contract surfaces are implemented or explicitly and legitimately deferred;
2. all mandatory negative/security/recovery tests have fresh evidence;
3. no material unresolved contradiction remains;
4. cross-domain authority boundaries are evidenced;
5. provenance and audit requirements are evidenced;
6. independent review exists;
7. GitHub state contains one canonical active review path;
8. no credential, production, release, or State Authority authority was granted by the qualification process.

Until all gates pass: status remains NOT QUALIFIED.

## Stop conditions

Stop and record BLOCKED/INCONCLUSIVE on:
- architectural ambiguity;
- contradictory source of truth;
- missing authorization boundary;
- unverifiable claim;
- absent required credential or external dependency;
- inability to reproduce a required check;
- attempted history rewrite or unauthorized mutation;
- any path that could bypass State Authority, Home Assistant authority, policy, authorization, or Consumer Boundary.

## Canonical GitHub hygiene

- PR #81 is historical/obsolete and remains closed/unmerged.
- PR #118 is the sole active MH-7 review path.
- Do not open another MH-7 PR unless #118 is explicitly superseded by a documented governance decision.
- Historical commits are evidence and are not erased merely because they were superseded.
