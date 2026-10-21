# Wave 331 — Gemini and Voktors-Mini readiness recheck

Date: 2026-10-21  
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)  
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

## Disposition

**Gemini Agents 1–3: NOT RUN. Claude-fcc-Ollama: NOT RUN. agent-browser: NOT RUN. Qualification and acceptance: NOT QUALIFIED / NOT ACCEPTED.** This pass did not dispatch workflows, post a trigger comment, read secret values, change the SentinelX allowlist, install packages, or use a physical server for Gemini.

## Immutable refs and governance

- Live `main` HEAD: `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`.
- Controller blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
- Child workflow blobs on `main`: Agent 1 `155a02159912ca371e6f826c51325ca269857aad`; Agent 2 `fff1820a6b97d379b23674f36bd62227b7d4dec2`; Agent 3 `781df56e8aa7c75ba453c08378611857862b2e44`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the governance issue.
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437) remains OPEN/DRAFT. Formal reviews are empty; combined status for its known head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14` returns no statuses.
- GitHub branch metadata says `main.protected=false`; required checks are disabled. The current controller source does not itself enforce the external branch-protection, formal-review and exact-head-CI gates required by project policy. Therefore the controller remains blocked by governance, even though its dispatch implementation is present.

## Controller run evidence

- [Run #39670089739](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39670089739): completed; all four jobs `skipped`; no artifacts.
  - `Require explicit batch admission flag`: job `119465372314`, skipped.
  - `Non-launching no-secret caller-context probe`: job `119465373355`, skipped.
  - `dispatch_and_monitor`: job `119465373553`, skipped.
  - `assert_probe_context`: job `119465374013`, skipped.
- [Run #39669477347](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669477347): all four jobs skipped; no artifacts.
- [Run #39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179): all four jobs skipped; no artifacts.

The skipped runs do not establish that the batch variable is false, and do not represent child workflow execution. No Gemini child run IDs, dispatch correlation IDs, provider calls or output artifact digests exist for this pass.

## GitHub transport and secret-name contract

The controller's GitHub-hosted workflow source contains signed GitHub API dispatch and exact-run monitoring for the three child workflows. This supports cloud/server independence at design level; runtime failover has not been tested.

The controller and all three child workflows reference exact ASCII secret name `MEDIAHUB_DISPATCH_HMAC_KEY`. Repository source search found no use of `MEDIAHUB_DISPATCH_NMAC_KEY`. The controller reads `secrets.MEDIAHUB_GITHUB_TOKEN` and `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`. The connected GitHub integration does not provide Actions secret/variable metadata listing in this session; effective existence, value format and minimum token scope remain NOT VERIFIED. No values were read. Never paste a secret value into an issue or report.

The controller's non-launching context probe is available through `workflow_dispatch` mode `probe`, but the available GitHub connector exposes no authorized workflow-dispatch operation. Posting the exact `/next` comment to Issue #301 is a potentially launching action when the batch flag is true, so it was intentionally not used while gates remain open.

## Voktors-Mini / SentinelX

- SentinelX identifies the host as `Voktors-Mini.Dlink`, ID `host_5f7264034bdf0b51`, macOS 14.7.4 ARM64, agent `0.22.0`; ping and a full capability response succeeded during this pass.
- The full allowlist contains 95 command prefixes but does not include `agent-browser`, `claude`, `ollama`, `fcc-claude`, or `npx`. A bounded read-only PATH check reported all five as `NOT_FOUND_IN_PATH`.
- Subsequent SentinelX calls again hit `duplicate_session`/timeouts; service status also could not be verified because the configured `sudo launchctl` path requires an interactive password.
- The agent-browser skill stub was read. Its mandatory next step is `agent-browser skills get core` on the host. That command was **not** run because the binary is absent and not allowlisted. No browser session or UI test was run.
- Claude-fcc-Ollama was not invoked. The free-only route and paid-fallback exclusion are not qualified. No allowlist edits or package installs were attempted.

## Next bounded step

1. In GitHub Actions settings, ensure the controller's exact secret identifier `MEDIAHUB_DISPATCH_HMAC_KEY` is configured and verify the token's minimum effective scope without disclosing values. Do not enable the batch flag as a workaround for governance.
2. Close formal review, exact-head CI and effective branch-governance gates. Add or verify a trusted-main, no-secret probe path before permitting batch dispatch.
3. Restore stable SentinelX command-channel access. Install/qualify the required browser and local LLM tools only through an explicitly approved, narrow command policy; then run `agent-browser skills get core` before any browser operation and verify a no-paid-fallback Claude route.

## Acceptance ledger

| Workstream | Status | Evidence |
|---|---|---|
| Gemini Agent 1 | NOT RUN | No child run ID/artifact |
| Gemini Agent 2 | NOT RUN | No child run ID/artifact |
| Gemini Agent 3 | NOT RUN | No child run ID/artifact |
| GitHub-only cloud architecture | Source-reviewed, runtime NOT VERIFIED | Controller/child workflow blobs above |
| SentinelX host identity | VERIFIED | Stable host ID and macOS state |
| Claude-fcc-Ollama | NOT RUN | Required executable/route not available |
| agent-browser | NOT RUN | Binary absent from PATH and not allowlisted |
| Failover / E2E / qualification | NOT RUN | No runtime test evidence |
| Overall readiness | NOT QUALIFIED / NOT ACCEPTED | Governance and execution gates open |
