# MH-14 — Persistence Architecture Package

Status: **QUALIFICATION-READY / ARCHITECTURE NOT YET ACCEPTED-FROZEN**

This directory is the durable GitHub record for the MH-14 architecture track.

## Primary documents

- `MH-14-persistence-architecture.md` — canonical architecture baseline
- `MH-14-gaps.md` — etalon gap and contradiction register
- `MH-14-qualification-blueprint.md` — autonomous qualification queue and gates
- `MH-14-master-prompt.md` — interface from architecture to development chats
- `MH-14-reverse-master-prompt.md` — interface from development chats back to architecture
- `MH-14-decision-log.md` — durable architectural decisions

## Etalon status

MH-14 is considered **architecture-complete enough for autonomous qualification**, but not yet accepted/frozen. The distinction is intentional:

- architecture boundary: defined;
- authority model: defined;
- persistence domains: defined;
- consistency/recovery/security/privacy semantics: defined;
- evidence/governance gaps: explicitly registered;
- physical persistence implementation: NOT AUTHORIZED;
- production qualification: NOT AUTHORIZED.

## Governance

MH-14 is an architecture-only track. Development, debugging and prolonged implementation discussion belong in the separate development chat.

Physical persistence implementation remains **NOT AUTHORIZED** until the explicit implementation gate is passed.

## Core invariant

> Persistence stores canonical state representations; it does not become canonical authority.

## Current status

- State Authority: canonical mutation authority
- Persistence: storage mechanism
- Physical persistence technology: TBD
- WAL/journal strategy: TBD
- RPO/RTO: TBD
- Backup verification: UNVERIFIED
- Recovery verification: UNVERIFIED
- Hardware/storage facts: REQUIRES VERIFICATION
- Autonomous qualification: QUEUED

## Qualification rule

Autonomous qualification may inspect and report evidence but cannot authorize production, authorize physical persistence implementation, redefine State Authority, or silently change MH-14.
