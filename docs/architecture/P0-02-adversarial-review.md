# P0-02 — Adversarial Architecture Review v1.0

**Status:** Review recorded; architecture acceptance remains pending.  
**Branch:** `architecture/p0-02-state-authority-design`  

## Review objective

Attempt to identify architectural paths that could allow invalid, stale, unauthorized, corrupted, partially applied, or externally controlled state to become canonical.

## Findings

### A-01 — Partial commit / torn canonical state
**Risk:** Critical if readers can observe a mixture of old and new state.  
**Disposition:** Closed at design level.

P0-02 now requires an explicit commit linearization point. Before that point readers retain the previous canonical revision; after it they observe one complete new revision. The concrete atomic primitive remains implementation-specific and therefore must be demonstrated by tests later.

### A-02 — Caller-selected state version
**Risk:** High if a caller can manufacture a future or conflicting canonical revision.  
**Disposition:** Closed at design level.

State-version advancement is owned by State Authority and occurs atomically with successful publication. Candidate input cannot arbitrarily choose the resulting canonical version.

### A-03 — Stale transaction overwrite
**Risk:** High if an older transaction silently overwrites newer canonical state.  
**Disposition:** Closed at design level.

Transactions are bound to observed generation/state version. Stale commit must fail closed; implicit last-writer-wins is prohibited.

### A-04 — Integrity confused with compatibility
**Risk:** High if a compatible state is assumed trustworthy merely because versions match.  
**Disposition:** Closed at design level.

Generation compatibility and integrity validation are explicitly separate acceptance gates.

### A-05 — Restore bypass
**Risk:** Critical if recovery can install state without normal authority, validation, or authorization.  
**Disposition:** Closed at design level.

Restore is explicitly a State Authority transition and creates a new accepted state revision. Invalid or unauthorized targets cannot replace canonical state.

### A-06 — Checkpoint substitution/tampering
**Risk:** High if checkpoint metadata/payload is trusted before validation.  
**Disposition:** Closed at design level.

Checkpoint data is treated as untrusted at the persistence/read boundary until authenticity, schema, generation, and integrity are validated.

### A-07 — Generic transaction capability as hidden privilege
**Risk:** High if opening a transaction implicitly grants all state operations.  
**Disposition:** Closed at design level.

Authorization is operation-specific, including checkpoint and restore operations.

### A-08 — Deserialization trust boundary
**Risk:** High if serialized state can execute code or bypass type/bounds validation.  
**Disposition:** Closed at design level.

Serialized state is explicitly untrusted input. Unsafe deserialization is prohibited; schema, types, bounds, generation, and integrity must be validated before candidate acceptance.

### A-09 — External/AI mutation path
**Risk:** Critical if AI/network/UI/plugin input can reach canonical mutation directly.  
**Disposition:** Closed at design level.

External content remains data/proposal/request and cannot acquire a direct State Authority mutation primitive merely by presenting a state-shaped payload.

### A-10 — Recovery history ambiguity
**Risk:** Medium if restore mutates or re-identifies an existing checkpoint.  
**Disposition:** Closed at design level.

Restore creates a new authoritative state revision and does not rewrite checkpoint identity.

## Residual implementation risks

The following are intentionally **not** considered architecturally solved until implementation evidence exists:

- atomic publication under actual persistence technology;
- crash consistency;
- transaction isolation under concurrent writers;
- cryptographic/authenticity mechanism for checkpoints;
- serialization format safety;
- durability semantics;
- retention/deletion policy;
- rollback interaction with generation upgrades;
- audit/event integrity;
- denial-of-service/resource exhaustion controls.

These require separate implementation and security evidence.

## Verdict

**Architecture hardening result: PASS with residual implementation obligations.**

**P0-02 acceptance:** PENDING explicit architecture acceptance.  
**Implementation authorization:** NOT GRANTED.  
**Persistence authorization:** NOT GRANTED.

No historical MH-02…MH-16 responsibility is inferred from this review.
