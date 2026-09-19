# MH-07 — Defaults

Status: CANDIDATE.

Defaults are explicit data, never undocumented behavior. Every security-relevant default requires owner, rationale, security impact, version semantics and evidence.

Critical behavior defaults fail safe: missing policy match is DENY; malformed/unsupported policy is DENY; missing authorization is DENY; stale publication is rejected; missing persistence is not silently replaced by a cache/checkpoint.

Reset names its target default; reset is not delete. Security-affecting defaults require explicit decision evidence.
