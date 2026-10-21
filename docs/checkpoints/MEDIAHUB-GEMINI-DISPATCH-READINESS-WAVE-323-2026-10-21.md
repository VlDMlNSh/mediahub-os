# Wave 323 — Gemini GitHub transport launch readiness and independent browser evidence (2026-10-21)

## Disposition

**CONTROLLER SOURCE PRESENT / THREE CLOUD WORKFLOWS ISOLATED FROM PHYSICAL HOSTS / NO AGENT DISPATCH / CONTOUR A NOT QUALIFIED.**

This pass prioritized the user's request to achieve three real Gemini cloud-agent runs, but did not bypass existing governance and admission gates. The controller's recent issue-comment runs were all skipped. Run #39650408656 came from a comment on PR #436, while the later runs #39663039781 and #39663132307 came from owner comments on Issue #301 whose bodies were Wave 322/323 report text, not the exact `/next` trigger. No Gemini child run was launched by this pass.

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Main HEAD: `79196054d84b1197cea1447dd1db5ad075302834`
- Documentation branch before this report: `5e8efb549ab71a7f283ec9d5f7d642ee98a72d29`

## Immutable source evidence

- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: blob `9453403bba899a2400ee3fb874d32badd034c704`.
- Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: blob `155a02159912ca371e6f826c51325ca269857aad`.
- Agent 2 `.github/workflows/gemini-agent-2.yml`: blob `fff1820a6b97d379b23674f36bd62227b7d4dec2`.
- Agent 3 `.github/workflows/gemini-agent-3.yml`: blob `781df56e8aa7c75ba453c08378611857862b2e44`.
- Transport contract test: blob `01ddae5e1d7fd0e49ffa651da9655a5a5ad7a8d5`.
- Child HMAC runtime contract test: blob `64d55eb2a78dd1ea015dae80a838dc44ad592f7e`.

## Cloud-host isolation finding

The controller performs the child workflow dispatches through GitHub's Actions API and passes one immutable full target SHA to three fixed child workflows. Each child workflow declares GitHub-hosted `ubuntu-latest` runners, checks the signed envelope, checks out the exact target SHA, and maps only its own provider credential to its model step:

- Agent 1: `GEMINI_API_KEY`.
- Agent 2: `GEMINI_API_KEY_2`.
- Agent 3: `GEMINI_API_KEY_3`.

The reviewed controller/child workflow source contains no dependency on Voktors-Mini, Alamo, SentinelX, agent-browser, or Claude Code. The physical host and local executor were not used as Gemini transport, dispatch proxy, or fallback. This is a source-level isolation finding, not evidence of a successful live agent run.

## Live Actions evidence

- [Main Astra Verify run #39649841150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649841150): `SUCCESS` on main HEAD `79196054d84b1197cea1447dd1db5ad075302834`.
- [Controller run #39650408656](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39650408656): `SKIPPED`; its source comment was on PR #436, all four jobs were skipped, and no artifacts were produced. Later [run #39663039781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39663039781) and [run #39663132307](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39663132307) were also `SKIPPED`: their owner comments were on Issue #301 but contained Wave 322/323 report text rather than the exact `/next` body.
- The GitHub Actions browser page for run #39650408656 identified its source comment as [PR #436 comment #6323130946](https://github.com/VlDMlNSh/mediahub-os/pull/436#issuecomment-6323130946). The controller requires an exact `/next` comment by the owner on Issue #301 or an explicit trusted `workflow_dispatch` with `mode=agents` and `confirm=yes`. A PR comment does not satisfy that trigger.
- PR #437 remains Draft/open/unmerged at head `01629874e8b4a10da68a0574ec77ecdfceeda8b9`. Prior checks on earlier head `7f491729bab024a72dc20f5d7a3e107a4393ba3b` must not be attributed to the latest head. No exact-head CI/check-run result or formal submitted review was found for latest head `01629874e8b4a10da68a0574ec77ecdfceeda8b9` (the commit checks endpoint returned zero check runs).
- No controller run with a successful `dispatch_and_monitor` job was found in the examined recent run list.

## Executor status for this pass

| Executor | Status | Evidence |
|---|---|---|
| Controller | `SKIPPED` | Run #39650408656; source comment was on PR #436 |
| Gemini Agent 1 | `NOT RUN` | No child run ID; no dispatch accepted |
| Gemini Agent 2 | `NOT RUN` | No child run ID; no dispatch accepted |
| Gemini Agent 3 | `NOT RUN` | No child run ID; no dispatch accepted |
| Claude Code on Voktors-Mini/Alamo | `NOT RUN` | No qualified free-only route established |
| agent-browser on Voktors-Mini | `USED — READ ONLY` | Opened the public Actions run page and captured an accessibility snapshot; no login, settings change, or dispatch action |
| Shared target SHA for a Gemini batch | `NOT ASSIGNED` | No batch was admitted |
| Agent artifacts / digests | `NONE` | No child runs |

## Voktors-Mini and browser evidence

- SentinelX identified the only active host as `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, agent `0.22.0`; capabilities summary reports exec/help/read/search/script-run support and an explicit policy summary.
- Desktop Commander identified device `e264f341-2e21-4dfc-9f97-9b95cd08bcd3`. `agent-browser skills get core` was read on this device. `agent-browser doctor --offline --quick` passed with 8 checks, 0 warnings and 0 failures; Chrome for Testing is installed.
- A read-only browser inspection of run #39650408656 confirmed the PR #436 source comment and that `Require explicit batch admission flag` and `dispatch_and_monitor` were skipped. The browser showed GitHub signed out; no repository settings or credentials were accessed.
- Local OmniRoute reports `configExists: false`; `fcc` and `freellmapi` commands were not found in PATH. No Claude session was started and no paid or alternative route was attempted.

## Remaining fail-closed admission gates

1. Independent security review tied to the current exact main/controller and child workflow blobs, covering HMAC canonicalization, replay/cross-workflow rejection, dispatch ambiguity, partial failure, least privilege, logs and artifacts.
2. Verify effective `MEDIAHUB_GITHUB_TOKEN` scope and the presence/separation of required secrets using approved non-disclosing controls. Secret values were not read.
3. Verify `MEDIAHUB_GEMINI_BATCH_ENABLED` variable metadata. This pass could not read Actions settings metadata through the available read-only GitHub connector.
4. Obtain authoritative branch-protection/ruleset evidence; the connected integration cannot read the branch-protection endpoint (403). Do not equate this with no protection configured.
5. Complete the trusted-main no-secret caller-context probe and confirm the current PR #437 exact-head CI status.
6. Keep the canonical A0 issuer/capability, task-scope, target-manifest, schema and evidence gates from Issue #301 open until supported by their own evidence.

## Decision and next step

Do not trigger a real batch until the listed controller admission gates are verified. Once they pass, use only the controller's GitHub API/GitHub Actions transport. Dispatch Agent 1, Agent 2 and Agent 3 with the same immutable target SHA, then record the controller run ID, each child run/job ID, conclusions, report/artifact digests, exact-head CI, and independent review. Voktors-Mini and Claude Code must remain outside the Gemini transport path.

No secrets were read or printed. No Gemini dispatch, provider/model call, merge, deployment, qualification, or acceptance occurred in this pass.
