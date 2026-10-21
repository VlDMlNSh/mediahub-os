# Wave 324 — Gemini dispatch gate and executor identity audit (2026-10-21)

## Disposition

**NO LIVE GEMINI DISPATCH. THREE CHILD AGENTS NOT RUN. CONTOUR A NOT QUALIFIED.**

The user explicitly requested three Gemini cloud agents over the existing GitHub Actions API transport, without routing Gemini through physical hosts, plus local Claude and agent-browser on the third Alamo server. This pass rechecked live refs, source, CI, issue comments and SentinelX host inventory. The live batch remains blocked by required security/governance evidence and an unverified Alamo identity. No credentials were read; no dispatch or model call was attempted.

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Main HEAD: `79196054d84b1197cea1447dd1db5ad075302834`
- Canonical docs branch HEAD before this report: `a93a4feb637a92b8adb61594881dcc429f13820c`

## Live GitHub state and source evidence

- PR #432 is merged; merge commit `1a6e5a16ef9950b72dda04abd69a27f019922489`. The current main controller blob is `9453403bba899a2400ee3fb874d32badd034c704`; transport contract test blob `01ddae5e1d7fd0e49ffa651da9655a5ad7a8d5`.
- Main Astra Verify [run #39649841150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649841150) succeeded on main HEAD `79196054d84b1197cea1447dd1db5ad075302834`.
- Current child workflow blobs on main: Agent 1 `155a02159912ca371e6f826c51325ca269857aad`; Agent 2 `fff1820a6b97d379b23674f36bd62227b7d4dec2`; Agent 3 `781df56e8aa7c75ba453c08378611857862b2e44`. Each declares `runs-on: ubuntu-latest` and the source audit found no Alamo, SentinelX, agent-browser or Claude dependency in those child workflows. This is source-level isolation only, not evidence of live runs.
- The controller permits issue-comment admission only for an exact `/next` comment by the repository owner on non-PR Issue #301. It separately requires `vars.MEDIAHUB_GEMINI_BATCH_ENABLED` to equal `true`. A comment on a PR is not a valid admission event.
- Controller run [#39650408656](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39650408656) was **SKIPPED**. Its source was comment [#6323130946 on PR #436](https://github.com/VlDMlNSh/mediahub-os/pull/436#issuecomment-6323130946), not Issue #301. All controller jobs were skipped. It is not a successful controller run and created no child runs or artifacts.
- PR #437 (`[Draft] Repair Gemini HMAC contract tests and execute child authorization`) remains open/Draft/unmerged at observed HEAD `01629874e8b4a10da68a0574ec77ecdfceeda8b9`; the formal review API returned zero submitted reviews. No verified exact-head CI evidence for that latest PR head was found in this pass. Do not attribute older-head results to it.

## Admission gates still unproven

1. **Independent security review:** no formal submitted review tied to current controller/child workflow blobs. Source-level review is not an independent reviewer qualification.
2. **Actions variable and secret metadata:** the available read-only connector could not retrieve repository Actions variable/secret metadata. `MEDIAHUB_GEMINI_BATCH_ENABLED` state and the effective least-privilege scope of `MEDIAHUB_GITHUB_TOKEN` therefore remain **NOT VERIFIED**. Secret values were not read.
3. **Branch protection/rulesets:** authoritative settings evidence remains unavailable through the connected read-only integration (prior API returned 403). This does not imply that protection is absent.
4. **Trusted-main no-secret probe:** current evidence is not sufficient to claim this gate has passed in the trusted-main context.
5. **Contour A product gates:** Issue #301 still governs issuer/capability, task scope, target manifest, schema and evidence qualification. Green general CI does not satisfy those gates.

Do not post `/next` to Issue #301 or manually dispatch agent mode until these gates are evidenced. Do not change the batch admission variable as a substitute for the gates.

## Local executor and browser

SentinelX reports only one connected host: `Voktors-Mini.Dlink`, ID `host_5f7264034bdf0b51`, macOS-like kernel `23.6.0`, arm64. The other enrolled hosts `mh-dev-01` and `mh-dev-02` are disabled. No connected host is positively identified as **Alamo / server 3**. A ping succeeded, but detailed state/project snapshot calls timed out, so no stronger identity claim is justified.

- Claude Code / FCC / FreeLLMAPI on Alamo: **NOT RUN** — host identity and approved free-only route not verified.
- agent-browser on Alamo: **NOT RUN** — no verified Alamo host. The prior Wave 323 report records a read-only browser inspection on Voktors-Mini; that is not substituted for the requested Alamo session.
- Gemini transport did not use any physical host or local Claude executor.

## Executor ledger

| Executor | State | Evidence |
|---|---|---|
| Controller | `SKIPPED` (observed unrelated comment event) | run #39650408656 |
| Gemini Agent 1 | `NOT RUN` | no child run ID |
| Gemini Agent 2 | `NOT RUN` | no child run ID |
| Gemini Agent 3 | `NOT RUN` | no child run ID |
| Claude Code / Alamo | `NOT RUN` | Alamo identity/free-only route not verified |
| agent-browser / Alamo | `NOT RUN` | Alamo identity not verified |
| Shared immutable target SHA | `NOT ASSIGNED` | no admitted batch |
| Child report/artifact digests | `NONE` | no child runs |

## Next bounded step

Verify the non-disclosing repository Actions variable/secret metadata and authoritative branch-protection/ruleset state; obtain a formal independent security review of the exact main controller and all three child workflow blobs; complete a trusted-main no-secret probe. Separately identify/connect Alamo through SentinelX and read `agent-browser skills get core` on that exact host before any browser operation. Only after these gates pass should an owner-authored exact `/next` comment on Issue #301 admit one batch. Record the controller run ID, all three child run IDs/conclusions, one common target SHA, artifact digests and independent verification.

No secrets were read. No Gemini dispatch, model call, Claude session, browser session on Alamo, merge, deployment, qualification or acceptance occurred in this pass.
