# MediaHub OS — Wave 496: Alamo/FCC/Claude Code on Ubuntu Hosted Runner

- Date: 2026-10-31
- Status: **IMPLEMENTATION PROPOSED ON WORKING BRANCH / NOT RUN / NOT QUALIFIED / NOT ACCEPTED**
- Immutable base target SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Working branch: `contour-a/alamo-fcc-claude-hosted-runner-20261031`
- Parent tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Cloud Claude tracker: [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Workflow blob SHA: `5878d6e91f52fb97342437078e5aa86d5252435a`
- Contract-test blob SHA: `69fe8e45993b98e67ec7e588ae0543611ce2e902`
- Report blob SHA before final reconciliation: `f71329367df64c6287c59bde5d37e0f699e17ca3`
- Canonical documentation branch remains `docs/mediahub-chat-tree-map-20261012`; this branch is non-canonical and unaccepted.

## Owner direction

The owner explicitly requested that physical-server placement be ignored for this task and that Alamo be placed on an Ubuntu Hosted Runner together with FCC and Claude Code. The runner is ephemeral; all local model data and runtime state are scoped to the job and discarded when the job ends.

## Source reconciliation

The accepted distributed-infrastructure architecture identifies Alamo as the local inference endpoint and states that its runtime/API/model must be discovered and verified. The Jarvis architecture crosswalk explicitly says that the relationship between Alamo and Ollama is unproven. The repository policy router already names a local FCC/Ollama route and `llama3.2:3b`, but it does not prove that Ollama is Alamo.

Accordingly, this bounded implementation creates an **Alamo-role local inference candidate** using pinned Ollama as the backend, while recording `alamo_equivalence=NOT_VERIFIED`. It does not claim to install an independently identified Alamo distribution or qualify Alamo equivalence.

## Proposed workflow

`.github/workflows/mediahub-alamo-fcc-claude-runner.yml`:
- Ubuntu Hosted Runner only; no self-hosted runner or physical host.
- Owner-only workflow_dispatch, explicit confirmation, exact current main SHA.
- Ollama installer checksum verified; Ollama version pinned to 0.40.11.
- Ollama binds to 127.0.0.1 only; model `llama3.2:3b` is downloaded into RUNNER_TEMP.
- FCC source pinned to `Alishahryar1/free-claude-code@3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- Claude Code pinned to 2.1.282.
- FCC proxy bearer auth is enabled; unauthenticated /v1/models must return HTTP 401.
- Claude Code runs through FCC in an empty workspace with plan mode and read-only tool allowlist.
- No provider API key, OpenRouter, Anthropic API credential, or paid fallback is used.
- Runtime provenance and bounded evidence are uploaded; no secrets or server logs are included.

## Resource envelope

The workflow preflights at least 4 vCPU, 8 GiB available RAM and 8 GiB free disk before model installation. This intentionally fails closed if the hosted runner's actual free disk is below the required threshold. A 3B CPU-only local model is a smoke-test target, not a production coding-model performance claim.

## Acceptance criteria

1. PR contract tests pass on exact PR head.
2. Owner dispatch gate passes on exact current main SHA.
3. Ollama runtime and model marker pass.
4. FCC bearer auth passes both positive (HTTP 200) and negative (HTTP 401) checks.
5. Claude Code returns exact local marker through FCC.
6. Evidence includes exact target SHA, runtime versions, route and model metadata, without credentials.
7. Independent review confirms no paid fallback, authority bypass, public listener, or secret leakage.

## Current execution disposition

- Workflow and tests are committed on the working branch. Exact-head PR CI passed at implementation head `f21496049c436aae1855fbe7dca3a9bde3a0a8c0`: Alamo workflow run `41183717447` (job `124486242023`, five contract tests passed; dispatch and runtime jobs skipped by design), Astra Cloud Runtime Validation `41183717449` (job `124486241847`), and Astra Verify `41183717401` (job `124486241820`). The Alamo PR job log confirms `5 passed in 0.04s`. The current report-only commit will receive its own exact-head CI check.
- No GitHub workflow dispatch was made; the available GitHub integration exposes no workflow-dispatch action. PR CI skipped both `dispatch-gate` and `alamo-local-fcc-claude`, so no runner installation or model execution occurred.
- No Ollama model download, FCC runtime start, Claude Code request, provider request, or secret access occurred.
- Code-contract CI: **PASS** at implementation head `f21496049c436aae1855fbe7dca3a9bde3a0a8c0` (see run IDs above). Independent review is still pending.
- Alamo/Ollama equivalence remains NOT VERIFIED.
- No qualification, deployment, or acceptance is claimed.

## Next step

Run PR CI and independent review. After those gates pass, owner-dispatch the local-only workflow from main with `confirm=true` and the exact current main SHA. Inspect run IDs, job statuses, artifact digest, and marker evidence before considering the runner Alamo candidate qualified.
