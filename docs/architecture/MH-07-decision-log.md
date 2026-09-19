# MH-07 — Decision Log

Status: CANDIDATE.

D1 — Keep Configuration, Policy, Authorization and Runtime State separate. Rationale: preserve P0-03 authority. Status CANDIDATE.

D2 — Keep v1 device-local/transient/bounded/non-executable. Rationale: match P0-07 governance baseline and reduce attack surface. Status CANDIDATE.

D3 — Fail closed on ambiguity, malformed/unsupported policy and stale revision. Rationale: explicit safety baseline. Status CANDIDATE.

D4 — Do not solve the P0-07 mutation gap by changing P0-03…P0-06. Status GOVERNANCE CONSTRAINT.

D5 — Defer physical persistence and technology selection. Status GOVERNANCE CONSTRAINT.
