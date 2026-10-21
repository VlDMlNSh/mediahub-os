# Wave 332 — Gemini and Voktors execution recheck

Date: 2026-10-21 (UTC 20:35–20:45 approx.)
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

## Immutable refs and live state
- Latest independently fetched `main` commit referenced by live report/checkpoint: `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b` (docs-only removal of a misplaced Wave 329 addendum).
- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: blob `9453403bba899a2400ee3fb874d32badd034c704`.
- Child workflow blobs on `main`: Agent 1 `155a02159912ca371e6f826c51325ca269857aad`; Agent 2 `fff1820a6b97d379b23674f36bd62227b7d4dec2`; Agent 3 `781df56e8aa7c75ba453c08378611857862b2e44`.
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437) is still OPEN/DRAFT/UNMERGED at head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`, base `1a6e5a16ef9950b72dda04abd69a27f019922489`. Exact-head workflow-run/status wrappers return empty arrays; formal reviews: 0.
- Repository branch metadata in the latest recorded checks says `main.protected=false`, required checks disabled, no rulesets. No evidence in this pass closes that governance gap.

## Gemini transport / actual execution
- All three child workflows use GitHub-hosted `ubuntu-latest` runners and check out the same `inputs.target_sha`; source-level architecture therefore does not depend on Voktors-Mini or any other physical server. This is design evidence only; failover remains untested.
- Controller run [#39670089739](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39670089739) has all four jobs `skipped`; direct job evidence confirms it. Artifact listing is empty. Run [#39669477347](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669477347) was also all-skipped; earlier [#39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) likewise skipped all jobs. These are not Gemini executions.
- Gemini Agent 1: **NOT RUN**. Agent 2: **NOT RUN**. Agent 3: **NOT RUN**. No child run IDs, dispatch IDs, provider calls, task reports or artifact digests exist in this pass.
- No controller trigger was posted. The available GitHub connector has no authorized workflow-dispatch operation, and posting exact `/next` on Issue #301 is a launch-capable event when the batch flag is true. Given open governance, exact-head CI/review, secret metadata and trusted-main probe gates, this would be premature.

## Credential contract
- Controller and all three child workflows reference exact ASCII `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`, `secrets.MEDIAHUB_GITHUB_TOKEN`, and `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`.
- User-supplied `MEDIAHUB_DISPATCH_NMAC_KEY` is not the same identifier as `MEDIAHUB_DISPATCH_HMAC_KEY`. This is a confirmed source/config-name mismatch, not proof that the expected secret is absent. The connected GitHub API does not expose Actions secret/variable metadata in this session. No secret values were read or emitted; effective presence, scope and token permissions remain **NOT VERIFIED**.

## Voktors-Mini.Dlink / SentinelX
- Host inventory identifies `Voktors-Mini.Dlink`, ID `host_5f7264034bdf0b51`, macOS 14.7.4, ARM64, SentinelX 0.22.0. The active-host limit is one and this host occupies it.
- Fresh full capabilities returned successfully once: 95 allowed command prefixes, 2 readable/writable paths, 1 configured service and 9 playbooks. The allowlist excludes `agent-browser`, `claude`, `fcc-claude`, `ollama`, and `npx` as command prefixes.
- A subsequent ping, direct read of `/Users/voktor/sentinelx/config.yaml`, and an allowed read-only `which/ls` inventory command failed with `agent_disconnected / duplicate_session`. Earlier Wave 331 evidence found `/opt/homebrew/bin/ollama` and the agent-browser binary on disk, but neither has been qualified for execution under the current allowlist; `claude`/FCC were not found on PATH. Latest notifications pool says no running jobs.
- Claude-fcc-Ollama: **NOT RUN / NOT VERIFIED**. agent-browser: **NOT RUN**; mandatory `agent-browser skills get core` did not complete and no browser session was opened. No allowlist change, installation, paid fallback, local task dispatch, or service mutation was performed.

## Gate decision and next step
**Overall: BLOCKED / NOT QUALIFIED / NOT ACCEPTED.**

1. Verify the exact Actions secret identifier `MEDIAHUB_DISPATCH_HMAC_KEY` and effective scope for `MEDIAHUB_GITHUB_TOKEN`, without exposing values; verify `MEDIAHUB_GEMINI_BATCH_ENABLED` at the controller's effective scope.
2. Restore effective branch protection/required checks, obtain independent security review and exact-head CI for PR #437, and establish the trusted-main no-secret probe. Keep the batch flag from being used as a substitute for governance.
3. After gates pass, use only the GitHub-hosted controller for three child workflows on one immutable SHA; record all run IDs, terminal statuses, reports and artifact digests.
4. Separately obtain explicit owner authorization for the narrowly scoped SentinelX allowlist entries needed for the existing browser binary and verified local runtime; restore stable SentinelX command execution, then run `agent-browser skills get core` before browser operations and qualify the free-only Claude/FCC route.

No controller launch, child dispatch, local execution, failover test, qualification, merge, deployment or acceptance is claimed.
