# MediaHub OS — Worker token authority minimization and GitHub API capability audit (Wave 236)

- Date: 2026-10-20
- Status: **SOURCE-VERIFIED FINDING; MITIGATION PROPOSED IN DRAFT PR; CI NOT YET EVIDENCED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Contour A governance: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Proposed mitigation: https://github.com/VlDMlNSh/mediahub-os/pull/405

## Live state revalidated

- `main` HEAD: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- Baseline 2.0 at `main`: blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; accepted canonical immutable reference.
- Bootstrap on documentation ref: blob `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`.
- Master Development Roadmap on documentation ref: blob `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- Continuation checkpoint on documentation ref: blob `7f6de5b928ad78bc7715b33f1645f5478c724ef5`.
- Canonical map blob remains `2187b4ca50792fe073f0979442c0f73432a2f6f9`; UTF-8 and base64 calls through the connected Contents wrapper both returned empty content. This is a connector read limitation, not proof the file is empty.
- Issue #301 is OPEN (updated `2026-10-20T05:16:07Z`).
- PR #388 remains OPEN/Draft at `815fa4af497a593f321ee692f64f53a12dcad061`.
- PR #404 remains OPEN/Draft at `75ce935bd54003b63086bb990496cee1ddc96d3b`; exact-head Astra Verify run `39371237195` and Cloud Runtime Validation `39371237182` are SUCCESS, but the proposal is design-only.
- PR #405 is OPEN/Draft, base `main` SHA `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`, head `59951fb247a6251b1693d5f0bc807c96480f7424`, 2 commits ahead / 0 behind. At read-back time, the connector returned no PR-triggered workflow runs and combined commit status had no statuses. **No CI pass is claimed for PR #405.**

## Primary source finding

Re-read `.github/workflows/astra-distributed-local-worker.yml` on `main`, blob `f650f2416c19dc75b4a0eeec037661c0c6169910`. It declared repository-level `permissions: contents: write` and all three `actions/checkout@v4` steps used `persist-credentials: true`.

Re-read `ops/qualification/run_distributed_local_worker.py` on `main`, blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`. The worker creates a task branch, runs the builder/test/verifier path, then stages all changes, commits and executes `git push origin HEAD:refs/heads/{branch}`. Task JSON is parsed and shape-checked, but the source does not call the standalone verifier proposed in PR #400. PR #400 itself remains Draft and its verifier is explicitly not an execution admission gate; accepted issuer/capability context and replay/revocation lifecycle remain unresolved.

This is a concrete credential-boundary risk: a self-hosted worker workflow has a write-capable workflow token persisted into Git credentials while worker code directly pushes. This finding does not establish that an exploit occurred or that ambient host credentials are absent.

## Proposed bounded mitigation in PR #405

On branch `work/contour-a-worker-token-minimization-wave236`:
- changed workflow permission to `contents: read`;
- changed all three checkouts to `persist-credentials: false`;
- added regression coverage asserting read-only token permission and no persisted checkout credentials.

Read-back after write:
- Workflow blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`, length 5,679 chars; read-only permission confirmed, 3 checkout steps use `persist-credentials: false`, no `contents: write` or `persist-credentials: true`.
- Test blob `12f25f684f0b37cf6d34d5c905394f9e0664fbf2`, length 4,615 chars; new test `test_worker_workflow_uses_read_only_token_without_persisted_credentials` present.
- PR head is `59951fb247a6251b1693d5f0bc807c96480f7424`.

## Official API research correction

- GitHub Contents API docs state files from 1–100 MB can be read using `raw` or `object` media types; in `object` mode the content field can be empty. Therefore an empty response from this connector does not prove that the map is too large for the API or that a Git LFS migration is needed: https://docs.github.com/en/rest/repos/contents
- GitHub's workflow-dispatch endpoint supports fine-grained PATs and GitHub App installation tokens with repository `Actions: write`; classic PATs require `repo`: https://docs.github.com/en/rest/actions/workflows# create-a-workflow-dispatch-event
- GitHub documents that `workflow_dispatch` and `repository_dispatch` are exceptions to the normal `GITHUB_TOKEN` no-new-workflow-run rule. Thus the blanket assertion that GITHUB_TOKEN cannot dispatch another workflow is incorrect: https://docs.github.com/en/actions/concepts/security/github_token
- Neither API permissions nor token possession automatically overrides branch protection/rulesets. Repository protection state is still UNKNOWN because the previous authorized integration read returned 403 for branch protection; an empty rulesets response alone is not enough to establish all effective protection settings.

## Limits / required next gates

PR #405 is defense in depth only. `contents: read` plus `persist-credentials: false` reduces the workflow-token path but does not prove direct pushes impossible if a self-hosted runner has ambient Git/SSH credentials. The worker's direct push implementation remains in source. The next architectural step is an accepted trusted admission boundary plus artifact-only worker output and a separately authorized publisher; do not wire PR #400's verifier into execution until issuer/key provenance, expected bindings, cancellation, replay, revocation and recovery semantics are accepted.

Do not merge PR #405 until its CI is exposed and green, exact-head read-back remains correct, and independent security review addresses ambient runner credentials. No worker was dispatched, no provider or secret was accessed, and no merge/deployment/qualification occurred. Contour A remains NOT_PROVEN / BLOCKED; Contour B remains gated.
