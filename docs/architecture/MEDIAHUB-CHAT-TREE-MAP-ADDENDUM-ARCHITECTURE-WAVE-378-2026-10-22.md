# Canonical map addendum — Wave 378 owner architecture decisions

- Date: 2026-10-22
- Status: **DOCUMENTATION PROPOSAL / NOT ACCEPTED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical documentation branch at authoring start: `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`

## New architecture record
- [Owner Architecture Decisions and Consolidated Target Design](MEDIAHUB-OWNER-ARCHITECTURE-DECISIONS-AND-TARGET-DESIGN-2026-10-22.md)
- [Wave 378 consolidation report](../checkpoints/MEDIAHUB-ARCHITECTURE-CONSOLIDATION-CHAT-WAVE-378-2026-10-22.md)

## Owner-confirmed choices
- Strict local-first privacy; user media and detailed local logs remain on user-owned nodes unless a task-specific external transfer is explicitly authorized.
- Encrypted backups on user-owned nodes, separated keys, integrity verification and periodic restore tests.
- Staged updates with provenance and compatibility checks, required gates, controlled activation and rollback.

## Cross-domain dependencies
- Authority separation: Jarvis / ASTRA GOLD A0 / GitHub Supervisor / MediaHub Product State Authority.
- Contour A acceptance is a prerequisite to starting Contour B.
- Privacy/egress binds to task issuer, capability, data class, named recipient, expiry and evidence.
- Queue recovery checks lease, prior result, idempotency and executor compatibility before retry.
- Model availability, executor dispatch, CI success, qualification and acceptance remain distinct states.

## Existing work to reconcile
- [PR #485 — user MediaHub compute and compact context state](https://github.com/VlDMlNSh/mediahub-os/pull/485) already records related node-admission and model-loading requirements. This addendum complements it; PR #485 is not treated as accepted.
- [Issue #301 — Contour A cloud-agent fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the governing implementation/qualification issue.
- [Functional Baseline 2.0](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md) remains the accepted functional reference.

This addendum is an index entry, not proof of implementation, CI success, independent review, qualification, deployment or acceptance.
