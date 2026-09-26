# MH-04 — Candidate API → v1.0 Verification Map

**Status:** PROPOSED / NOT VERIFIED  
**Control point:** MH-04 / CTR-001  
**Scope:** reconciliation of historical P0-04 `InMemoryStateAuthority` against current V-01…V-15 verification surfaces.  
**Authorization:** no production implementation or promotion authorization is granted by this artifact.

## Evidence baseline

Historical candidate implementation branch: `implementation/p0-04-in-memory-state-authority`  
Historical implementation commit: `456deb9aadd3cae7d8978a7d89f540e1a029b7f4`  
Historical implementation blob for `runtime/mediahub_runtime/in_memory_state.py`: `9432a5a790ab24ae0bbc7dce2663f3e8b34743fc`.

Historical execution evidence reported 123/123 full regression and 13/13 targeted P0-04 regression on `mh-dev-01`, Python 3.12.3, Linux 6.8.0-138-generic, x86_64. This map does not promote that historical evidence to current verification or acceptance.

## API surface identified

Candidate exposes:

- `begin(context, payload=None)`
- `commit(transaction)`
- `abort(transaction)`
- `read(key=None)`
- `snapshot(context)`
- `restore(snapshot_reference, context)`
- transaction identity/status and candidate isolation
- generation and state-version checks
- structural validation
- integrity validator hook
- authorization policy hook
- in-memory checkpoint authority-token binding

## Verification mapping

| Case | Candidate surface | Current assessment | Required next action |
|---|---|---|---|
| V-01 | `_authorize`, `begin`, `commit`, `abort`, `snapshot`, `restore` | REQUIRES CURRENT EXECUTION | Run positive/negative authorization cases with exact identity/context evidence |
| V-02 | no external mutation API in candidate; package exports authority API | NOT VERIFIED | Build boundary fixture proving UI/AI/cloud/plugin/device/automation/telemetry/health/cache/recovery cannot mutate authority directly |
| V-03 | `begin` → `Transaction.set_payload` → `commit`; structural/integrity validation | REQUIRES CURRENT EXECUTION | Execute legal and illegal transitions and capture pre/post state |
| V-04 | transaction captures `_state_version`; `commit` rejects mismatch | REQUIRES CURRENT EXECUTION | Two transaction stale-writer scenario |
| V-05 | `RLock` around authority operations; serialized commit | REQUIRES CURRENT EXECUTION | Concurrent transaction fixture and deterministic result capture |
| V-06 | transaction is removed after commit; terminal state enforced | EVIDENCE_GAP | Define exact duplicate-command/idempotency semantics required by CTR-001 before claiming pass |
| V-07 | current candidate mutates canonical state and returns state, but no current event emission surface identified | EVIDENCE_GAP | Do not infer event causality; add verification only after current event contract surface is identified |
| V-08 | no direct event-reentry API identified | EVIDENCE_GAP | Verify event reactions re-enter governed command path at integration boundary |
| V-09 | validation/integrity occurs before publication; mutation under lock | REQUIRES CURRENT EXECUTION | Fault-injection tests for validation/integrity failure and preservation |
| V-10 | no fallback authority in candidate; runtime integration not proven | EVIDENCE_GAP | Current-branch failure fixture must demonstrate mutation stop with no shadow authority |
| V-11 | in-memory restart loses state by design; lifecycle recovery contract is outside candidate | EVIDENCE_GAP / GOVERNANCE BOUNDARY | Verify lifecycle behavior without inventing persistence semantics |
| V-12 | implementation is local and persistence-free | NOT VERIFIED CURRENTLY | Execute with cloud/network unavailable and prove deterministic local operation |
| V-13 | physical persistence absent | BLOCKED | Remains blocked until persistence is separately authorized |
| V-14 | authorization/generation/integrity controls exist; broader authority attacks not proven | REQUIRES INDEPENDENT SECURITY EXECUTION | Execute current security negative matrix SEC-MH04-01…16 |
| V-15 | current evidence schema exists; historical execution tuple exists | NOT VERIFIED CURRENTLY | Generate current evidence records with command/output/artifact/reproducibility references |

## Explicit semantic gaps

### 1. Idempotency

The candidate uses transaction identity and terminal transaction state, but current CTR-001 requires explicit idempotency semantics. A duplicate request model with command identity/correlation identity is not demonstrated by the historical API. This is an **EVIDENCE_GAP**, not a claim that idempotency is absent from the entire system.

### 2. Command / correlation identity

The candidate transaction has `transaction_id`, but current MH-04 requires explicit command/correlation identity and authorization context at the governed command boundary. Transaction identity must not be silently substituted for command identity.

### 3. Event causality

The candidate implementation shown here has no event emission mechanism. V-07 therefore cannot be marked TESTED from candidate unit tests alone.

### 4. Event-driven re-entry

No candidate API establishes event → governed command → authorization → State Authority re-entry. This requires integration verification, not source-level assumption.

### 5. Restore self-test

Historical governance evidence explicitly identified the absence of an explicit restore self-test stage. This remains OPEN until contract/governance disposition and current verification.

### 6. Read-boundary immutability

`read()` returns a detached representation, while `CanonicalState` itself is frozen. The exact CTR-001 meaning of immutable logical revision at the read boundary remains a reconciliation item.

### 7. Restart / recovery

Because the candidate is deliberately in-memory, restart semantics cannot be promoted into durable recovery semantics. Recovery must not introduce database, cache, cloud, or another shadow authority.

## Promotion gate

The candidate MUST NOT be copied or merged into the canonical branch solely from historical evidence.

Required sequence:

`CURRENT CONTRACT → CURRENT INVARIANTS → CURRENT API RECONCILIATION → CURRENT EXECUTION → SECURITY/RED TEAM → EVIDENCE → GOVERNANCE ACCEPTANCE → EXPLICIT IMPLEMENTATION AUTHORIZATION`

## Gate result

**CURRENT CANDIDATE:** HISTORICAL IMPLEMENTATION EVIDENCE  
**CURRENT VERIFICATION:** NOT VERIFIED  
**PROMOTION:** BLOCKED  
**MH-04 ACCEPTANCE:** NOT GRANTED  
**PRODUCTION:** NO-GO
