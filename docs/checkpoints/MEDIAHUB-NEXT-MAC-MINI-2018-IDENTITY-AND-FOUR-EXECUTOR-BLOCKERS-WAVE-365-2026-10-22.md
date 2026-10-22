# MediaHub OS — Wave 365: Mac mini 2018 identity sweep and four-executor launch blockers

- Date: 2026-10-22
- Base main SHA verified at start: `25a2883bb8e3099df49c9bd688c028958102bc95` (merge commit for PR #450).
- Working branch: `docs/wave-365-mac-mini-2018-global-identity-2026-10-22`
- Status: DOCUMENTATION CORRECTION PARTIAL / GEMINI BATCH NOT DISPATCHED / LOCAL CLAUDE NOT RUN / EXACT-HEAD CI NOT VERIFIED.

## 1. Owner clarification and PR #450

PR #450, [docs(wave-364): correct Alamo host identity to Voktors-Mini](https://github.com/VlDMlNSh/mediahub-os/pull/450), is merged. Merge commit: `25a2883bb8e3099df49c9bd688c028958102bc95`. Current main ref recheck at the beginning of this pass returned the same SHA.

The owner clarifies that Alamo is hosted on `Voktors-Mini.Dlink`, which is the Mac mini 2018, and that this device is the intended local executor host. This supersedes the earlier mistaken interpretation that Alamo was a different host from the central Mac Pro role.

## 2. Mac Pro phrase sweep

GitHub repository search returned up to 100 candidate files for the terms “Mac Pro”; because the search tokenization also matched unrelated words such as “production” and “proposal”, every candidate was checked for the exact phrase. Three source documents contained actual `Mac Pro` references and were corrected on this branch:

- `architecture/MEDIAHUB-DISTRIBUTED-AI-INFRASTRUCTURE.md` — blob SHA `a7eba183aecf726cf6f720ed96059b5023793001`
- `docs/checkpoints/MEDIAHUB-JARVIS-CORPORATION-ARCHITECTURE-PROPOSAL-CROSSWALK-WAVE-01-2026-10-15.md` — blob SHA `04251812428e1154266b7a3ec49c3ec51907a4a7`
- `docs/checkpoints/MEDIAHUB-CONTOUR-A-WB-14-JARVIS-A0-AND-DIRECT-LOCAL-ROUTE-SOURCE-RECONCILIATION-2026-10-15.md` — blob SHA `048376919db64de57e96e3ca56207eaf8a82f295`

All exact `Mac Pro` phrases in those three files are now replaced with `Mac mini 2018`. The architecture text now states that `Voktors-Mini.Dlink` is the owner-identified Mac mini 2018 hosting Alamo and the central-infrastructure role. The generic “Mac mini/Linux worker” role remains distinct only if later inventory establishes a separate device.

Scope limitation: this was a source-backed sweep of the 100 search candidates returned by GitHub, not a proof that every branch, historical commit, issue, PR comment, release artifact, or file beyond that search result set contains no phrase. The open PR will include a final exact-string recheck on the changed source branch.

## 3. Gemini transport and controller evidence

Owner-provided run: [39773148250](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39773148250).

- Run conclusion: SUCCESS for the non-launching probe.
- Target SHA: `7cbbc0025ce01b8c476d512cfc5e12dc35fd952c` (the pre-PR-450 main head, not current main).
- Probe job `119805409315`: SUCCESS.
- Context assertion job `119805451915`: SUCCESS.
- Readiness gate job `119805411025`: SKIPPED.
- `dispatch_and_monitor` job `119805411677`: SKIPPED.
- Gemini child run IDs, child artifacts, and artifact digests: none created by this run.

This was a successful probe, not a Gemini-agent launch. The controller contract on main requires `vars.MEDIAHUB_GEMINI_BATCH_ENABLED == true` and, for manual agent mode, `mode=agents` plus `confirm=yes`. The owner has reported this variable as false in prior passes. The newly mentioned `SENTINEL_REQUEST_API_KEY` is a SentinelX credential and does not itself enable the GitHub Actions variable or replace `MEDIAHUB_GITHUB_TOKEN` / `MEDIAHUB_DISPATCH_HMAC_KEY`. I did not read any secret value.

No direct workflow-dispatch action is exposed by the connected GitHub integration in this conversation. I did not bypass the controller or trigger individual child workflows directly because the project contract requires Gemini to use the approved controller/GitHub transport.

## 4. Local Claude lane

Owner-confirmed host identity:
- Host: `Voktors-Mini.Dlink`
- SentinelX host ID: `host_5f7264034bdf0b51`
- Reported platform: macOS, kernel `23.6.0`, architecture `arm64`, SentinelX agent `0.22.0`.
- Connected/operational status was returned by `sentinel_list_hosts`; bounded capabilities summary succeeded and reported 95 allowed commands, one service, nine playbooks, two file-operation paths, and two writable paths.

The approved repo path used in prior notes, `/Users/voktor/dev/mediahub-pr437-sync`, is not in the current SentinelX file-operation allowlist. Only `/Users/voktor/sentinelx/workspace` and `/Users/voktor/sentinelx/config.yaml` were listed. A full capabilities request timed out; a read-only `claude --version` check then failed with `agent_disconnected / duplicate_session`. No Claude task was executed, no browser was started, and no files were changed on the host.

The prior local-route evidence only established some Ollama/FCC/OmniRoute inference connectivity, not reliable Claude Code tool execution. The local executor therefore remains NOT QUALIFIED. The SentinelX API key does not override host allowlists or prove Claude's no-paid-fallback route.

## 5. Current disposition

| Lane | Status | Evidence / blocker |
|---|---|---|
| Gemini 1–3 manual independent tasks | NOT RUN | Probe only; controller admission/dispatch skipped; batch variable reported false; no direct dispatch action exposed here. |
| Claude local task on Alamo | NOT RUN | Host confirmed by owner, but current host calls are unstable; repo path not allowlisted; full capability/route check not completed. |
| PR #450 host identity correction | MERGED | Merge commit `25a2883bb8e3099df49c9bd688c028958102bc95`. |
| Mac mini 2018 wording correction | PREPARED | Three actual-phrase source documents corrected on this branch; broad historical corpus still needs final exact-string verification. |
| Wave 365 docs PR | PLANNED | Report, map addendum, and checkpoint overlay are being assembled; exact-head CI/review must be checked after PR creation. |

## 6. Next bounded step

1. Finish the branch's docs and create a PR; reread the changed blobs and search the branch for exact `Mac Pro`.
2. Requalify the GitHub dispatch gate without enabling it prematurely. The next agent-mode attempt must be controller-owned and must capture the controller run ID, three child run/job IDs, terminal statuses, artifact digests and independent review.
3. Recover stable SentinelX sessions; verify allowlisted paths and the local Claude/FCC/Ollama no-paid-fallback route before invoking Claude Code. Do not treat inference-only evidence as tool-execution qualification.
4. Keep all missing execution evidence explicitly NOT RUN / NOT VERIFIED.
