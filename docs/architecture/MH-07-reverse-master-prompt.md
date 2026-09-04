# MH-7 — REVERSE MASTER PROMPT / DEVELOPMENT RETURN

## Purpose

Return verified implementation evidence to MH-7 without turning the architecture chat into a development workspace.

## Required return package

1. Branch name.
2. Exact HEAD commit.
3. Base commit.
4. Changed files.
5. Targeted tests: exact command and result.
6. Full regression: exact command and result.
7. Security scan result.
8. Capability/forbidden-call scan result.
9. Persistence scan result.
10. Relevant integration tests.
11. Exact deviations from MH-7.
12. Blockers and governance questions.
13. Unknowns discovered during implementation.
14. Repository clean/synchronized status.
15. Evidence references sufficient for independent verification.

## Status discipline

IMPLEMENTED is not VERIFIED.
VERIFIED is not ACCEPTED.
ACCEPTED is not FROZEN unless governance explicitly records the freeze.

## P0-07 gate

Do not claim production qualification while the P0-07→P0-05 authorization composition blocker remains unresolved or required evidence is missing.

## Scope discipline

Do not modify P0-03…P0-06 frozen contracts merely to bypass a P0-07 blocker. Escalate architectural changes as decisions/ADRs.
