# Merge and Routing Governance Audit — Wave 369 — 2026-10-22

## Scope and immutable baseline

- Repository: `VlDMlNSh/mediahub-os`
- `main` at audit start: `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`
- Related merged PRs inspected: #421, #432, #433, #437, #443, #450, #452, #455, and #79.
- Remediation PR: https://github.com/VlDMlNSh/mediahub-os/pull/458
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Findings

### 1. Sequential Gemini controller fixes — retain; do not individually revert

- PR #421 temporarily converted the child workflows to reusable `workflow_call` jobs.
- PR #432 subsequently restored the approved GitHub API dispatch/monitoring route and signed child authorization.
- PR #433 fixed Python syntax in HMAC contract tests.
- PR #437 added/fixed executable child authorization contract coverage.
- PR #443 expanded controller probe trigger-path coverage.
- PR #455 changed `confirm` to a boolean matching the GitHub UI (`true/false`).

These changes are sequential corrections, not evidence that all should be reverted. The current controller on `main` was read back at blob SHA `28874450099e70b0f9d276600e6452c1b8e1b1a6`; it checks `inputs.confirm == true` and binds `MEDIAHUB_GITHUB_TOKEN` and `MEDIAHUB_DISPATCH_HMAC_KEY` inside the controller. Runtime governance/qualification remains separate from source-level implementation.

### 2. Host-identity documentation — retain

- PR #450 corrected Alamo identity to `Voktors-Mini.Dlink`.
- PR #452 reconciled the global host label to Mac mini 2018 and corrected local-executor evidence.

No defect was identified in these documentation-only corrections during this bounded pass.

### 3. PR #79 introduced an unapproved provider routing surface — remediation opened

PR #79 merged at `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2` and added a generic router with OpenAI API, Anthropic API, Gemini API, and OpenRouter routes, plus direct-provider smoke workflows. This conflicts with the canonical Bootstrap contract:
- Gemini Agents 1–3 must use only `.github/workflows/gemini-batch-dispatch-controller.yml` through GitHub Actions/GitHub API/HMAC.
- SentinelX/physical hosts are not Gemini transport.
- Claude/Ollama is a separate local-only Alamo lane; Anthropic API is not an allowed substitute.
- No unapproved or paid provider fallback is allowed.

Remediation is in PR #458: replace the router with a policy-only, fail-closed contract; remove four direct-provider smoke workflows; update the verifier and tests to assert controller-only Gemini and local-only Claude/Ollama.

### 4. Post-merge workflow failures

On merge SHA `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`:
- OpenAI smoke workflow run #39786707954: `failure`, API reported zero jobs.
- Gemini smoke workflow run #39786706844: `failure`, API reported zero jobs.

Because the run API returned no jobs/log evidence, the precise cause is **NOT VERIFIED**. These failures must not be described as provider/model failures without job-level evidence. PR #458 removes these direct routes under the governing policy rather than attempting to repair them as alternate execution paths.

### 5. Historical Issue #301 comments corrected in place

The following owner-authored comments were edited to append explicit governance corrections while preserving historical run IDs and original evidence:
- https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6247849978 — withdraws the statement that Gemini dispatch required SentinelX recovery.
- https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6247960136 — marks the historical SentinelX dispatch route nonconforming.
- https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6247987862 — marks the historical SentinelX re-dispatch route nonconforming.
- https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6283650112 — clarifies that historical runs described as SentinelX/GitHub CLI are not proof of approved transport or acceptance.

Historical status comments stating `NOT RUN` were not deleted: they were time-scoped statements and are not errors solely because later runs occurred. No comment was deleted because preserving audit IDs and original execution evidence is safer than erasing history; the incorrect routing instruction is now explicitly superseded in each affected comment.

## Exact-head verification

- PR #458 head at report creation: `92624857fdff7039e32a047c22941ccacf3da52c` (will advance when this report commit is added).
- Provider-contract verification run #39788538190 passed on the previous PR head `92624857fdff7039e32a047c22941ccacf3da52c`.
- AI Factory verification run #39788538158 and Astra/cloud checks were still running/queued at the time of this report. After this report commit, rerun/inspect all checks at the new exact head.
- PR #458 remains OPEN / NOT MERGED; independent review and exact-head CI must pass before merge.
- Gemini controller run #39786556843 remained RUNNING; child runs #39786584867 (Agent 1), #39786587768 (Agent 2), and #39786592525 (Agent 3) were not all terminal at last inspection. Do not treat the batch as complete until controller and all children are terminal and outputs/artifact digests are verified.

## Next step

Verify all PR #458 checks at its latest exact head, inspect final controller/child results and artifacts, then review PR #458 independently. After acceptance, update the canonical documentation branch map/checkpoint with this audit and the final verified statuses.

