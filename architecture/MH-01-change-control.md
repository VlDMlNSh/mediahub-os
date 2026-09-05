# MH-01 Change Control

Status: PROPOSED / REQUIRES VERIFICATION.

| Class | Meaning | Minimum gate |
|---|---|---|
| A | Documentation-only | Owner review; no contract effect |
| B | Non-authoritative implementation | Domain review + tests |
| C | New capability | Architecture + security + verification |
| D | Contract change | Governance review + compatibility analysis |
| E | Authority/security model change | Explicit governance decision + full verification |
| F | Breaking architectural change | Full review + migration + verification + acceptance + freeze |

## Mandatory rules

- P0-03…P0-06 changes are always separate governance changes.
- No breaking change may be hidden inside a documentation or implementation change.
- A development chat may propose a change but cannot accept/freeze it.
- Unknowns cannot be resolved by assumption.
- Irreversible changes require explicit governance before implementation.
- Every change records evidence, decision, consequences, affected MH domains and verification method.

## Status lifecycle

`PROPOSED → REVIEWED → AUTHORIZED → IMPLEMENTED → TESTED → ACCEPTED → FROZEN`

A failure may move an item to `BLOCKED` or `DEFERRED`; it does not silently become accepted.