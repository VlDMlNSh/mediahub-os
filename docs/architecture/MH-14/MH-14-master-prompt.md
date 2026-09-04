# MH-14 MASTER PROMPT — ARCHITECTURE AUTHORITY

Use this prompt from a separate development chat when MH-14 architecture authority is required.

## Role

Treat `docs/architecture/MH-14/` in the MediaHub OS repository as the durable external record of MH-14 architecture. The MH-14 architecture chat is a semantic guardian of this baseline; GitHub is the long-term repository record. Do not assume chat history is the sole source of truth.

## Rules

1. MH-14 is architecture, not an implementation workspace.
2. Do not develop production code, debug implementation, or conduct long implementation discussions in MH-14.
3. State Authority remains the sole canonical mutation authority.
4. Persistence stores/retrieves state representations; it never becomes authority.
5. Persisted state is not automatically canonical.
6. Restore must be explicitly authorized, validated, and mediated by State Authority.
7. Backup is not HA.
8. Physical persistence implementation is NOT AUTHORIZED until separate governance authorization.
9. Do not select a database, filesystem, WAL strategy, cloud backend, or hardware behavior without evidence and the appropriate ADR/governance step.
10. Do not modify frozen P0-03…P0-06 or independently repair the P0-07 governance/API gap.
11. MH-12 security and MH-13 privacy boundaries are mandatory dependencies.
12. If evidence is absent, mark the claim `REQUIRES VERIFICATION` rather than guessing.
13. Any authority-model change requires explicit governance.
14. Development chats may consume MH-14 through this prompt but must not mutate the architecture implicitly.

## Expected development-chat behavior

When a development request touches persistence, first map the request to MH-14 invariants, contracts, constraints, and open decisions. If the request conflicts with MH-14, stop and report the contradiction rather than silently changing the architecture.

If implementation is authorized elsewhere, keep implementation details in the development workspace and return only architecture-impacting findings, proposed ADRs, evidence and contradictions to the architecture track.

## Canonical boundary

```text
Consumer/Input -> Authorization -> Consumer Boundary -> State Authority
-> Canonical Runtime State -> Persistence Contract -> Persistence Implementation
-> Physical Storage
```

Recovery:

```text
Physical Storage -> Validation/Integrity/Schema -> Candidate State
-> State Authority -> Canonical Runtime State
```

## Status

MH-14: `ARCHITECTURE WORK IN PROGRESS`

Physical persistence: `NOT AUTHORIZED`
