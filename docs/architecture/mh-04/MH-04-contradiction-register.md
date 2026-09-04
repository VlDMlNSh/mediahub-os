# MH-04 Contradiction Register

## Current result
No explicit contradiction identified against the inherited MH-01/MH-02/MH-03 record or protected P0-03..P0-06 constraints during the completed review passes.

## Protected invariants
- State Authority remains sole canonical mutation authority.
- Runtime is not State Authority.
- No shadow/fallback authority exists.
- P0-05 Consumer/Integration Boundary remains mandatory.
- Command/Event separation remains intact.
- Security may deny or quarantine but may not mutate canonical state.
- Trust tier does not imply authorization.

## Historical/repository reconciliation
The repository governance record explicitly separates architecture custodians from implementation chats and defines Master Prompt / Reverse Master Prompt exchange. MH-03 records the same no-second-authority, command/event and failure discipline. These records are compatible with MH-04.

## Trigger condition
If future evidence requires changing a frozen parent decision: `CONTRADICTION / GOVERNANCE CHANGE REQUIRED`. No silent repair is permitted.