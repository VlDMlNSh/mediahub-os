# MediaHub OS — GitHub Actions Entry-Point and Gemini Provenance Review, Wave 77

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **READ-ONLY SOURCE/EVIDENCE REVIEW / NO DISPATCH / R-06 AND A0 GATES OPEN**
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Working branch: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`

## 1. Ref and PR state at start

- PR #333: https://github.com/VlDMlNSh/mediahub-os/pull/333
- State: open, Draft, unmerged.
- Working HEAD: `dda8dea1e43287f9b62c03d0eadca52127798345`.
- Canonical base SHA: `a0c432273914fa5c4bd9e756736f9c9b72b41a77`.
- Comparison: ahead 34 / behind 0; 18 changed files.
- Canonical map Contents API returned empty `content` despite blob SHA `0141454f29b3da6c84488f9464be30812e0b13a3`. Treat this as a response limitation, not an empty document. Canonical bootstrap was re-read at blob `aa77ba6850f3b3cf51fcf5fae491b2998a276321`; Master Roadmap blob `22fc463f40fb9b8360b5bd15cbfe1edc97844699`; Wave 76 report blob `1bc5dcf73914488873ad75867ed2da84192b4bf8`; Issue #301 was re-read.

## 2. Workflow inventory and branch divergence

Read GitHub's public Contents API for `.github/workflows` on the canonical documentation ref and `main`:
- Canonical documentation ref: 28 workflow files.
- Working documentation branch: 28 workflow files.
- Current `main`: 35 workflow files.
- The seven files observed on `main` but absent from the documentation branch include:
  - `gemini-agent-2.yml`
  - `gemini-agent-3.yml`
  - `gemini-autonomous-engineering.yml`
  - `gemini-readonly-audit-retry.yml`
  - `gemini-readonly-audit.yml`
  - `mediahub-one-time-storage-migration.yml`
  - `mediahub-runner-migration-smoke.yml`

This difference is not permission to merge/rebase. It is evidence that the canonical documentation ref is not a substitute for checking executable workflow definitions on the exact target ref. All source conclusions below name the specific ref and blob.

## 3. Directly verified Gemini historical run

GitHub Actions API metadata for run `38952885501`:
- URL: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38952885501
- Workflow: `Gemini Read-only Architecture Audit (Retry)`
- Workflow file: `.github/workflows/gemini-readonly-audit-retry.yml`
- Event: `workflow_dispatch`
- Branch: `main`
- Source commit: `b45324009ac3aa65322a702c28069b12190bc4b8`
- Status/conclusion: `completed / success`
- Job: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38952885501/job/117148417231
- Job ID: `117148417231`; all five substantive steps observed succeeded, including “Call Gemini API with bounded retry” and “Upload audit result”.
- Artifact ID: `12069128185`, name `gemini-readonly-audit-retry-38952885501`, reported size 5,306 bytes, digest `sha256:a31c7a5036f003e6918c4c6a3ab0ad7f82c8c6c5fb10afde77f8a39d0d8b4d7d`, expiry `2026-10-30T19:10:27Z`.
- Run started `2026-10-16T19:10:02Z` and completed `2026-10-16T19:10:31Z`.

This proves one historical read-only Gemini workflow invocation succeeded. It does not prove current quota/provider availability, repeatability, full artifact provenance, or qualification of the wider agent fabric.

## 4. Source identity and execution boundary of Gemini workflows

On `main`:
- [gemini-readonly-audit-retry.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-readonly-audit-retry.yml) — blob `96fcc9ed4e45659d0118f0b9f3593a0c736200f0`.
- [gemini-readonly-audit.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-readonly-audit.yml) — blob `0d10efdda251f2ceca43175981c919102303572b`.

Static review confirms both have `workflow_dispatch`, declare `contents: read` at workflow/job scope, use `persist-credentials: false` for checkout, obtain the provider key through Actions secrets, and upload advisory output as an artifact. No dispatch was made during this pass.

Existing source-level gaps documented in Wave 09 remain relevant: caller-selected mutable `context_ref`, third-party actions referenced by version tags rather than full commit SHAs, caller-controlled context paths beyond a task-specific allowlist, free-form model selection in the retry workflow, and absence of a complete source/context/action/model/policy/output evidence manifest. The current source refs have not been patched or qualified by this pass.

## 5. Existing repository launch routes — distinguish read-only from privileged

### A. Gemini read-only audit

The Gemini workflow supports manual `workflow_dispatch` and runs on GitHub-hosted `ubuntu-latest`, with read-only repository permissions at source level. This is the narrowest candidate for a later authorized cloud-only verification, after immutable SHA/path/model/provenance hardening and explicit permission for a provider call.

The currently exposed GitHub connector catalog has no dedicated action for starting an arbitrary new workflow run. Read-only GitHub API fetches work; no authenticated browser session is verified. Therefore this session did not establish a usable direct dispatch route from the chat.

### B. Astra chat-control

[astra-chat-control.yml](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/.github/workflows/astra-chat-control.yml) — blob `51b17ec2410032772f9baa1de4afedb6b000f3c4`.

Static source review finds:
- Trigger: `issue_comment` on created comments.
- Permissions: `contents: write`, `issues: write`, `actions: write`.
- Runner: `[self-hosted, linux, x64, mediahub-control]`.
- Commands include `/astra status`, `/astra run-worker`, `/astra run-gold`.
- `run-gold` calls GitHub's `createWorkflowDispatch` for `astra-autonomous-supervisor.yml`.
- `run-worker` routes execution to a self-hosted worker and references an FCC environment file.

This is not a harmless test endpoint and is not the requested GitHub-hosted-only route. Do not post commands or trigger this workflow as a substitute for a read-only hosted worker.

### C. Astra autonomous supervisor

[astra-autonomous-supervisor.yml](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/.github/workflows/astra-autonomous-supervisor.yml) — blob `a0209a2d01122354d19e95d2f362a6ecfa3d6186`.

Static source review finds `workflow_dispatch`, a 10-minute schedule, `actions: write`, self-hosted control runners, HMAC secret injection, nested distributed verification and provider qualification workflows, local Claude qualification, and autonomous queue execution. This workflow has material execution/provider/credential side effects. It is explicitly out of scope for this pass.

### D. Runner admission probe

[astra-runner-admission-probe.yml](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/.github/workflows/astra-runner-admission-probe.yml) — blob `acbc9e6b73f5854b87fb053c538f675ed8bcae5f`.

Although it exposes `workflow_dispatch`, it targets `[self-hosted, linux, x64, mediahub-control]` and asserts host `mh-dev-01` and user `mediahub-runner`. It is a host identity probe, not a GitHub-hosted runner verification, and was not dispatched.

## 6. Safe disposition and next step

- No workflow was dispatched or rerun.
- No provider/model was called; no secrets or credentials were read.
- No tests, installation, qualification, runtime/host inspection, infrastructure changes, merge, rebase, cherry-pick or deployment occurred.
- Issue #301 remains governing and explicitly keeps provider calls, dispatch, tests/qualification and promotion behind separate authority gates.
- Recommended next bounded pass: source-only compare of `gemini-readonly-audit-retry.yml` against the Wave 09 findings, prepare an exact immutable-SHA/path/model/evidence-manifest patch proposal, and inspect current Actions run metadata without triggering anything. Implementing the patch or dispatching a provider call requires separate authorization.
- Candidate status: **HISTORICAL GEMINI RUN VERIFIED / CURRENT REPEATABILITY UNVERIFIED / FABRIC NOT QUALIFIED / NO DISPATCH**.
