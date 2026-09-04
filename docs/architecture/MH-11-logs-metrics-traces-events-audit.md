# MH-11 — Logs / Metrics / Traces / Events / Audit

Status: PROPOSED

These are distinct semantic records. Logs provide operational context; metrics provide measurements; traces provide execution correlation; events represent typed occurrences; audit records provide accountability. None is canonical state or mutation authority.

Mutation remains Authorization → Consumer Boundary → State Authority. Diagnostic observation is read-only unless it enters the ordinary mutation path.
