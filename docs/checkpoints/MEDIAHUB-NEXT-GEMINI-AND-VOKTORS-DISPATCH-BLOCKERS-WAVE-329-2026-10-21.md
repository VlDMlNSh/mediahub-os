# Wave 329 — Gemini dispatch gates and Voktors-Mini runtime recheck

Date: 2026-10-21  
Disposition: **BLOCKED / NOT QUALIFIED**. This pass gathered fresh evidence and documented the current gate state. It did not launch model agents or alter credentials, host policy, branch protection, or workflow behavior.

## Immutable refs and GitHub evidence

- Repository: `VlDMlNSh/mediahub-os`
- Current `main` HEAD: [`79196054d84b1197cea1447dd1db5ad075302834`](https://github.com/VlDMlNSh/mediahub-os/commit/79196054d84b1197cea1447dd1db5ad075302834); GitHub reports its commit signature verified.
- Active controller: [`.github/workflows/gemini-batch-dispatch-controller.yml`](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml), blob SHA `9453403bba899a2400ee3fb874d32badd034c704`.
- Current canonical documentation branch HEAD at start of this pass: `c85e1b4c78894a69da4f254098893cee9cc8e925`.
- Canonical map: [`MEDIAHUB-CHAT-TREE-MAP.md`](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md), blob SHA `30b1a0dae214eb61f5009084c4a6be8c30c7c9af`. Its contents endpoint returned empty text for this large file; this pass did not claim to re-read the map body.
- Governance issue: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301), open.
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437) remains Draft/open at head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14). Exact-head check-runs endpoint returned `total_count=0`; formal review listing returned no reviews. [PR #438](https://github.com/VlDMlNSh/mediahub-os/pull/438) also remains Draft/open.
- GitHub branch response says `main.protected=false`, required status checks disabled. Repository rulesets endpoint returned an empty list. The branch-protection detail endpoint returned HTTP 403 (integration permission boundary); no required protections were established.
- Controller run [39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) was `SKIPPED`. All four jobs were skipped: [batch admission](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179/job/119450946325), [non-launching probe](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179/job/119450947410), [probe assertion](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179/job/119450947925), and [dispatch/monitor](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179/job/119450997021). The run has no artifacts. The associated issue comment was a Wave 327 report, not a comment whose entire body was exactly `/next`; it was not a child dispatch.
- Main commit check-runs include historical skipped controller jobs and Astra Verify [39649841150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649841150) SUCCESS. This does not substitute for independent review, governance, trusted-main probe, or successful provider/child dispatch.

## Credential names and transport

- Owner reports the GitHub settings include `MEDIAHUB_GEMINI_BATCH_ENABLED` and the dispatch HMAC setting. The connected GitHub integration rejected direct Actions secrets/variables-list endpoints as unsupported, so metadata presence/value is **NOT independently verified**. No secret values were read.
- Controller source references the exact ASCII name `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`. The spelling `MEDIAHUB_DISPATCH_НМАС_KEY` contains Cyrillic characters in the HMAC segment and is **not the same identifier**. If that Cyrillic spelling was actually used as the GitHub secret name, the controller will not find the required ASCII secret and must fail closed. Do not print or expose values.
- Controller is the only permitted Gemini route; it holds `MEDIAHUB_GITHUB_TOKEN` for GitHub API dispatch/monitoring, while child workflows use separate provider credentials. No server, SentinelX, local Claude/Ollama or browser is used as Gemini transport.
- `main` protection/governance, formal independent review of the active implementation, exact-head CI for PR #437, effective minimum token permissions, secret separation, and a successful trusted-main no-secret probe remain open. Do not create an Issue #301 `/next` comment or dispatch the controller while these gates remain open, because the owner-reported batch setting may permit real child dispatch.

## Voktors-Mini.Dlink / SentinelX / agent-browser / Claude

- SentinelX host identity: `Voktors-Mini.Dlink`, stable host ID `host_5f7264034bdf0b51`, SentinelX agent `0.22.0`, macOS kernel `23.6.0`, arm64. Host inventory showed it operational, but requests intermittently timed out/disconnected and sessions reconnected.
- A full capability response was obtained. The command allowlist contains `which`, `ollama`, shell primitives and other explicit commands, but does **not** contain `agent-browser` or `claude`. This pass did not bypass that policy by wrapping an unapproved browser command in a shell.
- Bounded `which` probes: `ollama` resolved to `/opt/homebrew/bin/ollama`; `agent-browser`, `claude`, and `fcc-claude` returned exit code 1 / no path in those probes. Some parallel requests disconnected, so no broader host-health conclusion is made. A standalone Ollama binary does not prove the Claude-FCC-Ollama queue is configured or that it avoids paid fallbacks.
- Required CLI instruction `agent-browser skills get core` was **NOT RUN** because the command is not allowlisted and the executable did not resolve on PATH in this probe. No browser session, browser evidence, local Claude session/job ID, or queue execution exists. No allowlist/config change was made.
- Next local step: stabilize this exact host; locate/verify the installed browser CLI and intended Claude/FCC launcher; review the host policy; then authorize only the narrow required executable(s), run `agent-browser skills get core`, and inspect the browser in a read-only session. Separately prove Claude/FCC provider/auth and fallback behavior excludes paid routes before running the real queue.

## Run ledger

| Work item | Status | IDs / evidence |
|---|---|---|
| Gemini controller | SKIPPED; no valid `/next` trigger in run 39665960179 | [run 39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179) |
| Gemini Agent 1 | **NOT RUN** | No child run ID or artifact digest |
| Gemini Agent 2 | **NOT RUN** | No child run ID or artifact digest |
| Gemini Agent 3 | **NOT RUN** | No child run ID or artifact digest |
| Claude-FCC-Ollama on Voktors-Mini.Dlink | **NOT RUN** — launcher/route not verified | No local session/job ID |
| agent-browser on Voktors-Mini.Dlink | **NOT RUN** — executable path and allowlist gate unresolved | No browser session or evidence |

No provider calls, live child dispatch, secret reads, local model execution, merge, deployment, qualification or acceptance are claimed.

## Acceptance criteria for the next attempt

1. Independent security review and exact-head CI for the candidate/controller change.
2. Effective governance/protection confirmed; the repository currently reports `main` unprotected.
3. Confirm exact ASCII HMAC secret name and least-privilege transport-token scope without reading values.
4. Successful trusted-main no-secret probe; keep the batch flag unset/false until all gates are accepted.
5. Only then perform one controller-authorized three-child batch on one immutable SHA and record controller ID, all three child IDs, terminal conclusions, artifacts/digests and exact target SHA.
6. Independently stabilize Voktors-Mini, verify browser/Claude executable paths and policy, then run browser/Claude only on that host; never route Gemini through it.

Canonical map: [`MEDIAHUB-CHAT-TREE-MAP.md`](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).
