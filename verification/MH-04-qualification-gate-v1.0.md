# MH-04 Qualification Gate v1.0

Status: OPEN

Qualification is not granted by implementation or CI success alone.

## Authorized scope
The 2026-09-06 Product Owner acceptance authorizes the deterministic in-memory State Authority foundation only. Physical persistence, HA, production release and unrelated capability implementation remain unauthorized.

## Required evidence
- applicable V-01…V-15 current runtime execution with reproducible evidence;
- V-13 recorded as BLOCKED because physical persistence is outside the authorized foundation scope;
- independent Security/Red Team execution;
- command/correlation identity in mutation evidence;
- negative-path evidence for unauthorized, stale, duplicate, forged and shadow-authority scenarios;
- concurrency evidence;
- event causality/re-entry evidence;
- restart/recovery boundary evidence without claiming durability;
- contract/invariant traceability with no drift;
- exact Git SHA, branch, environment, command, exit code, timestamps and artifacts.

## Exit criteria
All applicable tests must be executed and assessed. Any NOT_VERIFIED, unexplained contradiction, security failure, invariant violation, or evidence identity gap blocks qualification. A blocked item must have explicit governance scope and cannot be silently converted to pass.

## Production rule
Qualification does not authorize release. Release requires separate product, security, privacy/legal, operational and release acceptance.
