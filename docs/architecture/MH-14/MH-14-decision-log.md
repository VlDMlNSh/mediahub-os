# MH-14 — DECISION LOG

## MH14-D001 — Persistence is subordinate to State Authority
Status: ACCEPTED / ARCHITECTURAL INVARIANT

Persistence stores and retrieves representations. It cannot determine canonical state or authorize mutation.

## MH14-D002 — Physical persistence remains implementation-neutral
Status: OPEN / GOVERNANCE REQUIRED

No database, filesystem, WAL, journal, object store or hybrid is selected by MH-14.

## MH14-D003 — Recovery uses candidate-state promotion
Status: ACCEPTED

Recovered data must pass validation, integrity and compatibility checks before State Authority may restore it.

## MH14-D004 — Backup is not HA
Status: ACCEPTED

Current reliability baseline is SINGLE NODE / NO HA. Replication and HA require separate governance.

## MH14-D005 — Recovery capability requires restore verification
Status: ACCEPTED

Backup without a successful restore and runtime/state validation remains UNVERIFIED.

## MH14-D006 — Exact RPO/RTO remain TBD
Status: OPEN

No numerical target is canonical without workload/business evidence.

## MH14-D007 — Development and architecture are separated
Status: ACCEPTED

Architecture chats MH-1…MH-23 are reference/governance spaces. Implementation and debugging occur in a separate development chat. Master/reverse-master prompts define the interface.

## MH14-D008 — GitHub is durable external architecture record
Status: ACCEPTED

Chat history is not the sole durable record. Architecture artifacts are maintained under docs/architecture/ in the repository.

## MH14-D009 — P0-07 is not repaired by MH-14
Status: ACCEPTED

MH-14 preserves the frozen P0-03…P0-06 contracts and does not independently resolve the P0-07 mutation-publication governance/API gap.

## MH14-D010 — No silent durability claim
Status: ACCEPTED

A successful persistence call may only claim the durability semantics actually established by the implementation contract and evidence.

## MH14-D011 — Qualification-ready without premature closure
Status: ACCEPTED / ARCHITECTURAL GOVERNANCE

MH-14 may enter autonomous qualification once its architecture boundary, invariants, domain model and explicit open-gate register are internally reconciled. Qualification readiness does not mean ACCEPTED/FROZEN, implementation authorization, HA authorization or production authorization.

## MH14-D012 — Qualification cannot mutate architecture authority
Status: ACCEPTED / ARCHITECTURAL GOVERNANCE

Autonomous qualification may inspect, compare, test and report evidence. It cannot redefine State Authority, silently select a physical persistence backend, approve unresolved governance decisions, authorize implementation, release or production.

## MH14-D013 — Erroneous architecture records are superseded, not rewritten
Status: ACCEPTED / ARCHITECTURAL GOVERNANCE

Historical Git commits remain immutable evidence. Erroneous current artifacts are corrected or superseded by an explicit reconciliation artifact. No history rewrite or destructive erasure is used to manufacture a clean provenance record.
