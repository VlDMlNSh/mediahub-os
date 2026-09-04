# MH-12 ARCHITECTURE CHAT CHARTER

## Purpose

MH-12 is a reference architecture chat for Security Architecture. It is a **canonical architecture work surface**, not a development environment.

## Allowed

- architecture decisions;
- evidence reconciliation;
- threat modeling;
- security-boundary definition;
- contract/invariant definition;
- ADR preparation;
- contradiction and unknown registers;
- acceptance criteria;
- concise governance decisions;
- synchronization of durable architecture records to GitHub.

## Prohibited

- production implementation;
- feature development;
- prolonged debugging;
- implementation experiments that change canonical behavior;
- treating chat history as the durable source of truth;
- silently changing frozen baselines;
- declaring production readiness without verification and governance evidence.

## Source of record

GitHub repository `VlDMlNSh/mediahub-os` is the durable source of record for architecture artifacts. The chat provides architectural context and decisions; GitHub preserves them for long-term development continuity.

## Development separation

Implementation occurs in a dedicated development chat/workspace and implementation branches. Development may consume MH-12 through the Master Prompt and Reverse Master Prompt. Development must return architecture-affecting contradictions/questions to the architecture workspace instead of resolving them by modifying architecture implicitly.

## Change discipline

Architecture change:
1. Evidence
2. Contradiction analysis
3. Decision/ADR
4. Governance authorization
5. Implementation impact
6. Verification
7. Acceptance
8. Freeze

## Clean-chat rule

Once a decision is recorded, do not repeat long exploratory implementation discussions in this chat. Use concise references to the durable artifact and move implementation work elsewhere.
