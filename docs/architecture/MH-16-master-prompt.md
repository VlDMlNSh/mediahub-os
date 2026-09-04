# MH-16 Master Prompt / Reverse Master Prompt

## Purpose

This file is the machine-readable governance handoff between the MH-16 architecture record and the dedicated development workspace.

## Master Prompt — sent from architecture to development

Implement nothing in the architecture chat. Treat `docs/architecture/MH-16-installer-recovery-update-architecture.md` as the current MH-16 architectural source of truth.

Preserve these invariants:

1. Installer != State Authority.
2. Update Coordinator != State Authority.
3. Migration Engine != State Authority.
4. Recovery Manager != State Authority.
5. Persistence != State Authority.
6. Signature != authorization.
7. Signed artifact != automatically trusted artifact.
8. Recovery privilege != runtime privilege.
9. Offline != trusted by default.
10. Boot success != operational readiness.
11. Unknown lifecycle state != success.
12. Rollback MUST obey security floor.
13. Migration MUST be explicit/versioned.
14. Restore MUST use approved State Authority semantics.
15. Existing data MUST NOT be silently destroyed.
16. AI/plugin/UI MUST NOT bypass lifecycle security boundaries.
17. Concrete technologies remain CANDIDATE until ADR + evidence + governance acceptance.

Development may implement only after the applicable architecture/governance gate authorizes it. Never silently change canonical architecture through implementation.

## Required development evidence

For each implementation slice return:

- exact commit SHA;
- changed paths;
- contract/ADR implemented;
- tests executed and exact results;
- security review status;
- hardware/platform assumptions;
- unresolved unknowns;
- deviations from MH-16;
- rollback/recovery evidence;
- whether implementation is COMPLETE, PARTIAL, BLOCKED or REQUIRES ARCHITECTURE DECISION.

Do not label work VERIFIED, ACCEPTED, FROZEN or PRODUCTION READY without corresponding evidence and governance decision.

## Reverse Master Prompt — returned from development to architecture

Provide a concise evidence package:

`Implementation Slice → Commit → Contract/ADR → Tests → Security Evidence → Platform Evidence → Failure/Recovery Evidence → Deviations → Open Questions → Gate Request`

If implementation reveals a conflict with MH-16, stop at the boundary and return `ARCHITECTURE_CONFLICT / REQUIRES_DECISION`; do not resolve the conflict by silently changing architecture in the development workspace.

## Architecture-chat hygiene

MH-01…MH-23 architecture chats are canonical architecture/governance records. They must not become implementation workspaces. No long debugging sessions, code-development threads, uncontrolled experiments or implementation drift are permitted here.

GitHub is the durable external record. Chat context is not the sole source of truth.

## Current MH-16 state

PROPOSED / GOVERNANCE ACCEPTANCE PENDING / NOT FROZEN / IMPLEMENTATION NOT AUTHORIZED.

Current repository sync commit for this handoff: 33ea4980a1fee60cf43609d5d060412fa0782301.
