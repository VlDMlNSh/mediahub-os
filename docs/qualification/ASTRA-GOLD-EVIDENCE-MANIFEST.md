# ASTRA GOLD Evidence Manifest

Date: 2026-09-27

## Immutable baseline

- R4 commit: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`
- R4 tree: `2279612908135418b2b5448d598274ea6741deaa`

## Current qualification evidence

| Gate | Evidence | Status |
|---|---|---|
| Scheduler fencing / remote SHA | PR #96; Scheduler Verification #28 / #29 | PASS |
| Recovery qualification | Recovery #15 / #16 / #17 | PASS |
| MH-05 baseline | MH-05 #126 | PASS |
| Ollama coding E2E | Scheduler Verification #28 / #30 | PASS |
| Crash-idempotent next-task generation | PR #97, scheduler tests | PENDING FINAL CI |
| Production reusable scheduler integration | No fresh production-service evidence yet | NOT VERIFIED |
| Physical multi-node fencing | SentinelX plan: 1 active host, 2 parked | BLOCKED |
| Reboot persistence | No fresh qualification run | NOT VERIFIED |
| Backup/restore drill | No fresh qualification run | NOT VERIFIED |
| Security qualification | Existing CI coverage; full GOLD pass pending | PARTIAL |
| Independent verification | Not completed | NOT VERIFIED |
| PRE-SOAK | Prerequisites incomplete | NOT REACHED |
| 24h soak | Not authorized / not started | NOT STARTED |
| GOLD authorization | Not granted | NOT AUTHORIZED |

## Qualification run IDs

- Scheduler Verification #28: `36329177593`
- Recovery Qualification #15: `36329177623`
- MH-05 #126: `36329177602`
- Scheduler Verification #29: `36329533535`
- Recovery Qualification #16: `36329533545`
- Scheduler Verification #30: `36330079106`
- Recovery Qualification #17: `36330079195`
- MH-05 #127: `36329533528`
- MH-05 #128: `36330079161`

## Current production infrastructure truth

- `mh-dev-01`: SentinelX active/operational.
- `mh-dev-02`: parked under current SentinelX Free active-host limit.
- `Voktors-Mini.Dlink`: parked under current SentinelX Free active-host limit.
- `mediahub-astra.service`: active and enabled on `mh-dev-01`.
- The currently installed service is a resident runtime process; it is not yet fresh evidence of the reusable durable scheduler loop.

## Certification rule

No `VERIFIED`, `QUALIFIED`, `AUTHORIZED`, `GOLD`, or `24x7 ACTIVE` status is asserted unless a fresh evidence pointer for the corresponding gate exists.

The 24h soak requires explicit human confirmation after PRE-SOAK is PASS.
