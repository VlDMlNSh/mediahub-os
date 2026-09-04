# MH-14 — Persistence Architecture Package

Status: **ARCHITECTURE WORK IN PROGRESS**

This directory is the durable GitHub record for the MH-14 architecture track.

## Primary documents

- `MH-14-persistence-architecture.md` — canonical architecture baseline
- `MH-14-master-prompt.md` — interface from architecture to development chats
- `MH-14-reverse-master-prompt.md` — interface from development chats back to architecture

## Governance

MH-14 is an architecture-only track. Development, debugging and prolonged implementation discussion belong in the separate development chat.

Physical persistence implementation remains **NOT AUTHORIZED** until the explicit implementation gate is passed.

## Core invariant

> Persistence stores canonical state; it does not become canonical authority.

## Current status

- State Authority: canonical mutation authority
- Persistence: storage mechanism
- Physical persistence technology: TBD
- WAL/journal strategy: TBD
- RPO/RTO: TBD
- Backup verification: UNVERIFIED
- Recovery verification: UNVERIFIED
- Hardware/storage facts: REQUIRES VERIFICATION
