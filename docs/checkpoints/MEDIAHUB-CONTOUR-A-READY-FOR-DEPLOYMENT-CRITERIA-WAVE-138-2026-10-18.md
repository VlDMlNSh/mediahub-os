# Contour A Ready-for-Deployment Criteria — Wave 138

Date: 2026-10-18. Canonical ref: `docs/mediahub-chat-tree-map-20261012`.

Status: owner clarification recorded; criteria only; no qualification claim.

## Owner clarification
Contour A development is considered closed when all project-selected components have been tested and selected, integrated, and the complete system is ready to deploy using those components. Report this state as `READY_FOR_DEPLOYMENT`. Keep `DEPLOYED` and `INDEPENDENTLY_ACCEPTED` as separate states. Contour B remains gated until deployment and independent acceptance, per the Master Roadmap.

## Mandatory readiness gates
1. **Component selection:** canonical component manifest or owner-approved equivalent lists each required component, pinned version/source, purpose, license, dependencies, owner, alternatives, selection rationale, and status. Stable existing components are preferred where suitable. A search miss is not evidence that a manifest does not exist.
2. **Component qualification:** required contract, compatibility, security and negative tests pass; versions/source SHAs, logs and artifact digests are retained. License, maintenance, vulnerability and data-egress reviews are recorded where applicable.
3. **Integrated system:** accepted contracts connect components; actual queue/worker execution is proven (the CAF-Q-001…CAF-Q-015 documentary queue alone is not a scheduler); isolated workspace, immutable provenance, runtime-only credentials, output quarantine, fail-closed policy, bounded retry, cancellation/recovery and backup/restore are tested as required.
4. **Target/deployment package:** approved target topology and runner/workspace/network manifest exist; installation, configuration, migration, upgrade, rollback, recovery and health-check procedures are reproducible; no critical manual decisions remain.
5. **Governance/release evidence:** A0 issuer/ingress/lifecycle and R-06 gates are accepted and tested; schemas have standards validation, negative fixtures and independent review; exact refs, SHAs, run/job IDs and artifact digests are recorded. CI claims are limited to checks actually run.

## Exit rule
Set `READY_FOR_DEPLOYMENT` only when all applicable mandatory gates are PASS with evidence links and exact refs. Missing, stale, conflicting or non-authoritative evidence is BLOCKED. Any non-applicable gate requires a documented rationale and accepted authority. This criteria document does not itself qualify the system.

## Current disposition
Issue #301 remains open. Its current evidence still identifies unresolved A0 issuer/ingress/lifecycle and R-06, target manifest acceptance, schema validation/review, live read-only worker/queue and controlled runtime evidence. Current status remains **NOT READY FOR DEPLOYMENT / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.

## Next action
Locate the canonical component manifest via the canonical map/tree and build a per-component matrix: pinned version, owner, contract, tests, actual evidence, runtime dependency, target fit, security/data route review, status and blocker. Do not infer selection from mentions alone.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
Baseline 2.0: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md
