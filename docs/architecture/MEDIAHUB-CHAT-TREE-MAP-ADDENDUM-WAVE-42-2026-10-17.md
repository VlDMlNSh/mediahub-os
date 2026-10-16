# MediaHub Chat Tree Map — Wave 42 Addendum

- Date: 2026-10-17
- Status: CPRG HOSTING ALTERNATIVES COMPARED / HOST UNSELECTED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Primary report: [CPRG Hosting Alternatives and Reuse-First Readiness, Wave 42](../checkpoints/MEDIAHUB-CPRG-HOSTING-ALTERNATIVES-AND-REUSE-READINESS-WAVE-42-2026-10-17.md)

## Navigation update

The repository already contains the Central Protected Registration Gateway (CPRG) architecture, threat model, trust/identity contract and bootstrap/revocation/recovery protocol. Wave 42 extends those sources and explicitly avoids creating a competing registration design.

## Current direction

- CPRG remains one logical registration authority with a replaceable, dedicated physical host.
- A small self-owned Linux server is the first hosting candidate to evaluate due to potentially lower recurring rental costs when suitable hardware already exists.
- A European VPS remains a first-class alternative.
- iPhone-based manual enrollment is temporary.
- Existing GitHub Actions Secrets remain the default credential boundary where applicable. SOPS+age and OpenBao are compared only if a documented need warrants another secret-management authority.
- Browser automation, provider enrollment, server implementation and hosting are unqualified/unselected.

## Next dependency

Use current workflow definitions and exact secret-name references to prepare a provider-by-provider readiness matrix from official public policies. Keep provider calls, credentials, tests, qualification and infrastructure changes gated.

- Detailed report: [Wave 42](../checkpoints/MEDIAHUB-CPRG-HOSTING-ALTERNATIVES-AND-REUSE-READINESS-WAVE-42-2026-10-17.md)
