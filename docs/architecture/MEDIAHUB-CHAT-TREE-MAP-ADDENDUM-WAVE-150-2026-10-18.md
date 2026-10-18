# Project map addendum — Wave 150 — 2026-10-18

## New evidence and current next step
- Wave 150 report: [CI and provider-registry reconciliation](../checkpoints/MEDIAHUB-CONTOUR-A-CI-AND-REGISTRY-RECONCILIATION-WAVE-150-2026-10-18.md).
- Wave 150 checkpoint: [continuation checkpoint](../checkpoints/MEDIAHUB-CONTINUATION-CHECKPOINT-ADDENDUM-WAVE-150-2026-10-18.md).
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md.
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301.
- PR #358: https://github.com/VlDMlNSh/mediahub-os/pull/358.

## Evidence update
PR #358's exact current-at-checkpoint head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5` has successful `Astra Verify` run 39117896120; job logs show 429 unit tests and all seven worker-run correlation tests passed. This is CI evidence, not full worker qualification.

## Registry authority
Existing registry artifacts have different roles: agent catalogue (`profiles/agent-registry.json`), provider-selection schema (`schemas/ai/ai-provider-registry.schema.json`), qualification model order (`ops/qualification/provider_model_registry.json`), and proposed cloud-agent registry record schema (Wave 16 v0.2). Do not create a parallel registry or equate `enabled`/free-tier labels with issuer authorization or account quota. The next pass must inspect consumers and writers and produce a field-level authority crosswalk.

## Gates
Issue #301 remains open. PR #358 remains Draft/unmerged. A0 issuer/ingress, R-06, target manifest, schema negative fixtures and controlled worker-dispatch evidence remain open. No provider routes are admitted from candidate-list documentation alone. Contour A is not qualified/deployed/accepted; Contour B remains blocked.
