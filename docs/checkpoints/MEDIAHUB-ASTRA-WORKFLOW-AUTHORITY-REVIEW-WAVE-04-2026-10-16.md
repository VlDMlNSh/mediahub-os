# MediaHub OS — Astra Workflow Authority Review, Wave 04

- Date: 2026-10-16
- Repository: `VlDMlNSh/mediahub-os`
- Reviewed source ref: `main`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD snapshot: `b45324009ac3aa65322a702c28069b12190bc4b8`
- Status: **SOURCE-ONLY SECURITY REVIEW / FINDINGS REQUIRE TRIAGE / NO WORKFLOW CHANGES**
- Scope: workflow triggers, actor/issuer gates, GITHUB_TOKEN permissions, untrusted inputs, reusable-workflow secret transfer, target binding, credential lifetime, self-hosted execution, evidence paths.

## 1. Executive assessment

The two controller workflows create a high-authority execution path from GitHub events to self-hosted runners and, through reusable workflows, to provider credentials and node-specific HMAC keys. The strongest source-level concern is the supervisor's `workflow_dispatch` trigger combined with implicit event-ref checkout, broad inherited secrets, and no visible default-branch guard. A dispatch run selected on a non-default ref may execute the workflow/code from that ref on privileged self-hosted runners. The source should fail closed to an immutable, approved main commit before any secret-bearing or self-hosted job starts.

The issue-comment control workflow has a separate authorization gap: it authorizes by broad GitHub `author_association` categories alone, while workflow-level token permissions grant `contents: write`, `issues: write`, and `actions: write` to its single job. It also parses node/executor options that later fail against hard-coded execution values.

This is a static source assessment. No workflow was dispatched, no runner or host was inspected, and no provider/model was invoked.

## 2. Source identity and evidence

| Source ID | Source | Blob SHA | Reviewed facts |
|---|---|---|---|
| AST-WF-01 | `.github/workflows/astra-chat-control.yml@main` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | `issue_comment.created`; one self-hosted control job; OWNER/MEMBER/COLLABORATOR association gate; workflow-wide contents/issues/actions write; command parser and dispatch/worker branches |
| AST-WF-02 | `.github/workflows/astra-autonomous-supervisor.yml@main` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | main push path filter, manual dispatch, ten-minute schedule; workflow-wide contents read/actions write; HMAC signing, three reusable workflows, provider secrets inheritance, privileged supervisor job |
| AST-WF-03 | `.github/workflows/astra-distributed-verification.yml@main` | `648f56badd2b919b822b4fe4b61f285cca99ed93` | three node jobs and aggregate job; all three node HMAC secrets are passed into reusable workflow and aggregate environment |
| AST-WF-04 | `.github/workflows/astra-provider-qualification.yml@main` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | provider runner; explicit environment mapping of numerous provider API keys and Cloudflare tokens; checkout disables persisted credentials |
| AST-WF-05 | `.github/workflows/astra-local-claude-qualification.yml@main` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | reusable local-qualification workflow; contents-read scope; checkout disables persisted credentials |
| AST-CODE-01 | `astra_github_agent.py@main` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | HMAC verification and freshness checks; fetches main and node refs; can publish to node branch in normal mode; supervisor sets deferred publication |
| AST-CODE-02 | `ops/control/sign_command.py@main` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | node-specific HMAC signing and command signature generation |

