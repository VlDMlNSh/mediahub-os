# Wave 330 — Gemini dispatch gates and Voktors-Mini executor status

Date: 2026-10-21  
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)  
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

## Disposition

**Gemini Agents 1–3: NOT RUN. Claude-fcc-Ollama: NOT RUN. agent-browser execution: NOT RUN.** No secret values were read, no batch flag was enabled, no controller trigger was created by this pass, and no alternate transport was used. This is a fail-closed evidence pass, not runtime qualification.

## Immutable refs and current state

- `main` HEAD: `79196054d84b1197cea1447dd1db5ad075302834`.
- Controller `.github/workflows/gemini-batch-dispatch-controller.yml` blob: `9453403bba899a2400ee3fb874d32badd034c704`.
- Canonical docs branch HEAD observed during this pass: `1554bfb97d947bb2556c2c5761013fbe2f1a596a` before this report/checkpoint update.
- Governance issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) is OPEN.
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437) remains OPEN/DRAFT; independent formal review and exact-current-head CI are not evidenced in this pass.
- [PR #438](https://github.com/VlDMlNSh/mediahub-os/pull/438) remains OPEN/DRAFT and is documentation-only; it is not an admission approval.

## Controller and configuration findings

Source inspection confirms the controller's intended execution path is GitHub-hosted Actions and GitHub API dispatch/monitoring; the three fixed child workflows are intended to receive one shared immutable target SHA. No physical server is required for Gemini execution by source design.

The controller reads the exact secret name `MEDIAHUB_DISPATCH_HMAC_KEY` (HMAC), as well as `MEDIAHUB_GITHUB_TOKEN`, and reads `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`. The requested/configuration name `MEDIAHUB_DISPATCH_NMAC_KEY` is **not the same name** and will not satisfy the controller's HMAC lookup. The earlier Cyrillic-lookalike spelling `MEDIAHUB_DISPATCH_НМАС_KEY` is also not equivalent. This is a name-level contract finding only; the connected GitHub integration cannot inspect sensitive secret values or establish their effective presence/scope. Do not disclose values in comments, logs or artifacts.

GitHub branch metadata reports `main.protected=false` with no required checks. The integration could not establish a compensating repository ruleset or effective governance protections. This leaves a required admission gate open.

## Controller run evidence

The latest three controller runs inspected were:
- [39667761725](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667761725) — `issue_comment`, completed / `skipped`; jobs #119457216843, #119457217665, #119457218629 and #119457260696 all `skipped`.
- [39667424495](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667424495) — completed / `skipped`; all four jobs `skipped`.
- [39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) — completed / `skipped`; all four jobs `skipped`.

These runs created no Gemini child runs and do not demonstrate model invocation, queue execution or agent output. Controller run [39650408656](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39650408656) was likewise skipped. No child run IDs or artifact digests exist for this pass.

## SentinelX / Voktors-Mini / agent-browser / Claude

- SentinelX inventory lists `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, agent `0.22.0`, as operational in the inventory.
- SentinelX initially returned timeout/`agent_disconnected` (`read_loop_ended`) for capability/state/ping calls. A later ping succeeded (`pong: true`, agent `0.22.0`), but repeated `detail=full` capability requests still timed out/disconnected. Therefore the live command allowlist could not be revalidated; no remote command was executed.
- As allowlist/capability evidence is unavailable, `agent-browser skills get core` was **not** run remotely and no browser command/session was started.
- Claude-fcc-Ollama / FCC was not invoked. No route qualification proves allowed non-paid authentication, upstream terms, cost class, egress, or paid-fallback exclusion.
- No server was used to transport or execute Gemini. Cloud/server independence is supported by workflow source design, but failover has not been dynamically tested.

## Admission gates still open

1. Correct and non-disclosingly verify the exact secret name `MEDIAHUB_DISPATCH_HMAC_KEY`; verify `MEDIAHUB_GITHUB_TOKEN` minimum effective permissions and `MEDIAHUB_GEMINI_BATCH_ENABLED` metadata without revealing values.
2. Obtain independent security review of the exact active controller/child contract and verify exact-head CI.
3. Establish effective governance/protection requirements; current `main` metadata says unprotected.
4. Run the controller's non-launching trusted-main no-secret probe and retain its run evidence.
5. Restore SentinelX command-channel stability and revalidate host ID, capabilities and allowlist before running agent-browser core instructions or Claude.

Do not post an exact `/next` comment on Issue #301 or enable batch admission until these gates pass. No dispatch was attempted because the GitHub integration available in this session provides read/write repository operations but no authorized workflow-dispatch operation, and the issue-comment bridge remains gated.

## Next bounded step

Correct the secret-name mismatch in GitHub Actions settings (without sharing any secret value), retain metadata-only proof of exact name and scope, and obtain independent review plus current-head CI/governance evidence. In parallel, recover SentinelX's command channel, then read the installed agent-browser core instructions and inspect Claude/FCC only after allowlist and non-paid-route requirements can be proven.

## Acceptance status

Implementation evidence: controller source contains the GitHub API dispatch route.  
Runtime dispatch: **NOT RUN**.  
Gemini Agents 1–3: **NOT RUN**.  
Claude-fcc-Ollama: **NOT RUN**.  
agent-browser: **NOT RUN**.  
Qualification / acceptance: **NOT QUALIFIED / NOT ACCEPTED**.
