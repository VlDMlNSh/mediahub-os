# Master Roadmap Execution Addendum — Wave 42

- Date: 2026-10-17
- Status: HOSTING ALTERNATIVES COMPARED / DESIGN ONLY
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Primary report: [CPRG Hosting Alternatives and Reuse-First Readiness, Wave 42](MEDIAHUB-CPRG-HOSTING-ALTERNATIVES-AND-REUSE-READINESS-WAVE-42-2026-10-17.md)

## Sequence and technical direction

The existing CPRG architecture and security contracts are the source of truth for the protected registration contour. Extend these documents instead of introducing a parallel gateway design.

Evaluate a small self-owned Linux host first because it may minimize recurring rental cost when suitable hardware already exists. Retain a European VPS as a first-class alternative. Compare total cost of ownership, network reachability, supported OS lifecycle, physical/cloud trust, backup/recovery, operator burden, provider eligibility and failure isolation before selecting a host.

Phone enrollment remains temporary. The credential boundary remains GitHub Actions Secrets where applicable unless a documented capability gap justifies comparing an additional secret manager. Existing SOPS+age and OpenBao entries remain candidates, not newly selected services.

## Next bounded step

Build a provider-by-provider readiness matrix from current workflow definitions, exact secret names and official public provider policies. Capture account and server-region eligibility, key scope, free-tier limits/reset behavior, permitted failover, rotation and required evidence. No provider calls or credential use in this step.