Line anchors for direct source inspection:
- Chat control: [lines 7–31](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L7-L31), [lines 33–48](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L33-L48), [lines 60–72](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L60-L72), [lines 74–123](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-chat-control.yml#L74-L123).
- Supervisor triggers/permissions: [lines 5–37](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml#L5-L37).
- Supervisor command signing and dispatch: [lines 39–119](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml#L39-L119).
- Supervisor privileged job and credential persistence: [lines 121–222](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-autonomous-supervisor.yml#L121-L222).
- Reusable distributed workflow: [source](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-distributed-verification.yml).
- Provider workflow secret environment: [lines 30–76](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-provider-qualification.yml#L30-L76).
- Controller HMAC verifier and publisher: [source](https://github.com/VlDMlNSh/mediahub-os/blob/main/astra_github_agent.py).
- Command signer: [source](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/control/sign_command.py).

## 3. Per-job authority matrix

| Workflow/job | Trigger / trust input | Token or secret authority | Execution target | Assessment |
|---|---|---|---|---|
| Chat control / `control` | Issue comment; body is transferred via environment; author association must be OWNER, MEMBER, or COLLABORATOR | `contents: write`, `issues: write`, `actions: write` at workflow scope | Self-hosted Linux `mediahub-control`; status checks identify `mh-dev-01`; worker branch targets `mh-dev-02` | **HIGH**: broad issuer category gate and all write scopes apply to every step; no per-job permission reduction |
| Supervisor / `prepare-command` | main push, manual dispatch, or ten-minute schedule | `ASTRA_NODE_HMAC_KEY_MH_DEV_01` in signing step; caller workflow token scope includes `actions: write` | Self-hosted `mediahub-control`; checks host/user as `mh-dev-01` / `mediahub-runner` | **CRITICAL REVIEW**: no visible `github.ref == refs/heads/main` guard; default checkout ref follows event SHA; command signer and workflow source can therefore be ref-dependent |
| Supervisor / `distributed-verification` | Depends on prepared command | Passes all three node HMAC keys to reusable workflow | Three self-hosted node targets plus aggregate controller | **HIGH**: signing keys cross a broad reusable-workflow boundary; aggregate receives all node keys |
| Supervisor / `local-claude-qualification` | Depends on prepared command | No explicit secret map in caller | Self-hosted provider-labeled runner | **MEDIUM**: target/ref and caller trust still need main-ref fencing; reusable source reviewed statically |
| Supervisor / `provider-qualification` | Depends on prepared command | `secrets: inherit`; callee maps numerous provider keys/tokens into job environment | Self-hosted `mediahub-provider` runner | **CRITICAL REVIEW**: broad secret inheritance; no visible main-ref guard at caller boundary; code from selected ref may run in secret-bearing job |
| Supervisor / `supervise` | Runs after qualification jobs succeed | `GITHUB_TOKEN` exposed as `GH_TOKEN`; node-01 HMAC key; checkout `persist-credentials: true`; workflow scope includes `actions: write` | Self-hosted `mediahub-control`; executes `astra_github_agent.py` | **HIGH**: persisted credential lifetime and write-scope justification need narrowing; source inspection found no direct Actions API call in the controller file, while it does use Git fetch and has a normal-mode node-branch push path; supervisor defers result publication |
| Distributed verification / node jobs and aggregate | Called by supervisor with command ID and target SHA | Node-specific keys in each node job; aggregate receives all three | Self-hosted node runners and controller aggregate | **HIGH**: limit each key to the narrowest step and verify that aggregate needs signing secrets rather than only verification material |
| Provider qualification / `qualify` | Called workflow inputs `command_id`, `target_sha` | Numerous API keys and provider tokens mapped into job environment | Self-hosted provider runner; checkout sets `persist-credentials: false` | **HIGH**: expected provider access exists, but ref fencing, per-provider isolation, and minimal secret scope require evidence |

## 4. Findings

### ASTRA-04-01 — Privileged manual dispatch lacks a visible main-ref fence

**Severity:** Critical review priority; exploitability depends on repository write permissions and GitHub workflow dispatch behavior.

The supervisor permits `workflow_dispatch` alongside main push and scheduled triggers. Its `prepare-command` checkout omits an explicit ref, and the command's `target_sha` is populated from `GITHUB_SHA`. The workflow then passes that target to reusable workflows that check out the selected SHA. No explicit default-branch assertion appears before the HMAC key is used, the command is signed, or secret-bearing jobs start.

**Risk:** a writer able to dispatch against a non-default ref may select a ref containing changed workflow or program code and cause privileged self-hosted execution with node HMAC keys and provider secrets.

**Recommended control:** remove manual dispatch if operationally unnecessary; otherwise gate every privileged job on the approved default branch and resolve a single immutable main SHA before secret access. Verify that the workflow definition and every executable source path match that approved SHA.

### ASTRA-04-02 — Chat-control author association is a coarse authorization gate

**Severity:** High.

The control accepts OWNER, MEMBER, and COLLABORATOR associations. The check does not establish an explicit actor allowlist, command-specific capability, independent approval, or cryptographic authorization of the requested operation. The command comment can trigger `run-gold`, which dispatches the autonomous supervisor, or `run-worker`, which executes a local worker.

**Recommended control:** map stable GitHub actor IDs or an approved team to named capabilities; require separate approval for high-impact operations; bind actor, command ID, operation, target SHA and expiry in signed command evidence; add replay/idempotency checks.

### ASTRA-04-03 — Workflow-wide write permissions exceed demonstrated step needs

**Severity:** High.

Chat control declares `contents: write`, `issues: write`, and `actions: write` at workflow scope. Its steps include checkout, parsing, host checks, task validation, worker execution, artifact upload and issue-comment reporting. The source does not document a least-privilege rationale for each write permission. Supervisor similarly declares `actions: write` at workflow scope and exports the token as `GH_TOKEN`; the inspected controller source contains no direct GitHub Actions API operation, while git network operations are present.

**Recommended control:** set explicit per-job permissions; use `issues: write` only for the reporting job and `actions: write` only for the dispatch step if required; justify `contents: write` against the actual worker publication path. Preserve read-only permission elsewhere.

### ASTRA-04-04 — Reusable provider workflow inherits the caller's full secret set

**Severity:** Critical review priority.

The supervisor uses `secrets: inherit` for provider qualification. The called workflow maps numerous model-provider API keys and Cloudflare tokens into its job environment. This creates a broad secret-bearing execution context on a self-hosted provider runner.

**Recommended control:** enumerate only the specific required secret names at the caller boundary, separate provider families into distinct jobs/environments, and keep secrets limited to the exact step that needs them. Combine this with immutable-ref fencing and environment approval rules.

### ASTRA-04-05 — HMAC key concentration increases node impersonation blast radius

**Severity:** High.

The supervisor passes three node HMAC keys to distributed verification; the aggregate job receives all three keys. The controller uses node-specific HMAC verification, and the signer can create signatures for a key it possesses.

**Recommended control:** confirm whether the aggregate must possess signing-capable secrets. Prefer a verification design that separates signing authority from aggregation, while preserving existing accepted contracts until a governed design change is approved.

### ASTRA-04-06 — Credential persistence is enabled in the privileged supervisor job

**Severity:** High.

The supervisor's `supervise` job uses `actions/checkout@v4` with `persist-credentials: true` and also exports `GITHUB_TOKEN` as `GH_TOKEN`. The token remains available to later steps and Git configuration for the job duration. The job executes the controller and performs Git fetches.

**Recommended control:** use `persist-credentials: false` where possible; inject a short-lived, least-privilege token only into the exact network step that requires it; avoid simultaneous token exposure through environment and Git configuration.

### ASTRA-04-07 — Chat-control parser accepts combinations that its execution step rejects

**Severity:** Medium / reliability.

The parser accepts `codex|claude` and `mh-dev-02|Voktors-Mac-mini.local`. The worker execution step hard-codes `ASTRA_NODE_ID=mh-dev-02`, `ASTRA_EXECUTOR=codex`, and asserts both target values. Requests for Claude or the alternate node can pass initial parsing and task validation, then fail closed at execution.

**Recommended control:** define one canonical capability/target registry and validate against the actual executor path before dispatch. Remove stale target aliases only after the owner-approved topology contract confirms their status.

### ASTRA-04-08 — Scheduled execution is an autonomous side-effect trigger

**Severity:** High operational-risk review.

The supervisor runs every ten minutes and can also start on matching main pushes and manual dispatch. The workflow reaches provider qualification and self-hosted controller execution. This may consume provider quota and exercise local infrastructure without a contemporaneous user command.

**Recommended control:** tie recurring execution to an explicitly accepted operating policy, bounded schedule, concurrency/duplication controls and cost limits; retain an immediate pause mechanism and auditable run provenance.

### ASTRA-04-09 — Third-party actions use major-version tags rather than immutable commit pins

**Severity:** Medium / supply-chain hardening.

Reviewed controller workflows use tags such as `actions/checkout@v4`, `actions/github-script@v7`, and `actions/upload-artifact@v4`. Major-version tags can move over time.

**Recommended control:** pin external actions to full commit SHAs and record the corresponding verified upstream release/version; automate controlled update review.

### ASTRA-04-10 — Target SHA checks are present but branch identity and actor provenance remain separate

**Severity:** High.

Chat control checks that the checked-out `main` HEAD equals the supplied target SHA before worker validation. Supervisor signs a command whose target SHA comes from the workflow event. HMAC validation and target-SHA binding are useful controls, but they do not independently prove that the originating ref was approved or that the actor had capability for the requested operation.

**Recommended control:** validate approved ref, actor/capability, operation, target SHA, issue/run ID, expiry and one-time command ID as a single authorization decision.

## 5. Evidence and confidence

- Exact source blob SHAs are recorded above; relevant line anchors link directly to the live `main` source.
- This is a source-only review. No YAML parser, test suite, qualification, workflow dispatch, API provider call, secret access, host/runtime inspection, runner inspection, or infrastructure change occurred.
- Findings are based on source structure and stated assumptions. In particular, the manual-dispatch branch-selection risk requires owner-visible validation of allowed dispatch refs and branch protection before final severity can be confirmed.
- Repository branch-protection and secret-scanning evidence remains UNKNOWN from the prior Wave 02 evidence ledger.
- No workflow or normative contract was modified.

## 6. Prioritized remediation sequence

1. **P0:** add a fail-closed default-branch and immutable-target fence before any secret-bearing/self-hosted job; validate manual dispatch ref policy.
2. **P0:** replace coarse association-only authorization with actor/capability policy and replay-safe command binding for chat control.
3. **P0:** remove `secrets: inherit` from provider qualification in favor of an explicit secret allowlist; isolate provider keys by job/environment.
4. **P1:** narrow workflow/job token permissions and review whether supervisor `actions: write` is required; disable checkout credential persistence where feasible.
5. **P1:** reduce HMAC key distribution to minimum required jobs/steps and review signing-versus-verification authority.
6. **P1:** resolve chat-control executor/target contradictions against the approved node registry.
7. **P2:** pin third-party actions to full commit SHAs and document recurring schedule authority/cost guardrails.

## 7. Next bounded step

Create a proposed patch plan, without applying it, for P0 controls in this order: supervisor main-ref fence, explicit provider-secret allowlist, per-job token permissions, chat-control actor/capability binding, and target/executor consistency. The next implementation pass must remain subject to the project's separate authorization rules; this report itself changes documentation only.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
