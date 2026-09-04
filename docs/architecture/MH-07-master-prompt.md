# MH-7 — MASTER PROMPT FOR DEVELOPMENT CHAT

## Authority

This prompt requests the current canonical MH-7 architecture. It is not an implementation instruction by itself.

## Request

Return only the minimum architecture package required to implement or verify Configuration/Policy work without violating MH-7 or frozen P0-03…P0-06.

Required output:

- canonical Configuration model;
- canonical Policy model;
- lifecycle and mode constraints;
- validation stages;
- revision/stale semantics;
- policy evaluation semantics;
- authorization boundary;
- P0-05/P0-04 interaction;
- AI/plugin/proposal restrictions;
- persistence boundary;
- security invariants;
- current blockers;
- unknowns;
- acceptance criteria;
- exact evidence required for return.

## Non-negotiable

Configuration is desired behavior, Policy is admissibility, Authorization is principal/operation authority, Runtime State is actual effective state, and P0-04 State Authority is the sole canonical mutation authority.

No direct mutation, self-grant, wildcard, inheritance, hidden merge, LWW, hidden retry/rebase, executable configuration/policy, hidden persistence, network execution, or arbitrary plugin execution.

P0-07 mutation publication is blocked until the P0-07→P0-05 authorization composition gap receives an explicit governance-approved resolution.

## Development boundary

Implementation occurs in the separate development chat/repository branch. This architecture chat is not the implementation workspace.
