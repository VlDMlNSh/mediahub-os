# MH-15 — Contradiction Register

Status: ACTIVE / NO ACCEPTANCE YET

## Governing rule

Contradictions between MH-1…MH-15, P0-03…P0-07, runtime, security, privacy, persistence, observability, update and recovery architecture MUST be surfaced explicitly.

A contradiction MUST NOT be resolved by silently modifying a frozen baseline.

## Known dependency checks

- MH-14 Persistence vs MH-15 filesystem/storage: persistence remains subordinate to State Authority.
- MH-12 Security vs MH-15 host privilege: host privilege does not bypass authorization.
- MH-11 Observability vs MH-15 telemetry: observation is not authority and private data is not automatically telemetry.
- MH-10 AI / MH-8 Plugins vs MH-15 shell/device/filesystem: arbitrary privileged execution is forbidden.
- MH-7 Policy vs MH-15 resource/self-healing: policy and authorization precede privileged host actions.
- MH-16 Update/Recovery vs MH-15 lifecycle: installer/update/recovery remain separate trust/lifecycle mechanisms, not State Authority.

Current verdict: no accepted contradiction is established; all future conflicts require explicit governance review.
