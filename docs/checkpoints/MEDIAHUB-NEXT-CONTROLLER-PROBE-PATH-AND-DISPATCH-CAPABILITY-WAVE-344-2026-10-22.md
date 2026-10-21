# Wave 344 — controller probe-path and dispatch-capability audit (2026-10-22)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
Controller: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml

## Immutable source snapshot

- `refs/heads/main` SHA: `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`.
- Controller blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
- Bootstrap blob SHA: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical map blob SHA: `38d8903bc640fd37009f0fc19a11ea7869840dbc`; the Contents endpoint returned empty text, while the blob endpoint previously returned 1,165,629 characters.
- Canonical checkpoint blob SHA: `3bb3ea262c2a30c8f780d36eb61902833325fb29`; working checkpoint on `docs/mediahub-next-wave340-20261022` has continued past the canonical branch.
- Master Roadmap blob SHA: `cea169e55e02903ab9871d51ff643b3da7ef0e8c`.

## New controller finding

The controller explicitly defines `workflow_dispatch` inputs with `mode=probe` as the default and `mode=agents` plus `confirm=yes` for the launch path. The probe path uses the local reusable context-probe workflow with empty permissions; its assertion reports that transport/HMAC/provider secrets are not mapped and Gemini is not reachable in probe mode. The agent path is separate and maps `MEDIAHUB_GITHUB_TOKEN` and `MEDIAHUB_DISPATCH_HMAC_KEY` only inside the dispatch job.

The controller source also contains an owner-only Issue #301 comment trigger requiring the exact literal body `/next`. Prior run #39678989141 was skipped because comment #6326943789 was a report announcement rather than the exact trigger. No controller or Gemini child execution has been demonstrated.

**Capability limitation:** the available GitHub connector actions expose read operations, file/PR operations and rerun-failed-job operations, but no approved `workflow_dispatch` action. Posting the owner `/next` comment would select the agent-launch path, not the non-launching probe, so it is deliberately not used as a substitute. No probe was dispatched.

## Current gates

- PR #437 HEAD `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`, open and not mergeable; prior exact-head suite `107496095390` was queued with zero check runs and no formal review.
- PR #441 HEAD `9f40b90c3106662cfcc337c48f29e4794fa713dc`, open and not mergeable; prior exact-head suite `107524023551` was queued with zero check runs and no formal review.
- PR #442 is a draft documentation PR; latest observed head before this report was `c3d5230e002837263c930126cce14899de137052`, open and unmerged. The earlier exact-head suite for `5da1dea0b57e70c695ee8b40f28e1d2a96d548d2` does not certify the newer head.
- Main Astra Verify run `39669337754` succeeded. Branch protection API returned 403; an empty ruleset list is inconclusive.
- SentinelX identifies `Voktors-Mini.Dlink` as `host_5f7264034bdf0b51` (macOS 14.7.4 ARM64, agent 0.22.0); ping, state and capabilities responded. A bounded read-only `which agent-browser` request timed out, so CLI presence and browser evidence remain unverified.
- Gemini Agents 1–3: NOT RUN; no controller run ID, child run IDs, target manifest, or artifact digests.
- Claude-FCC/Ollama local execution: NOT RUN / NOT VERIFIED. No secret values read. No trigger, dispatch, host modification, merge, deployment, qualification, or acceptance occurred.

## Disposition and next step

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

Next: provide an authorized route to run the controller's non-launching `workflow_dispatch` probe (or an authorized operator can run it with `mode=probe` and an explicit immutable target SHA); then resolve exact-head CI, obtain independent controller/HMAC security review, and verify governance and effective token scope before any agent dispatch. Separately, re-establish a bounded read-only SentinelX session to inspect agent-browser core instructions and the free/no-paid-fallback Claude-FCC/Ollama route. Do not substitute a literal `/next` trigger for the probe.
