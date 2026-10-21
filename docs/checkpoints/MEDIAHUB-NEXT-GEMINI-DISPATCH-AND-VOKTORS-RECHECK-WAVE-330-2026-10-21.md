# Wave 330 — Gemini dispatch gate and Voktors-Mini execution-channel recheck

Date: 2026-10-21  
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)  
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

## Scope and immutable references

- Live `main` HEAD at this pass: `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`; commit message: `docs: remove misplaced Wave 329 addendum from main`.
- Controller `.github/workflows/gemini-batch-dispatch-controller.yml` blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
- Canonical documentation branch HEAD at recheck: `332d5275262bb20b4d6bb35ba8eb0d7e56a560fc`.
- Governing [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open.

## Gemini / GitHub transport

The controller is GitHub-hosted. Its three child dispatches use GitHub Actions workflow-dispatch API with a shared immutable target SHA; no physical server is required for Gemini execution. The controller source at the recorded blob contains:
- a non-launching `probe` default;
- the explicit `vars.MEDIAHUB_GEMINI_BATCH_ENABLED == true` admission check;
- the exact ASCII secret names `secrets.MEDIAHUB_GITHUB_TOKEN` and `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`;
- HMAC-signed child envelopes and correlated child-run monitoring.

This source inspection is not proof that the credentials are configured or that Gemini was invoked.

Latest live-main evidence:
- [Controller run 39669477347](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669477347), on main SHA `5cac2f27685c88e5e5e391fcf315d07fc16c6a6b`, completed `skipped`. All four jobs were skipped; it produced no artifacts. Its source comment ID was `6325680146`, whose body was a report, not the exact `/next` trigger.
- The current-main check inventory includes [run 39669722103](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669722103), also with controller jobs skipped, and [Astra Verify run 39669337754](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39669337754) successful. These are not evidence of child Gemini model runs.
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437) remains open and Draft at `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; review listing is empty, and exact-head combined status/workflow-run wrappers returned no entries.
- GitHub branch metadata reports `main.protected=false`, with required status checks disabled; the repository rulesets listing is empty. This is a governance blocker, not a green light.
- The connected GitHub integration rejects repository Actions variable/secret metadata endpoints. No secret values were read; token permissions, effective variable value/scope, HMAC validity and secret separation remain NOT VERIFIED.

### Exact credential identifier

The controller expects the exact ASCII secret identifier `MEDIAHUB_DISPATCH_HMAC_KEY`. The recently supplied strings `MEDIAHUB_DISPATCH_NMAC_KEY` and `MEDIAHUB_DISPATCH_НМАС_KEY` are not that identifier: the first spells NMAC rather than HMAC, and the second also uses Cyrillic characters. This does not prove the correct secret is absent; it means its exact presence must be verified in GitHub Settings. Do not read, copy, or disclose secret values. The batch variable identifier is exactly `MEDIAHUB_GEMINI_BATCH_ENABLED`.

## Agent ledger

| Executor | State | Evidence |
|---|---|---|
| Gemini Agent 1 | NOT RUN | No controller-admitted batch, child run ID, report, or artifact digest |
| Gemini Agent 2 | NOT RUN | No controller-admitted batch, child run ID, report, or artifact digest |
| Gemini Agent 3 | NOT RUN | No controller-admitted batch, child run ID, report, or artifact digest |
| Controller | SKIPPED | Run `39669477347`; no child dispatch |
| Claude-fcc-Ollama on Voktors-Mini.Dlink | NOT RUN | SentinelX remote command/script request disconnected during the call; no executor process/result evidence |
| agent-browser on Voktors-Mini.Dlink | NOT RUN | Required `agent-browser skills get core` retrieval did not complete; no browser session/evidence |

## SentinelX / Voktors-Mini.Dlink

- Host identity is positively established by SentinelX inventory: `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, macOS 14.7.4, ARM64, SentinelX agent 0.22.0.
- The host returned successful ping/pong responses during this pass, and a summary capabilities response reported 95 allowed commands, two readable paths and two writable paths.
- Full capability/allowlist detail repeatedly timed out or disconnected; a bounded read-only script request returned `agent_disconnected / duplicate_session`. Thus the actual command allowlist and current browser/Claude/Ollama executable state could not be re-verified reliably.
- No browser command/session was run; no host allowlist, installation, secret, or provider configuration was changed. No paid Claude fallback was used.

## Decision

**Dispatch remains BLOCKED; no qualification or acceptance is claimed.** Do not post the exact `/next` trigger or manually launch agent mode while the main branch is unprotected and PR #437 lacks exact-head CI/review evidence. This pass did not launch Gemini, Claude, or browser work.

## Next bounded actions

1. In [Actions Secrets](https://github.com/VlDMlNSh/mediahub-os/settings/secrets/actions), verify metadata/name only: `MEDIAHUB_DISPATCH_HMAC_KEY` must exist with exact ASCII spelling and must be separate from `MEDIAHUB_GITHUB_TOKEN`. Never reveal either value.
2. In [Actions Variables](https://github.com/VlDMlNSh/mediahub-os/settings/variables/actions), verify `MEDIAHUB_GEMINI_BATCH_ENABLED` is configured at repository scope used by the controller; do not use the value alone to bypass other gates.
3. Restore governance on [branch settings](https://github.com/VlDMlNSh/mediahub-os/settings/branches), obtain independent review and exact-head CI for [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437), and prove the trusted-main no-secret probe before considering a single controller-only batch against one immutable SHA.
4. Restore a stable SentinelX command channel; then re-check the exact allowlist and executable availability. Only after policy verification, retrieve `agent-browser skills get core`, validate the browser in a non-mutating session, and separately qualify the Claude/FCC free-only route with no paid fallback.
5. After all admission gates pass, use the GitHub controller only for three Gemini children; record controller and child run IDs, statuses, target SHA, reports, and artifact digests.

No secret values were read. No controller launch, child dispatch, merge, deployment, or local executor run is claimed.
