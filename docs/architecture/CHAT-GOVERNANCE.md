# Architecture Chat Governance

## Purpose
MH-01…MH-23 are architectural custodians. They preserve canonical model, decisions, invariants, evidence, contradictions and master prompts. They are not implementation/development chats.

## Development separation
Implementation is performed only in the dedicated development chat. Architecture chats must not accumulate implementation sessions, debugging, prolonged design-by-chat, code iteration, or operational troubleshooting.

## Allowed architecture-chat work
- architecture decisions;
- compatibility/reconciliation reviews;
- acceptance/freeze gates;
- evidence and contradiction registers;
- master prompt / reverse master prompt updates;
- concise architectural clarification required to preserve canonical intent.

## Forbidden
- feature implementation;
- code development or refactoring;
- long-running debugging;
- implementation task tracking;
- technology selection by convenience;
- silent modification of parent decisions.

## Cross-chat protocol
Development chat may request from an architecture chat:
1. Master Prompt — authoritative input constraints for the next development task.
2. Reverse Master Prompt — development result/decision packet to return for architectural review.

Architecture chat responds with bounded artifacts, not implementation work.

## Status discipline
PROPOSED ≠ ACCEPTED ≠ FROZEN. Research never becomes canonical automatically.

## GitHub role
GitHub is the durable repository mirror/evidence store for canonical architecture artifacts. Chat remains the active architectural custodian; GitHub provides versioned synchronization. A GitHub artifact must not be treated as a governance approval unless its status explicitly records approval.
