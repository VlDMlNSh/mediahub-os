# MH-04 Failure Semantics

ambiguity -> fail closed
malformed input -> reject
missing authorization -> deny
stale transaction -> reject
unknown identity -> deny/quarantine
unknown device -> quarantine/deny
invalid credential -> deny
security decision unavailable -> deny
cloud unavailable -> local degraded operation where safe
AI unavailable -> deterministic core continues
State Authority unavailable -> no shadow/fallback mutation authority

Security failure must never widen trust or capability.