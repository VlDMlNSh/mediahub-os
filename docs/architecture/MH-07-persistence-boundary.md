# MH-07 — Persistence Boundary

Status: CANDIDATE.

Physical persistence is NOT AUTHORIZED by P0-07. Logical ownership is defined without selecting a database, file format, cache, KV store or cloud service.

Any future persistence layer must remain subordinate to the configuration/policy lifecycle and must not become State Authority, hidden checkpoint, recovery source or authorization store without an explicit decision.

No network/cloud transfer is implicit. External sources are proposals until local validation, policy and authorization complete.
