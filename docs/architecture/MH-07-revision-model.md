# MH-07 — Revision / Concurrency Model

Status: CANDIDATE.

Configuration and Policy require explicit revision/version metadata where publication or concurrency requires it. A candidate is bound to the authoritative revision/generation observed when produced. Publication verifies expected generation/version and fails closed when stale.

Replacement is complete-document replacement, not implicit merge. No LWW, hidden rebase, patch merge or retry. Rollback is an explicit new candidate derived from an identified accepted revision.

P0-04 generation/state-version checks remain authoritative for runtime mutation. Current P0-07 objects do not yet expose complete revision/publication metadata.
