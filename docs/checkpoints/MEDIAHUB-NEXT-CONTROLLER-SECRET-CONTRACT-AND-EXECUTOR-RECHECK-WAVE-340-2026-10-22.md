# Wave 340 — Controller secret-name contract and executor channel recheck (2026-10-22)

## Disposition

**BLOCKED / NOT QUALIFIED / NOT ACCEPTED.** No Gemini workflow was dispatched. No child run IDs, jobs, or artifact digests were created by this pass. No local model task or browser automation was run.

## Immutable source and canonical references

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Candidate target SHA from current checkpoint: `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`. A fresh main-ref lookup was not completed because the commit connector requires a known SHA, so do not treat this as a newly confirmed main HEAD.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md — fetch returned blob SHA `38d8903bc640fd37009f0fc19a11ea7869840dbc` but empty content; no map edits made.
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md — blob SHA `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Current continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md — blob SHA `3bb3ea262c2a30c8f780d36eb61902833325fb29`.
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md — blob SHA `cea169e55e02903ab9871d51ff643b3da7ef0e8c`.
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301 remains the governing Contour A tracker.
- Controller on `main`: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml — blob SHA `9453403bba899a2400ee3fb874d32badd034c704`.

## Newly verified controller contract discrepancy

The controller's `dispatch_and_monitor` step injects:
- `GH_API_TOKEN: ${{ secrets.MEDIAHUB_GITHUB_TOKEN }}`
- `HMAC_KEY: ${{ secrets.MEDIAHUB_DISPATCH_HMAC_KEY }}`

The task's named variable is `MEDIAHUB_DISPATCH_NMAC_KEY` (NMAC), whereas the controller requires `MEDIAHUB_DISPATCH_HMAC_KEY` (HMAC). These are different identifiers. This is a **verified naming mismatch between the requested configuration name and controller source**, but actual GitHub secret presence/value cannot be inspected through this read-only pass. The controller fails closed if `HMAC_KEY` is empty, before dispatching any child workflow.

Do not silently alias or rename the secret. The authoritative contract should decide the canonical spelling; then update the controller, tests, and secret references together in a reviewed change if needed. No secret values were read.

Controller safeguards observed in source: explicit `mode=agents` plus `confirm=yes` for manual launch; batch variable `MEDIAHUB_GEMINI_BATCH_ENABLED=true`; main-ref gate; full 40-hex target SHA validation; HMAC-signed child dispatch payloads; unique correlation IDs; run reconciliation and timeout reporting. Source inspection alone does not prove successful execution or security qualification.

## GitHub runtime evidence

- Combined status for PR #437 head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14` returned an empty status list. This is NOT VERIFIED, not PASS.
- Exact-head workflow-run evidence, formal review status, and live workflow dispatch could not be verified with the available connector calls. No dispatch was attempted.
- Gemini Agents 1–3: NOT RUN; controller run ID / child run IDs / job IDs / artifact digests: none for this pass.
- Queue and server-failover test: NOT RUN.

## Voktors-Mini / SentinelX

- Host: `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`; SentinelX `0.22.0`; macOS `14.7.4`; ARM64.
- Fresh SentinelX ping succeeded.
- A bounded read-only command succeeded. `ollama` was found at `/opt/homebrew/bin/ollama`; `agent-browser` and `claude` were not found on the minimal PATH `/usr/bin:/bin:/usr/sbin:/sbin`. This does not establish whether other paths contain them.
- SentinelX capability/help requests timed out after 60 seconds; current full allowlist could not be revalidated. No install, service change, model call, Claude invocation, or browser task was attempted.
- The host is operational but is not a dependency for cloud Gemini execution.

## Execution ledger

| Item | Status | Evidence |
|---|---|---|
| Gemini controller dispatch | NOT RUN | No authorized dispatch operation used |
| Gemini 1 / 2 / 3 | NOT RUN | No child IDs or artifacts |
| Secret-name contract | BLOCKED | Source requires HMAC name; request lists NMAC name |
| Ollama presence | FOUND, not qualified | `/opt/homebrew/bin/ollama` exists; version/model/route not probed |
| Claude-FCC-Ollama | NOT RUN | CLI absent on current PATH; route unverified |
| agent-browser | NOT RUN | CLI absent on current PATH |
| E2E / failover | NOT RUN | No live queue dispatch |

## Next bounded step

1. Resolve the canonical HMAC secret identifier without reading secret values. Keep fail-closed behavior.
2. Obtain exact-head CI and independent security review for the controller and child workflow set.
3. Use the approved GitHub Actions path to run the no-secret probe only, with batch admission false; record run/job IDs and terminal status.
4. Revalidate SentinelX policy/capabilities when its help endpoint responds; then inspect Ollama version and local model inventory read-only, and identify the permitted non-paid Claude/FCC route.
5. Dispatch three Gemini children only after the governance/security gates pass, using one immutable target SHA and recording every run ID and artifact digest.

No tests, merge, deployment, qualification, or acceptance were performed in this pass.
