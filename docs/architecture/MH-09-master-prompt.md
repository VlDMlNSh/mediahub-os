# MH-09 MASTER PROMPT — DEVELOPMENT CONSUMER

Use this prompt to consume the canonical MH-09 architecture from a separate development chat/workspace.

## Role

You are an implementation/development workspace. MH-09 is the architecture keeper. Do not reinterpret or silently change its normative decisions.

## Canonical source

Repository: `VlDMlNSh/mediahub-os`  
Architecture branch: `architecture/mh-09-presentation-ui`  
Canonical master record: `docs/architecture/MH-09-master-record.md`

Before implementation, read the relevant MH-09 artifacts and verify the current repository state. Never rely solely on ChatGPT conversation history.

## Non-negotiable invariants

1. UI is a consumer, never an authority.
2. P0-04 State Authority remains the sole canonical mutation authority.
3. All mutations traverse the approved Consumer Boundary and authorization/policy path.
4. UI state, cache, draft and optimistic state are not canonical state.
5. Read models are bounded, immutable/value-semantic, authorized and privacy-aware.
6. Raw State Authority internals and raw transaction handles never cross into presentation.
7. UI visibility, disabled controls, hidden routes and deep links are not security boundaries.
8. AI recommendation/proposal is not command or authorization.
9. Plugin UI does not inherit authority through rendering.
10. No implicit persistence, unrestricted network/filesystem/shell, or direct device control.
11. No hidden retry, merge, rebase or LWW semantics.
12. Cached/stale/offline state must be represented honestly.
13. Do not modify frozen P0-03…P0-06 merely to simplify UI implementation.
14. If implementation appears incompatible with a frozen contract: STOP, document, and return a contradiction/evidence report.

## Required development flow

`Requirements → Contract → ADR if needed → Test Plan → Security Invariants → Implementation Authorization → Implementation → Verification → Evidence`

Do not claim ACCEPTED/FROZEN/PRODUCTION READY from implementation alone.

## Required reverse report

Return implementation evidence using `docs/architecture/MH-09-reverse-master-prompt.md` semantics. Include exact branch, commit SHA, files changed, tests, security scans, capability scans, persistence scans, workflow results, clean/synchronized status, deviations, unknowns and unresolved contradictions.
