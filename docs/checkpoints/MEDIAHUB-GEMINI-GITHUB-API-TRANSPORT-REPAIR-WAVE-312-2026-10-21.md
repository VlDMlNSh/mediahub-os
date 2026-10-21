# MediaHub OS — Gemini GitHub API transport repair, Wave 312

Date: 2026-10-21
Status: **IMPLEMENTED ON PR BRANCH / VALIDATION PARTIAL / NOT MERGED / NO AGENT DISPATCH**

## Owner correction applied

The executor boundary is now stated explicitly:

- Gemini Agents 1–3 must be launched only by the GitHub-hosted controller through GitHub API using `MEDIAHUB_GITHUB_TOKEN`, mapped only into the controller's dispatch/monitoring steps.
- The token is not passed to child workflows, model processes, prompts, logs, summaries, or artifacts.
- Each child workflow receives only its own provider key.
- Server 3 / Alamo is reserved for local Claude Code and the browser agent. It is not Gemini transport or fallback.

## Code proposal

PR: [#431 — Restore token-backed GitHub API transport for three Gemini agents](https://github.com/VlDMlNSh/mediahub-os/pull/431)
Branch: `fix/gemini-github-api-transport-wave-312`
Latest head SHA at final verification: `4764c74f6b3373fdb09117d3bc02576a39668a4f`
Base SHA: `f16e5bae202a78584f273132e7f88c6e25d3142e` (main at PR creation)

Changed files on PR branch:

- `.github/workflows/gemini-batch-dispatch-controller.yml` — blob SHA `21ad3507c15346d25adf0bd6eaedea07c4cbb1ba`
- `.github/workflows/gemini-autonomous-engineering.yml` — blob SHA `b95a77ff2fe5df6740c1344e049a22bce581c403`
- `.github/workflows/gemini-agent-2.yml` — blob SHA `74f4c639ab50a3f9f9f0437d3d448c133f674dfc`
- `.github/workflows/gemini-agent-3.yml` — blob SHA `6714f5b2a73ff9f10e9fa26368ff6475ed2afe92`
- `tests/test_gemini_transport_controller_contract.py` — blob SHA `a501649d8da823a5f4b2dd07dd6129c7bbba3d9d`

Controller behavior proposed:

1. Default `mode=probe` runs a no-secret, no-dispatch probe.
2. Agent dispatch requires both `mode=agents` and explicit `confirm=yes`.
3. The controller resolves `main` to one full commit SHA through the GitHub API and passes that SHA as `base_ref` to all three children.
4. Only the three fixed child workflow paths are dispatched. Pre-dispatch run baselines and bounded polling correlate run IDs; ambiguous/missing/failed runs fail closed.
5. The controller's `MEDIAHUB_GITHUB_TOKEN` is not mapped to child workflows. Children keep pinned checkout/Gemini CLI actions and digest-pinned GitHub MCP container.

## Verification evidence

Latest observed head `5676bf402c807d069d1374a9321b12743fb72854`:

- [Wave 284 workflow contract validation run 39600173823](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892953): **SUCCEEDED**.
- [No-launching caller-context probe run 39600173779](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892994): **SUCCEEDED**; PR context was tested without launching Gemini.
- [Astra Cloud Runtime Validation run 39600173792](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892899): **SUCCEEDED**.
- [Controller workflow PR run 39600173791](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892909): **SUCCEEDED**; no-secret probe succeeded and dispatch job was skipped.
- [Astra Verify run 39599892964](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892964): **RUNNING at last check**; do not treat exact-head full verification as complete until terminal conclusion is rechecked.
- Formal independent PR review: **NOT RECORDED** at last check.
- No Gemini agent was dispatched. No secret value was read or exposed. No merge, deployment, qualification or acceptance occurred.

An earlier intermediate head failed because legacy tests still encoded the merged reusable-workflow architecture. Those tests were updated to the token-backed GitHub API contract; only the newer exact-head runs above are relevant to the current candidate.

## Remaining gates

- Recheck terminal status of Astra Verify at exact head.
- Obtain genuine independent security review of token scope, direct child-workflow triggerability, API run correlation, and child provider-secret isolation.
- Verify effective repository/org governance and required checks, then merge only through normal project protection.
- After merge, verify exact-main CI and a no-secret default probe. Do not use `mode=agents` before all gates pass.
- No agent dispatch has been run by this wave.

## Navigation

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Transport policy: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governance Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
