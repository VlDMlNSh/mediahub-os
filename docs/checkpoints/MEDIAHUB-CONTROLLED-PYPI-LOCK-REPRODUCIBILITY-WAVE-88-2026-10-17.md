# MediaHub OS — controlled PyPI lock reproducibility Wave 88

- Date: 2026-10-17
- Work branch: `contour-a-schema-validation-wave81-20261017`
- PR: [#337 — Wave 81: Add pinned cloud-agent schema validation workflow](https://github.com/VlDMlNSh/mediahub-os/pull/337)
- Status: controlled lock regeneration and current-head schema CI verified; PR remains Draft and has no independent review.

## 1. Changes committed

### Lock-generation workflow

- File: [.github/workflows/cloud-agent-lock-generation.yml](https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-wave81-20261017/.github/workflows/cloud-agent-lock-generation.yml)
- Blob SHA: `951631787208740daf7999e71df24beb625b9910`
- Workflow commit containing explicit environment isolation: `0864ec9e396d297d32005cbccf253d60a16162ae`; final command-header update: `35b5d861035dae826b4e24518f18c98faf6e075a`.
- The generator explicitly selects `https://pypi.org/simple`, sets `PIP_CONFIG_FILE=/dev/null`, removes inherited `PIP_NO_INDEX` from the compiler process, and passes `--no-config` to pip-tools.
- `CUSTOM_COMPILE_COMMAND` now records the actual controlled regeneration command in the lock header, avoiding the misleading earlier `--no-index` header.
- The workflow no longer regenerates merely because the lock file itself changed; input and workflow changes remain the relevant push paths.

### Committed lock

- File: [requirements/cloud-agent-schema-validation.lock](https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-wave81-20261017/requirements/cloud-agent-schema-validation.lock)
- Commit: `9898787e5ef9e5f045a0f644c070165973fd19a6`
- Blob SHA after read-back: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`
- Size: 15,083 bytes; 213 newline-separated records.
- SHA-256 from generator: `f30c923e5bf25777fda85de14fbe1b2cdc33bc57b2a1ff88adc3e2bef5205f29`.
- The committed lock text was reconstructed from the successful generator log, then read back from GitHub and compared byte-for-byte with that log output.

## 2. Reproducibility evidence

Two separate successful generator runs produced the same input and lock SHA-256 values and the same controlled command header:

1. [Run 39046826239](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046826239), head `35b5d861035dae826b4e24518f18c98faf6e075a`.
2. [Run 39046901040](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046901040), head `9898787e5ef9e5f045a0f644c070165973fd19a6`.

Both logs show `Using indexes: https://pypi.org/simple`; both report input SHA-256 `1056b740383d453db32b92c7f24170a952eadf5ffafaaa7875ad58329c313916` and lock SHA-256 `f30c923e5bf25777fda85de14fbe1b2cdc33bc57b2a1ff88adc3e2bef5205f29`.

### Artifact inspection

- Latest artifact: `12106331705`, attached to run `39046901040`.
- Artifact API digest: `sha256:fa5a99df325011844a8998a8f9db848cc691ebd69f2ff55fde4dfe2ba9ece599`.
- Downloaded ZIP size: 6,816 bytes; local ZIP SHA-256 matched the API digest.
- ZIP contains one file, `cloud-agent-schema-validation.lock`, size 15,083 bytes.
- Independently extracted file SHA-256: `f30c923e5bf25777fda85de14fbe1b2cdc33bc57b2a1ff88adc3e2bef5205f29`, matching both generator logs and the committed lock content.
- The ZIP digest and lock-file digest differ because they identify different byte sequences (archive versus extracted file); both were verified against their respective evidence.

## 3. Current-head CI

- Current PR head: `9898787e5ef9e5f045a0f644c070165973fd19a6`.
- Successful schema-validation run: [39046905941](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046905941), job `117437332532`, conclusion `success`.
- The job installed from the lock with `python -m pip install --require-hashes -r requirements/cloud-agent-schema-validation.lock`.
- The log confirms positive fixtures and expected negative cases for all three v0.2 schemas: task envelope, agent registry, and evidence manifest. Nested required-field rejection counts were 37, 25, and 36. Additional-property, enum, date-time, cross-artifact consistency and cross-artifact task-ID mismatch checks passed.
- This is schema/lock CI evidence, not qualification of the full autonomous development environment.

## 4. Current governance state

- PR #337 remains OPEN / DRAFT / unmerged. GitHub currently reports `mergeable=true`; that is not approval to merge.
- No independent review submissions are recorded.
- Comparison against canonical documentation branch `docs/mediahub-chat-tree-map-20261012`: 45 commits ahead / 18 behind; merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open; A0 issuer/verifier, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema review, and bounded read-only worker/queue qualification remain open gates.
- No merge, deployment, provider invocation, credential access, task dispatch, or Contour B work was performed.

## 5. Next bounded step

1. Perform a file-by-file review of PR #337 and request independent review.
2. Reconcile the 45/18 branch divergence only after inspecting all changed files and potential loss/conflicts; rerun CI on any reconciled head.
3. Continue the separate authority/readiness audit of PR #332 against the canonical Baseline 2.0 sources and Issue #301; do not conflate Jarvis, ASTRA A0, and MediaHub Product State Authority.

## Canonical navigation

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap instruction](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Current continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [PR #337](https://github.com/VlDMlNSh/mediahub-os/pull/337)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)


## Current-head revalidation (2026-10-17, 15:54 UTC)

This follow-up supersedes the earlier head/divergence figures above for navigation; it does not rewrite the historical evidence captured by the original pass.

- Current PR #337 head: `7697165ba8c2b0f24bef0ad00fbf34e6483841f0`; current lock-generation workflow blob: `951631787208740daf7999e71df24beb625b9910`; lock blob: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`.
- The workflow now explicitly neutralizes pip environment/configuration and uses `--no-config --index-url=https://pypi.org/simple`; the current lock header reproduces that exact command context. The earlier `--no-index` ambiguity is not present in the current file.
- Current-head schema-validation runs [39047028293](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047028293) and [39047025408](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047025408) both completed successfully. The generator run [39046901040](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046901040) also completed successfully on prior head `9898787e5ef9e5f045a0f644c070165973fd19a6).
- The PR branch is now 47 commits ahead / 18 behind the canonical documentation branch, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- **Integration hazard:** PR #335 (`test/cloud-agent-schema-validation-20261017`, head `44e2bc7c735ad7f70294d66de8e08eb1da612e0d`) and PR #337 both add `.github/workflows/cloud-agent-schema-validation.yml`. Both remain Draft and unmerged. Do not merge these PRs independently or assume their workflow implementations are interchangeable; perform an explicit file-level design comparison and choose one canonical workflow path before integration.
- PR #337 has no independent review submissions at this observation. Issue #301 remains open. CI success here qualifies only the observed schema workflow on the cited commits, not the complete Contour A environment.
