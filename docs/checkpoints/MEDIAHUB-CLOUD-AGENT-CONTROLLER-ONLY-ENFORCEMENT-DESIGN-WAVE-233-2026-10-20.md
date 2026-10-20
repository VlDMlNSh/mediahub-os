# MediaHub OS — controller-only cloud-agent route enforcement design (Wave 233)

Date: 2026-10-20  
Status: **POLICY PERSISTED / TECHNICAL EXCLUSIVITY OPEN / DESIGN PROPOSAL ONLY**

## Objective

Revalidate the sole approved cloud-agent/API launch route, refresh PR/CI/review state, and identify the smallest credible technical enforcement approach without dispatching agents or changing the accepted transport contract silently.

## Read-back evidence

- Binding transport policy on `docs/mediahub-chat-tree-map-20261012`: blob `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap: blob `77368971b90071812f82c384cdd3be813513a5dc`, section 1A explicitly says controller-only.
- Controller on `main`: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob `99e5a87825aeb239568f96ecef004a102ff3e53b`. It exposes a confirmed `workflow_dispatch`, uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST API dispatch/monitoring, and dispatches three child workflow files.
- The three child workflows on `main` still expose `workflow_dispatch`:
  - Agent 1 `gemini-autonomous-engineering.yml`, blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d`.
  - Agent 2 `gemini-agent-2.yml`, blob `259c8c82b8d90a39e1c90e65390e469b241b5581`.
  - Agent 3 `gemini-agent-3.yml`, blob `91b5397001e088dfae2f450ee77c9c23118b5601`.
- PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) remains Draft/unmerged at head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`, 13 commits ahead / 0 behind `main` `80be45a70732b1d568164571d4273a6397792c3b`. Review API returned no submitted reviews.
- Exact-head CI runs both completed successfully: [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) and [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885). This does not qualify the untested failure-path diagnostic behavior or enforce controller-only dispatch.

## Sole approved launch route — binding project rule

**Every cloud-agent/API launch for MediaHub OS must enter through the GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` and its fixed-scope child workflows.** The currently approved controller dispatch/monitoring transport uses repository secret `MEDIAHUB_GITHUB_TOKEN`. Never launch agents directly from SentinelX, a server shell, local CLI, ad-hoc script, unrelated workflow, or alternate transport. Never expose the token to Gemini/model processes or artifacts. No fallback or paid fallback without explicit governance authorization.

This is a policy statement, not proof that alternate paths are technically disabled.

## Technical enforcement finding

The current implementation uses REST `workflow_dispatch` calls to the three children. GitHub's reusable-workflow mechanism instead requires child files to declare `workflow_call` and be invoked as jobs from the caller workflow. Official GitHub documentation describes this distinction and explicit input/secret passing:
- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Workflow syntax: reusable workflow inputs/secrets](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

The current controller cannot keep REST-dispatching child workflows while those same child workflows no longer expose `workflow_dispatch`. Therefore, removing the direct child entry points requires an explicit orchestration redesign, not merely deleting trigger lines.

## Recommended design for a separately reviewed change

1. Keep exactly one externally dispatchable entry point: the controller workflow, with explicit confirmation and fixed task scopes.
2. Convert each child workflow from `workflow_dispatch` to `workflow_call`; invoke each from a separate, statically declared controller job so the three bounded jobs can run independently on GitHub-hosted runners.
3. Pass only the corresponding provider secret to each called workflow (`GEMINI_API_KEY`, `GEMINI_API_KEY_2`, or `GEMINI_API_KEY_3`); do not use `secrets: inherit`. Preserve minimal job permissions, the fail-closed output validation, sanitized diagnostics, immutable action pins, and run/job correlation.
4. Treat the existing `MEDIAHUB_GITHUB_TOKEN` REST-dispatch requirement as a policy-contract conflict that must be explicitly reconciled before implementation. A `workflow_call` redesign no longer needs REST dispatch to start child workflows; do not silently weaken or repurpose the binding policy. Either obtain explicit owner/governance approval to amend the internal dispatch mechanism, or separately prove an enforceable repository-level control that prevents direct child dispatch while retaining the current REST route.
5. Build a focused test plan before editing: actionlint; positive/negative trigger-contract assertions; per-child secret-boundary assertions; exact-head CI; then a separately authorized controlled failure-path artifact test. Do not redispatch Agent 2 or run the controlled failure test as part of this documentation pass.

GitHub documents workflow execution protections for actor/event restrictions, but that source alone does not prove a per-workflow restriction is configured in this repository: [Actions execution protections](https://docs.github.com/en/actions/concepts/about-actions-policies).

## Safety and acceptance status

- No cloud agent dispatched; no workflow manually triggered.
- No secret value read or exposed.
- No code/workflow change, merge, deployment, or qualification performed.
- PR #420 remains Draft/unmerged; independent review and authorized controlled failure-path test remain open.
- Controller-only route is **documented and binding**, but technical exclusivity remains **NOT PROVEN / OPEN**.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains blocked.

## Synchronization links

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map addendum: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governing issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
