# MediaHub OS — Wave 78: Cloud Model Invocation Readiness and Dispatch Boundary

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **MODEL CALL AUTHORIZED BY OWNER / INVOCATION NOT EXECUTED / DISPATCH ACCESS BLOCKED / FABRIC NOT QUALIFIED**
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Working branch: `docs/contour-a-a0-r06-evidence-reconciliation-wave68-20261017`

## 1. Authorization and scope

The user explicitly authorized cloud-model invocation in this /next turn. This authorizes a bounded provider call for the current task; it does not authorize secret disclosure, paid fallback, self-hosted execution, privileged Astra automation, repository merge, deployment, or unrelated infrastructure changes.

The narrow intended execution path is the existing Gemini read-only architecture-audit workflow on GitHub-hosted `ubuntu-latest`, with `contents: read`, runtime-only Actions secret injection, and artifact output.

## 2. Live repository and PR state

- PR #333: open, Draft, unmerged; https://github.com/VlDMlNSh/mediahub-os/pull/333
- Working branch HEAD reported by live PR metadata: `4458751d07e64c44d950591b78ef31681bc9dc37`.
- Canonical documentation branch base SHA: `a0c432273914fa5c4bd9e756736f9c9b72b41a77`.
- Compare: 38 commits ahead, 0 behind; status `ahead`.
- Live `main` HEAD: `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`, commit message `docs: remove misplaced Wave 75 addendum from default branch`, dated `2026-10-17T12:18:15Z`.
- Canonical map path is `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md`; canonical map blob SHA from the latest Contents read remains `0141454f29b3da6c84488f9464be30812e0b13a3`, while its returned content is empty. This is a read/API limitation, not evidence that the file is empty.
- Working checkpoint blob SHA before this update: `dd7b72a92bebf773e03463e198674e10ff8d8c12`.
- Issue #301 was re-read and remains the governing sequence: close A0 issuer/ingress and R-06 gates; accept target manifest; validate schemas; harden Gemini workflow; then execute a controlled authorized dispatch and record run/job/artifact provenance.

## 3. Existing workflow and historical evidence

- Retry workflow on `main`: [.github/workflows/gemini-readonly-audit-retry.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-readonly-audit-retry.yml), blob SHA `96fcc9ed4e45659d0118f0b9f3593a0c736200f0`.
- Non-retry workflow on `main`: [.github/workflows/gemini-readonly-audit.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-readonly-audit.yml), blob SHA `0d10efdda251f2ceca43175981c919102303572b`.
- Historical run `38952885501`: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38952885501 — `completed/success`, source commit `b45324009ac3aa65322a702c28069b12190bc4b8`, job `117148417231`, artifact `12069128185`, digest `sha256:a31c7a5036f003e6918c4c6a3ab0ad7f82c8c6c5fb10afde77f8a39d0d8b4d7d`.
- Historical success establishes only that one prior invocation worked; it does not establish current quota, repeatability, current model availability, or fabric qualification.

## 4. Invocation path check and blocker

The connected GitHub tool catalog exposes read operations for workflow runs/jobs/artifacts and rerun operations, but no operation to create a new arbitrary `workflow_dispatch` run. A rerun action is not an appropriate substitute because it repeats a historical execution with its old inputs/context.

Browser-profile discovery returned two profiles, neither of which lists GitHub among its signed-in sites:
- Default profile ID `prof_bbd411fee04b491c`, signed-in sites empty.
- MediaHub Freebuff profile ID `prof_a273d0d4a13e4ab3`, signed-in sites empty.

No authenticated browser dispatch route is therefore verified. Per browser integration rules, do not attempt authenticated navigation against a profile without confirming sign-in or obtaining permission to establish a session. No model API call, workflow dispatch, rerun, credential access, test, host inspection, or self-hosted workflow was performed in this pass.

## 5. Source-level gaps that must remain visible

Both Gemini workflows use mutable caller-selected `context_ref`; action references use tags rather than full commit SHAs; caller-supplied context paths are not a narrow task-specific allowlist; the retry workflow accepts a free-form model ID; and the workflow does not emit a complete source/context/action/model/policy/output evidence manifest. These are previously observed source gaps, not claims of a new runtime failure.

The safest next execution is not to dispatch the current un-hardened workflow blindly. First either:
1. confirm a browser profile is already signed in to the intended GitHub account and authorize use of that profile to submit one read-only dispatch; or
2. approve a source-only hardening patch on a dedicated branch, then authorize the dispatch separately.

Any invocation should use an immutable source SHA, exact allowlisted context paths, an explicitly approved model ID and no paid fallback, plus an artifact manifest containing source SHA, workflow/action identities, context file digests, model identifier, policy/task digest, response/artifact digest, run/job IDs and timestamp. Do not include secret values in logs, prompt, summary, or artifact.

## 6. Disposition

- Cloud-model invocation: **authorized by user, not executed**.
- Dispatch: **blocked by lack of a dispatch API action and no verified signed-in browser profile**.
- Historical Gemini workflow: **verified once**.
- Current provider/quota repeatability: **unverified**.
- Contour A fabric: **not qualified**; A0 issuer/ingress, R-06 privacy/audit authority, target manifest and schema gates remain open.
- No changes to executable workflows; no dispatch/rerun, secret read, provider call, tests, installation, qualification, host/runtime inspection, infrastructure change, merge, rebase, cherry-pick or deployment.

## 7. Next step

Ask the user whether either existing browser profile is already signed in to the intended GitHub account, or whether they authorize establishing a GitHub browser session. After that access prerequisite is resolved, perform one bounded read-only dispatch only if the workflow source and inputs satisfy the current approved gates; otherwise present the exact hardening patch for separate authorization.
