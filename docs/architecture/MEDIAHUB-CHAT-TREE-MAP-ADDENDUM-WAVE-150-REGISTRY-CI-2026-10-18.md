# Project map addendum — Wave 150 registry/CI supplement — 2026-10-18

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Detailed report: [Wave 150 CI and registry reconciliation](../checkpoints/MEDIAHUB-CONTOUR-A-CI-AND-REGISTRY-RECONCILIATION-WAVE-150-2026-10-18.md)
- Continuation checkpoint: [Wave 150 registry/CI checkpoint](../checkpoints/MEDIAHUB-CONTINUATION-CHECKPOINT-ADDENDUM-WAVE-150-REGISTRY-CI-2026-10-18.md)
- Master plan supplement: [Wave 149 Contour A roadmap addendum](../checkpoints/MEDIAHUB-CONTOUR-A-MASTER-ROADMAP-ADDENDUM-WAVE-149-2026-10-18.md)
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #358: https://github.com/VlDMlNSh/mediahub-os/pull/358

## Evidence
PR #358's exact head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5` has successful Astra Verify run 39117896120; job logs show 429 unit tests and all seven worker-run correlation tests passed.

## Registry reconciliation
The agent catalog, provider-selection schema, qualification provider/model ordering and proposed cloud-agent authorization-record schema are distinct artifacts. Inspect readers/writers and authority before modifying them. No duplicate registry should be created. Provider free-tier claims remain unverified and all unadmitted routes stay BLOCKED.

## Status
PR #358 remains Draft/unmerged; Issue #301 remains open. A0 issuer/ingress, R-06, target manifest, schema negative fixtures and controlled dispatch evidence remain open. Contour A is not qualified/deployed/accepted; Contour B remains blocked.
