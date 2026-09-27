# MH-01 REVERSE MASTER PROMPT — RETURN FROM DEVELOPMENT

Purpose: return implementation findings to the MH-01 architecture custodian without contaminating the architecture chat with development discussion.

## Required header

- MH domain:
- Development task/change ID:
- Repository:
- Branch:
- Exact commit:
- Date:
- Development status: IMPLEMENTED / TESTED / BLOCKED / DEFERRED

## Required evidence

1. Requirements consumed from MH-01.
2. Architecture artifact versions/SHAs consumed.
3. Files/components changed.
4. Tests and exact results.
5. Security/authority impact.
6. Privacy/data-flow impact.
7. Compatibility impact.
8. Contradictions discovered.
9. Unknowns discovered.
10. Proposed decision, if any.
11. Whether governance action is required.

## Mandatory prohibitions

Do not declare architecture accepted or frozen from a development chat. Do not alter P0-03…P0-06 semantics. Do not convert implementation behavior into canonical architecture without review. Do not bury breaking changes inside implementation reports.

## Promotion flow

`Development evidence → Reverse Master Prompt → Architecture reconciliation → Governance decision → Repository canonical update → Acceptance → Freeze`.

A Reverse Master Prompt is evidence/input to architecture, not an authority grant.