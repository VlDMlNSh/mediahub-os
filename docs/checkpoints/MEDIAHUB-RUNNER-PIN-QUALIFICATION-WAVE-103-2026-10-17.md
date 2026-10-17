# MediaHub OS — runner label stabilization, Wave 103 (2026-10-17)

## Scope
Pin the dependency-lock generation workflow to a deliberate GitHub-hosted runner image before the announced `ubuntu-latest` migration on 2026-10-19. This is a narrow CI-maintenance change; it does not resolve bootstrap package integrity or the Node.js action-runtime deprecation.

## Change
- Workflow: [cloud-agent-lock-generation.yml](https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-consolidation-wave98-20261017/.github/workflows/cloud-agent-lock-generation.yml)
- Candidate branch: `contour-a-schema-validation-consolidation-wave98-20261017`
- Commit: [`9e1a59278dfee164635457ff9cd2ce2145ceafc0`](https://github.com/VlDMlNSh/mediahub-os/commit/9e1a59278dfee164635457ff9cd2ce2145ceafc0)
- Workflow blob SHA after read-back: `0574ac933d8ccfa70e447f203aa3bf775cc2dd63`
- Exact change: `runs-on: ubuntu-latest` → `runs-on: ubuntu-24.04`; no other workflow line changed in this commit.

## Verification
- GitHub commit diff confirms exactly one line replaced.
- Read-back from the candidate branch confirms `runs-on: ubuntu-24.04` and the blob SHA above.
- Workflow history page showed run [#16 for commit `9e1a592`](https://github.com/VlDMlNSh/mediahub-os/actions/workflows/cloud-agent-lock-generation.yml) as **in progress** at the last check. Therefore this change is committed, but its CI qualification is **pending**, not passed.
- Baseline run [#15 / `39053279868`](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053279868) remains successful and had verified byte-for-byte lock reproducibility for its earlier commit; that result does not qualify this runner change.
- PR [#338](https://github.com/VlDMlNSh/mediahub-os/pull/338) remains Draft/open/unmerged. Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open.

## Remaining risks / gates
- Bootstrap tools `pip==24.3.1` and `pip-tools==7.4.1` are version-pinned but are not independently hash-locked; integrity hardening remains open.
- Existing checkout/setup-python/upload-artifact action SHAs produced Node.js 20 deprecation warnings and were forced to Node.js 24 in the prior run. This is not fixed by runner pinning and should be handled as a separate reviewed change.
- No secrets, external model providers, worker dispatch, deployment, merge, or Contour A acceptance were involved.

## Next
1. Recheck run #16 and record its final conclusion; inspect its annotations for remaining runner/action warnings.
2. Then evaluate a non-circular, independently hash-verified bootstrap mechanism for pip and pip-tools. Do not fabricate hashes or trust the generated application lock to authenticate the tools that generate it.
3. Continue the Issue #301 A0/R-06/runner-workspace-network-manifest/review/qualification gates.

Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md). The Contents API returned an empty body for that map during this pass, so this report and its linked addendum are additive and do not replace it.
