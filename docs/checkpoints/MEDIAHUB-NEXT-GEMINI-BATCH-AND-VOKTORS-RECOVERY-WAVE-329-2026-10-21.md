# Wave 329 — Gemini batch admission and Voktors executor recovery check

Date: 2026-10-21  
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)  
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/tree/docs/mediahub-chat-tree-map-20261012).

## Objective and immutable references

- Current `main` HEAD: `79196054d84b1197cea1447dd1db5ad075302834`.
- Controller `.github/workflows/gemini-batch-dispatch-controller.yml` blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
- Current canonical documentation branch HEAD at inspection: `778af25d5b07eb70269d7e91d1ecddbab8133f66`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN.

## Gemini transport and dispatch evidence

The controller is GitHub-hosted and its child dispatches use GitHub Actions workflow-dispatch API. No physical server is part of the cloud Gemini route.

Latest inspected controller runs against main SHA `79196054d84b1197cea1447dd1db5ad075302834`:
- [39667761725](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667761725): `issue_comment`, all four jobs SKIPPED; no artifacts.
- [39667424495](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39667424495): all four jobs SKIPPED; no artifacts.
- [39665960179](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39665960179): all four jobs SKIPPED; no artifacts. Its display title identifies comment `6325212756`, which was a report comment, not the exact trigger body `/next`.

The controller readiness gate requires `vars.MEDIAHUB_GEMINI_BATCH_ENABLED == true`; the launch step also requires a trusted `main` controller context and non-empty exact secret names `secrets.MEDIAHUB_GITHUB_TOKEN` and `secrets.MEDIAHUB_DISPATCH_HMAC_KEY`. It signs each child dispatch and monitors exact correlated run IDs. No secret values were read. The connected GitHub integration rejects repository Actions variable/secret endpoints, so configured names, effective scope/value, token permissions and HMAC validity remain NOT VERIFIED by this pass.

**Identifier correction:** the controller expects ASCII `MEDIAHUB_DISPATCH_HMAC_KEY`. The owner-supplied spelling `MEDIAHUB_DISPATCH_НМАС_KEY` contains Cyrillic characters in the `НМАС` segment and is not the same identifier. Do not rename/delete anything blindly; verify the actual secret name in Settings. If only the Cyrillic/misspelled name exists, create the exact ASCII name with the intended key value using GitHub UI, without displaying or transmitting the value in chat.

PR [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437) is OPEN/DRAFT/UNMERGED at head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`, base `1a6e5a16ef9950b72dda04abd69a27f019922489`; no requested reviewers, no formal review submissions, no combined status entries and no exact-head workflow runs were returned. Main's combined commit status also reports zero statuses; one earlier Astra Verify run `39649841150` succeeded, but that is not proof of the full current admission gate. The branch response says `main.protected=false`; rulesets query returned an empty list, while detailed branch-protection API returned 403 for the connected integration. Governance remains NOT VERIFIED.

Gemini Agent 1: **NOT RUN**. Agent 2: **NOT RUN**. Agent 3: **NOT RUN**. Controller/child IDs for a real batch: none. Child reports and artifact digests: none. No model call is claimed. No trigger was posted by this pass.

## Voktors-Mini.Dlink macOS, Claude/FCC and agent-browser

SentinelX identifies the intended host as `Voktors-Mini.Dlink`, stable ID `host_5f7264034bdf0b51`, agent `0.22.0`, operational inventory flag true. However, live `ping`, `capabilities`, `state` and `help` calls timed out (60 s); a read-only `pwd` probe returned `agent_disconnected / duplicate_session`. This means host presence in inventory is not proof of a responsive command channel.

The agent-browser skill stub was read. Its installed-version instructions must be retrieved on the host with `agent-browser skills get core` before any browser command. This command was NOT RUN because current SentinelX capabilities/allowlist could not be obtained and host calls are unstable. No browser session or browser test is claimed. Previous bounded inventory found `claude` and `ollama` absent from PATH; Claude-fcc-Ollama free-only routing remains NOT VERIFIED. No paid fallback or alternate host was used.

The cloud Gemini design remains independent of physical servers; local Claude/browser availability is a separate executor lane and must not gate cloud dispatch.

## Verification and classification

- Read-back completed for this report after creation is still required; blob SHA and branch HEAD are to be recorded after write.
- No application code, workflow, secret, variable, allowlist, host service, merge or deployment was changed.
- Gemini batch: **BLOCKED / NOT DISPATCHED**.
- Claude-fcc-Ollama: **NOT RUN / NOT VERIFIED**.
- agent-browser: **NOT RUN / NOT VERIFIED**.
- Contour A qualification/acceptance: **NOT ACCEPTED**.

## Next bounded step

1. Resolve the exact ASCII HMAC secret name and verify the batch variable's effective scope without revealing values; independently establish token least privilege.
2. Obtain independent review, exact-head CI and authoritative governance/trusted-main no-secret-probe evidence for PR #437/controller.
3. Only after all gates pass, use the controller on `main` with one immutable target SHA and record its run ID, all three child run IDs/statuses, reports and artifact digests.
4. Restore SentinelX command-channel stability; re-read full capabilities/allowlist; then retrieve the installed agent-browser core guide and qualify the free-only Claude/FCC route separately.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## Follow-up verification from the same Wave 329 pass

- Rechecked SentinelX after the initial report: host inventory, ping, summary capabilities and `help(topic=index)` / `help(topic=operations)` did return successfully. The host is `Voktors-Mini.Dlink`, ID `host_5f7264034bdf0b51`, macOS kernel `23.6.0`, ARM64, SentinelX `0.22.0`. This proves control-plane reachability, not command execution readiness.
- A direct `agent-browser --version` invocation timed out. Background attempts returned failures `job_e0b52555987d` (duplicate_session) and `job_f2c139badedb` (agent did not respond within 10 seconds); notification polling showed no active/running jobs. Thus browser core instructions remain unretrieved and no browser session was opened.
- The latest controller/PR check still returns no exact-head runs/statuses or formal PR reviews. Gemini Agents 1–3 remain NOT RUN; no controller or child run IDs were created in this pass.
- This report has now been re-read after creation; current blob SHA is to be captured by the final readback. No host allowlist, workflow, secret or variable was modified.


### Owner spelling clarification

The latest user message spells the requested identifier as ASCII `MEDIAHUB_DISPATCH_NMAC_KEY` (not Cyrillic). This still differs from the controller's exact `MEDIAHUB_DISPATCH_HMAC_KEY`. No secret metadata/value can be read through the connected integration. Verify the exact name in GitHub Settings and add the controller-expected ASCII name if it is missing; do not display or transmit its value.
