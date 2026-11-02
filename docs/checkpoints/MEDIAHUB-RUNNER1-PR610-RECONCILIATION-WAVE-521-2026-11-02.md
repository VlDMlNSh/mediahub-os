# MediaHub Runner 1 PR #610 reconciliation — Wave 521

Date: 2026-11-02

## Decision

PR #610 is **NOT A SAFE MERGE CANDIDATE** in its current form. PR #623 already merged the Runner 1 workflow and contract test paths. PR #610's copies of those paths are older, divergent implementations and must not overwrite the current main versions.

## Verified refs

- PR #610 head: `cac44b8a867945d4b544c3e46bd819bc42373f36`; open, unmerged.
- PR #623 head: `504507a4335e353e8adac90d755f002ff476f33b`; merge commit: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`.
- Current main workflow blob: `12b684bbd3d475d64cac7e37bbaf64c65ce40529`.
- Current main contract test blob: `a3cf0c8fffbe5fd049144619d388354b4704b1d8`.
- PR #610 workflow blob: `dd6a577f6c704b0453fcd5b05754d10967f8babb`.
- PR #610 contract test blob: `2cf879635b68008b90af2e1ae0ec831f1b5a65a1`.

## File-by-file disposition

| PR #610 path | Disposition |
|---|---|
| `.github/workflows/mediahub-ollama-fcc-claude-runner.yml` | **SUPERSEDED / DO NOT MERGE**. Main contains the PR #623-integrated version with later owner-gated workflow changes. |
| `tests/test_mediahub_ollama_fcc_runner_contract.py` | **SUPERSEDED / DO NOT MERGE**. Main contains the later contract test version. |
| `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` | **UNIQUE HISTORICAL ARCHITECTURE MATERIAL / REVIEW REQUIRED**. The file is outside the current docs path convention and must be reconciled against current owner-directed two-runner topology before promotion. |
| Wave 365/496/497/498/500 addenda and checkpoint files | **HISTORICAL EVIDENCE / REVIEW REQUIRED**. Preserve provenance; do not bulk-copy old snapshots into current checkpoint. |
| Wave 509 terminology report and new-chat master continuation prompt | **POTENTIALLY USEFUL, BUT NOT AUTOMATICALLY PROMOTABLE**. Their canonical claims must be checked against current Bootstrap, checkpoint and map; preserve only still-valid content. |
| PR #610 checkpoint copy | **STALE SNAPSHOT / DO NOT REPLACE CURRENT CHECKPOINT**. Current canonical checkpoint has later Waves through 520. |
| Wave 510 preflight report | **HISTORICAL EVIDENCE / REVIEW REQUIRED**. Reconcile its claims with merged PR #623 and Wave 520/521 status before indexing. |

The PR #610 description refers to an older head `495d3f8eca33eb3feb52426131fed7d07dc9c372` and historical run IDs. The live PR metadata now reports head `cac44b8a867945d4b544c3e46bd819bc42373f36`; do not reuse the description's old exact-head CI as evidence for the current head.

## Runtime and governance disposition

- PR #623's successful PR-head workflows established contract CI, not live runner operation. Ollama install/inference, FCC service, Claude Code invocation and artifact upload were skipped on the pull_request event.
- PR #610's historical workflow evidence is not transferable to current main or current PR head.
- Do not dispatch the Runner 1 workflow until the current workflow's owner/target-SHA gates, provider route, FCC auth behavior and approved placement contract are verified.
- Gemini agents remain NOT RUN; this reconciliation does not authorize Gemini dispatch or alter the separate Runner 2 co-location requirement.
- No file was merged, cherry-picked, or copied from PR #610. No runtime, provider, secret, or infrastructure action was performed.

## Next bounded step

1. Independently review the unique architecture and Wave 509/510 documentary content against current Bootstrap, map, checkpoint, Master Roadmap, Issues #296/#496/#301, and the owner-directed two-runner proposal.
2. Retain only current, source-backed facts; leave historical reports intact as provenance.
3. Keep PR #610 open until an explicit close/retire decision is made after its unique material is dispositioned.
4. Continue implementation work on Runner 2 only through the approved controller governance and same-host isolation design; no dispatch until its admission gates pass.

## References

- [PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)
- [PR #623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [PR #625](https://github.com/VlDMlNSh/mediahub-os/pull/625)
- [PR #626](https://github.com/VlDMlNSh/mediahub-os/pull/626)
- [PR #627 — Wave 520 evidence PR](https://github.com/VlDMlNSh/mediahub-os/pull/627)
- [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296)
- [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
