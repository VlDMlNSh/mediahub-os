# MH-04 — Historical P0-04 Candidate Reconciliation v2

**Status:** RECONCILIATION / NOT ACCEPTED  
**Candidate commit:** `456deb9aadd3cae7d8978a7d89f540e1a029b7f4`  
**Candidate blob:** `9432a5a790ab24ae0bbc7dce2663f3e8b34743fc`  
**Current target:** MH-04 / CTR-001  
**Current implementation authorization:** BLOCKED

## Executive result

The historical candidate contains a substantial deterministic in-memory transaction implementation, but historical execution does not constitute current qualification. The candidate may be selectively reused only after current contract, invariant, security and verification reconciliation.

## Observed candidate capabilities

Source inspection confirms:

- typed generation and state-version tracking;
- canonical state representation;
- transaction handles with ACTIVE/COMMITTED/ABORTED lifecycle;
- structural payload validation with bounded depth/node/string/key limits;
- integrity validator boundary;
- authorization policy checks for begin/commit/abort/snapshot/restore;
- stale generation/version rejection;
- atomic publication under a re-entrant lock;
- immutable checkpoint authority-token binding;
- restore generation/schema/binary compatibility checks;
- read-side thawing of canonical state.

These observations are source evidence, not current runtime qualification.

## Reconciliation gaps

| Requirement | Candidate observation | Current disposition |
|---|---|---|
| Sole canonical authority | class is StateAuthority candidate | REQUIRES current boundary verification |
| Command identity | transaction identity exists | INSUFFICIENT for CTR-001 command contract |
| Correlation identity | not demonstrated | EVIDENCE GAP |
| Consumer Boundary | not demonstrated in candidate | EVIDENCE GAP |
| Authorization propagation | transaction context is retained | REQUIRES execution/security verification |
| Concurrency | lock + state version present | REQUIRES adversarial execution |
| Idempotency | no explicit command-id semantics demonstrated | EVIDENCE GAP |
| Event emission | not demonstrated | EVIDENCE GAP |
| Event re-entry | not demonstrated | EVIDENCE GAP |
| Failure/no-shadow-authority | local failure semantics exist | REQUIRES system-level verification |
| Recovery self-test | historical remediation exists separately | REQUIRES current execution |
| Read-boundary immutability | freeze/thaw mechanism present | REQUIRES negative execution |
| Physical persistence | absent | CORRECTLY NOT AUTHORIZED |
| Evidence generation | not integrated into mutation path | EVIDENCE GAP |

## Reuse decision

**CONDITIONAL REUSE ONLY.** The candidate is a technical reference and possible implementation seed. It must not be merged unchanged into the canonical production branch.

Required promotion order:

`CURRENT CONTRACT → CURRENT INVARIANTS → CANDIDATE RECONCILIATION → IMPLEMENTATION DELTA → CURRENT EXECUTION → SECURITY/RED TEAM → EVIDENCE → GOVERNANCE ACCEPTANCE → EXPLICIT IMPLEMENTATION AUTHORIZATION`

## Prohibited promotion

Do not promote historical 123/123 regression or 13/13 targeted historical results as current qualification. Do not introduce physical persistence, a second authority, event-driven bypass, cloud authority, or unqualified recovery authority.

## Current conclusion

The candidate substantially reduces implementation uncertainty but does not remove the current MH-04 gate. Current runtime qualification remains **NOT VERIFIED** and production remains **NO-GO**.
