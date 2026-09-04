# MH-09 REVERSE MASTER PROMPT — DEVELOPMENT → ARCHITECTURE

Return implementation evidence to the MH-09 architecture keeper. This is an evidence protocol, not permission to alter architecture.

## Required report

### 1. Identity
- Project/repository
- development branch
- exact HEAD commit SHA
- base/reference commit
- date/time

### 2. Scope
- requirements implemented
- contracts implemented
- files changed
- files intentionally not changed
- architecture documents referenced

### 3. Verification
- targeted tests: exact command + result
- full tests: exact command + result
- contract tests
- integration tests
- failure/offline/concurrency tests
- accessibility tests
- security/capability scans
- persistence/forbidden-access scans
- workflow/run identifiers and results where available

### 4. Security evidence
Explicitly report whether any path exists from UI/presentation to:
- State Authority internals
- raw transaction
- persistence authority
- unrestricted filesystem
- unrestricted network
- shell/subprocess
- direct device control
- plugin execution
- implicit capability escalation

### 5. State semantics
Report evidence for:
- current/stale/cached/unavailable
- generation/revision
- pending/accepted/committed/rejected/failed/cancelled/unknown
- optimistic UI behavior
- retry semantics
- conflict handling

### 6. Deviations
For every deviation from MH-09:
- exact architectural rule
- implementation behavior
- reason
- evidence
- proposed disposition

Never silently resolve a contradiction.

### 7. Status
Use only the approved vocabulary:
`VERIFIED, OBSERVED, HISTORICAL, FROZEN, ACCEPTED, PROPOSED, CANDIDATE, IMPLEMENTED, TESTED, BLOCKED, DEFERRED, UNKNOWN, REQUIRES VERIFICATION`.

Do not use `PRODUCTION READY` or `QUALIFIED` unless a separate governance process has explicitly established those states.

### 8. Repository integrity
Report:
- working tree clean/dirty
- synchronization state
- unexpected files
- unexpected commits
- merge/rebase status

### 9. Governance handoff
State explicitly:
- what is evidenced
- what remains unverified
- what is blocked
- what requires architecture decision
- whether implementation authorization remains valid for the next step

The architecture keeper decides whether evidence changes the canonical architectural state. Development must not self-accept or self-freeze MH-09.
