# MediaHub OS — Wave 505: two Ubuntu runner placement audit

- Date: 2026-10-31
- Status: **VM1 PR CONTRACT PASS / VM1 LIVE RUNTIME NOT RUN / VM2 CO-LOCATION NOT IMPLEMENTED / BOTH RUNNERS NOT QUALIFIED**
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Required placement

Owner clarification requires two isolated Ubuntu Hosted Runner execution environments:
1. VM 1 — Alamo FCC and associated ECC components, Claude Code, and only their dependencies. No Gemini CLI, mini-SWE-agent, Aider, OpenHands SDK or Goose.
2. VM 2 — three independent Gemini CLI roles, mini-SWE-agent, Aider, OpenHands SDK and Goose. Provider authentication is through provider-issued API keys injected at runtime, with separate identity, quota and scope controls.

GitHub-hosted ubuntu-latest jobs are ephemeral, not persistent VMs. A successful Actions job does not establish persistent availability.

## 2. Immutable source snapshot

- main: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- Canonical docs branch before this pass: d9a289b9113f7567711b641a7017eb814d6c259d.
- PR #610 head: 8f59cc25e789796979637aab6edd7e0e98c4f511.
- PR #613 head: 237948e03088c3ea43608b0c284327c552d34f4b.
- Issue #301 remains OPEN.

## 3. VM 1 — PR #610 evidence

PR #610 workflow installs Ollama 0.40.11, local llama3.2:3b, FCC pinned at 3d2ae2306752dbdf504714a5489bcfcf69b2d04a and Claude Code 2.1.282. It also installs Gemini CLI 0.66.0, mini-SWE-agent 2.4.6, Aider 0.86.0, OpenHands SDK 1.59.0 and Goose 1.57.0 in the same job. This is a direct placement mismatch: those five tools belong on VM 2, not VM 1.

Exact PR-head run 41191982864: event pull_request, head SHA 8f59cc25e789796979637aab6edd7e0e98c4f511, terminal SUCCESS.
- Job 124510457300 workflow-contract: SUCCESS; contract test step SUCCESS.
- Job 124510457433 dispatch-gate: SUCCESS in PR no-op mode.
- Job 124510476414 alamo-local-fcc-claude: job SUCCESS, but only the PR no-op marker ran. FCC checkout, capacity checks, Ollama, model download, Claude Code, extra agent toolchain and runtime evidence upload were all SKIPPED.
- Run artifacts: none.
- No model inference, FCC service, Claude Code invocation or agent task was executed.

Therefore PR #610 proves only the PR safety/no-op contract. It does not test or qualify VM 1 runtime.

PR #610 exact Check Runs do not publish the five active required ruleset contexts. Its legacy commit status endpoint is pending with zero statuses. Required-context CI is NOT VERIFIED for merge.

## 4. VM 2 — controller and worker topology

The approved Gemini controller is .github/workflows/gemini-batch-dispatch-controller.yml. Agent mode dispatches three child workflows through GitHub API after admission and signed-payload checks. Each child workflow currently defines its own runs-on: ubuntu-latest job. The current implementation therefore provisions three separate ephemeral runners; it does not co-locate three Gemini CLI processes on one VM 2.

Child workflow sources map provider credentials to GEMINI_API_KEY, GEMINI_API_KEY_2 and GEMINI_API_KEY_3. Source-level names are verified; secret existence, scope, rotation and successful authentication are NOT VERIFIED. No secret values were read.

PR #610 installs the other four tools on VM 1 without provider authentication. They are not deployed on a separate VM 2 or admitted as A0-managed executors.

Required architecture change: if three Gemini roles and the four supporting tools must share one runner, the approved controller/child contract needs a reviewed extension that dispatches one VM-2 worker. That worker must start three independent Gemini CLI instances with distinct role/task envelopes and provider-key scopes, while installing and smoke-testing mini-SWE-agent, Aider, OpenHands SDK and Goose. Direct Gemini invocation outside the approved controller is prohibited.

## 5. Runtime and host availability

SentinelX inventory at audit time:
- Operational host Voktors-Mini.Dlink, host ID host_5f7264034bdf0b51, session sess_4a0767589e21, agent 0.23.30. This is a SentinelX-managed host, not evidence of either GitHub-hosted Ubuntu runner.
- Free plan: one active slot, one occupied, zero available.
- mh-dev-01 and mh-dev-02 are user-disabled.
- No second active SentinelX host and no confirmed server-3 Claude Code target.
- No SentinelX command was executed in this pass.

No persistent VM resource or long-lived runner registration was created.

## 6. Governance and blockers

- Active main ruleset MediaHub-main-autonomous-merge, ID 26108066, requires five exact contexts: Astra Cloud Runtime Validation, AI Factory verification, provider contract verification, Astra Verify, Gemini workflow contract validation (Wave 284).
- PR #613 has all five exact contexts SUCCESS on its current head, but remains OPEN/DRAFT/UNMERGED and has zero formal reviews. Independent review is NOT VERIFIED.
- PR #610 remains on the older base and its exact required contexts are NOT VERIFIED. Its review record is owner-authored COMMENTED, not an independent approval.
- Issue #301 requires A0 issuer/ingress/lease/cancel/recovery and R-06 gates before agent admission and runtime dispatch.
- No controller dispatch, Gemini child run, provider/model call, Claude Code run, secret read, persistent infrastructure change, merge, deployment, qualification or acceptance occurred.

## 7. Disposition and next bounded work

| Work item | State |
|---|---|
| VM 1 PR no-op contract | **PASS** |
| VM 1 live Alamo/FCC/Claude runtime | **NOT RUN** |
| VM 1 placement isolation | **FAIL — extra agent tools co-located** |
| VM 2 single-runner co-location | **NOT IMPLEMENTED** |
| Gemini controller no-secret probe on PR #613 | **PASS; child dispatch SKIPPED** |
| Three Gemini child runtime executions | **NOT RUN** |
| Provider API-key presence/authentication | **NOT VERIFIED** |
| Two hosted runner environments | **NOT CREATED / NOT QUALIFIED** |
| Contour A | **NOT ACCEPTED** |
| Contour B | **GATED** |

Next sequence:
1. Obtain independent review of PR #613; integrate only through the active ruleset.
2. Correct PR #610 so VM 1 contains only Alamo/FCC/ECC/Claude Code and required local inference dependencies; rebase and verify all five exact contexts.
3. Prepare a separate VM-2 worker and controller-contract change for co-located three-role Gemini plus mini-SWE-agent/Aider/OpenHands/Goose. Add behavioral tests for distinct keys, role separation, fail-closed admission, artifact provenance and no paid fallback.
4. Verify secret names/scopes without reading values, then perform separately authorized runtime tests on exact main SHA. Record controller run, child job IDs, artifacts and digests.
5. Keep runtime qualification, acceptance and any persistent infrastructure decision separate.

No live runner was started in this pass. No secrets were read.