# Canonical map addendum — Wave 291 (2026-10-20)

- **Report:** [GitHub governance visibility and positive-probe safety audit](../checkpoints/MEDIAHUB-GITHUB-GOVERNANCE-VISIBILITY-AND-POSITIVE-PROBE-SAFETY-WAVE-291-2026-10-20.md).
- [Canonical map](MEDIAHUB-CHAT-TREE-MAP.md); [checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md); [Master Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Rulesets API returned `[]`; classic `main` branch-protection endpoint returned 403 `Resource not accessible by integration`. This does not establish that classic protection is absent. Effective Actions and org policy remain unverified.
- `main` remains `80be45a70732b1d568164571d4273a6397792c3b`; PR #421 is 61 commits ahead, draft/unmerged, with no submitted independent reviews. Its controller has different semantics from main and includes secret-mapped agent calls; do not dispatch it as a probe.
- Safe next design: dedicated default-deny controller probe mode, separate read-only observer, no secrets, no write permissions, and explicit gating that makes model/provider jobs unreachable. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B gated.
