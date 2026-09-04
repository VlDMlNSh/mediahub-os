# MH-13 — MASTER PROMPT / ARCHITECTURE REFERENCE CONTROL POINT

**Purpose:** durable Git-backed control point for the MH-13 Privacy / Data Governance architecture reference chat.

## Role of this document

This repository record preserves the architecture-reference operating contract independently of ChatGPT conversation storage.

MH-13 is an architecture reference domain. The architecture chat is a keeper of the canonical architectural context, not a development workspace.

## Operating rules

1. Architecture reference chats MH-01…MH-23 are authoritative architecture-context holders for their respective domains.
2. Development is performed in a separate development chat/workspace.
3. Architecture chats MUST NOT be used for production implementation, prolonged implementation discussion, or implementation debugging.
4. Development may consult architecture chats through a Master Prompt / Reverse Master Prompt exchange.
5. Material architecture changes discovered during development must return through governance/review and be recorded in Git; they must not silently mutate the architecture reference context.
6. Git is the durable long-term record and MUST be used to preserve accepted/reconstructed architecture state, provenance, decisions, unknowns and governance status.
7. ChatGPT conversation history MUST NOT be treated as the sole long-term storage mechanism.
8. No architectural artifact may be presented as historically recovered unless its historical lineage is evidenced.

## MH-13 authority boundary

MH-13 owns Privacy / Data Governance.

MH-13 is NOT State Authority, canonical mutation authority, Persistence authority, Media authority, AI authority, or Cloud authority.

Canonical mutation remains exclusively with State Authority through Boundary → Authorization → State Authority.

## Current MH-13 control point

- Historical original: NOT RECOVERED.
- Reconstruction: AUTHORIZED.
- Reconstructed artifact: `docs/architecture/MH-13-privacy-data-governance.md`.
- Reconstruction registers: `docs/architecture/MH-13-reconstruction-registers.md`.
- Current artifact status: RECONSTRUCTED / PROPOSED unless and until the explicit governance state in Git is updated.
- Frozen: NO unless separately authorized.
- Production implementation: NOT AUTHORIZED by this architecture record.

## Downstream boundaries

- MH-12: Security / trust / authentication / authorization.
- MH-14: Persistence / durable lifecycle.
- MH-17: Device/protocol domain and device-specific privacy application.
- MH-18: Media/content-specific privacy application.
- MH-21: Hybrid-cloud/distributed-AI privacy application.
- MH-23: Long-term compatibility/migration/evolution.

## Non-negotiable privacy invariants

Purpose-bound use; minimization; privacy-aware classification before applicable external egress; explicit governed transfer; bounded retention; defined deletion semantics coordinated with Persistence; protected-data redaction from unauthorized telemetry/diagnostics/audit/external channels; auditability without protected payload disclosure; no AI privacy authority; no implicit provider trust; no hidden mutation path; unknown classification does not authorize external transfer.

## Historical lineage rule

The forensic conclusion remains permanently relevant: the original historical MH-13 artifact was not recovered. Any reconstructed artifact must preserve this fact and must never rewrite the historical lineage.

## Development handoff

The development workspace should consume MH-13 as architecture input and return implementation findings, proposed changes and verification evidence through normal governance. It must not reinterpret the reconstructed artifact as production authorization.

## Reverse Master Prompt contract

A Reverse Master Prompt returned to a development chat should contain, at minimum:

- domain: MH-13 Privacy / Data Governance;
- historical original: NOT RECOVERED;
- reconstruction: AUTHORIZED;
- current Git artifact and commit/PR lineage;
- current governance status;
- authority boundaries;
- dependencies and downstream contracts;
- non-negotiable invariants;
- explicit UNKNOWN / REQUIRES VERIFICATION items;
- implementation authorization state;
- required return path for proposed architecture changes.
