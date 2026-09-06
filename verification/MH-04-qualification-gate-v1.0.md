# MH-04 Qualification Gate v1.0

Status: OPEN

Qualification is not granted by implementation or CI success alone.

## Required evidence
- V-01…V-15 current runtime execution with reproducible evidence.
- independent Security/Red Team execution.
- command/correlation identity in all mutation evidence.
- negative-path evidence for unauthorized, stale, duplicate, forged and shadow-authority scenarios.
- restart/recovery boundary evidence.
- contract/invariant traceability with no drift.
- exact Git SHA, branch, environment, command, exit code, timestamps and artifacts.

## Exit criteria
All applicable tests must be executed and assessed. Any NOT_VERIFIED, unexplained contradiction, security failure, invariant violation, or evidence identity gap blocks qualification.

## Production rule
Qualification does not itself authorize release. Release requires separate product, security, privacy/legal, operational and release acceptance.
