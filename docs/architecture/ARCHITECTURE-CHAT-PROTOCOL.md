# MediaHub OS — Architecture Chat Protocol

Status: PROPOSED / GOVERNANCE CONVENTION

## Purpose

MH-1…MH-23 are canonical architecture custody chats. They are not implementation workspaces and must remain concise, evidence-driven, and free of prolonged implementation discussion.

## Source of truth

GitHub is the durable external synchronization layer. Architecture chats may hold the working canonical record, but long-term continuity must not depend on ChatGPT chat history alone.

## Separation of concerns

### Architecture chats MH-1…MH-23

Allowed:
- architecture decisions;
- canonical contracts;
- evidence assessment;
- reconciliation;
- contradiction and unknown registers;
- acceptance/freeze state;
- master prompts and reverse-master prompts;
- implementation impact at architectural level.

Forbidden:
- feature implementation;
- routine coding/debugging;
- long implementation threads;
- speculative technology selection without an ADR/evidence gate;
- treating implementation output as architectural evidence without verification.

### Development chat

The separate development chat performs implementation, tests, refactoring, CI/debugging, and operational work.

It may query architecture chats using a Master Prompt and return a Reverse Master Prompt / evidence package.

## Mandatory method

Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze

No ACCEPTED, FROZEN, VERIFIED, QUALIFIED, or PRODUCTION READY status without evidence.

## Master Prompt

The development chat should request from an architecture chat:

1. current canonical state;
2. applicable frozen baselines;
3. current constraints/invariants;
4. permitted implementation scope;
5. explicit blockers;
6. unknowns requiring verification;
7. acceptance criteria;
8. required evidence to return.

## Reverse Master Prompt

The development chat returns:

1. exact branch/head commit;
2. changed files;
3. implementation status;
4. targeted/full test results;
5. security/capability/persistence scans;
6. deviations from architecture;
7. unresolved blockers;
8. evidence references;
9. clean/synchronized repository state.

## Freeze discipline

Architecture chats never infer freeze from implementation existence. Freeze requires explicit governance acceptance backed by evidence.

## MH-7 application

MH-7 remains CANDIDATE until P0-07 verification and the P0-07→P0-05 authorization composition governance gap are resolved. P0-03…P0-06 frozen contracts must not be changed merely to bypass the gap.
