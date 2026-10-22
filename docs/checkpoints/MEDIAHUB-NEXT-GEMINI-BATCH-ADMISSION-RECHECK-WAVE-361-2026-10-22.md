# Wave 361 — Gemini batch admission recheck and dispatch boundary

Date: 2026-10-22. Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Scope and immutable target

Bounded read-only recheck following Wave 360. Re-read the live controller from `main`, the canonical Bootstrap/map/checkpoint/Roadmap on `docs/mediahub-chat-tree-map-20261012`, Issue #301, PR #437 and PR #441. No dispatch, host command, secret read, branch mutation, merge, or deployment was performed.

- Controller on `main`: [gemini-batch-dispatch-controller.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml), blob SHA `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f`.
- Last independently verified `main` HEAD remains the Wave 360 merge SHA `7cbbc0025ce01b8c476d512cfc5e12dc35fd952c`; the current branch ref was not independently re-queried by a dedicated ref endpoint in this pass, so treat this as the last verified HEAD, not a newly confirmed HEAD.
- Canonical map blob SHA at read-back: `ba5731256321251b6a92b35d51f5bd0f2c1d4e86`.
- Canonical Bootstrap blob SHA: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical checkpoint blob SHA: `89a8721f3509212b4e38e4d5bdd55560ba629fa9`.
- Wave 360 report remains [available](MEDIAHUB-NEXT-POST-MERGE-RECHECK-WAVE-360-2026-10-22.md), blob SHA `9af5a3c13a5adcab25bbd0d95233481e54197e37`.
- Master Roadmap was re-read from the canonical docs branch; it remains the required planning authority. Its retrieved response was truncated in this pass, so no new roadmap item/status is inferred from that partial response.

## Controller contract findings

- Controller supports `workflow_dispatch` with `mode=probe|agents`, defaults to `probe`, and defaults confirmation to `no`.
- The batch readiness gate reads `vars.MEDIAHUB_GEMINI_BATCH_ENABLED`; unless its normalized value is `true`, it sets output `enabled=false` and downstream child dispatch is skipped.
- The controller's separate issue-comment path can dispatch only for an exact `/next` comment on Issue #301 authored by an OWNER, on trusted `main`, with the batch flag enabled and the controller's remaining credential/HMAC/authorization checks passing. Posting that trigger now would be unsafe because it could launch real work if the setting changed; no comment was posted.
- The user explicitly reports `MEDIAHUB_GEMINI_BATCH_ENABLED=false`. This is owner-provided configuration evidence, not an API-verified variable read. Therefore the correct current disposition is to keep the batch disabled; do not change it in this pass.
- Available connected GitHub tool inventory has no workflow-dispatch write operation. No controller run ID, child run/job IDs, artifacts, or digests were created. Do not claim a probe or batch was executed.
- The PR #437 post-merge Astra Verify remains positively evidenced by run [39765496724](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39765496724), job `119779790759`, on merge SHA `7cbbc0025ce01b8c476d512cfc5e12dc35fd952c`. Full post-merge controller contract CI remains NOT VERIFIED from available evidence.
- Branch rules endpoint previously returned an empty ruleset list and branch-protection endpoint returned 403; effective governance remains NOT VERIFIED. Secret/variable metadata scopes remain NOT VERIFIED by API. No secret values were accessed.
- PR #441 is still listed open in the last fetched metadata; its comments endpoint returned an empty list. Its current exact-head checks/review status were not qualified by this pass.

## Status ledger

| Gate | Status | Evidence |
|---|---|---|
| Controller contract source read | VERIFIED | Blob SHA `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f` |
| Owner reports batch flag false | VERIFIED as owner-provided statement | Current user message; settings API not available |
| Batch flag API metadata | NOT VERIFIED | Integration lacks variable metadata access |
| Exact current main ref in this pass | NOT VERIFIED | Last verified SHA is recorded; no dedicated ref query available in this pass |
| Exact-head post-merge Astra Verify | VERIFIED historically | Run `39765496724`, job `119779790759` |
| Full post-merge controller contract CI | NOT VERIFIED | No exact-head run IDs evidenced |
| Effective branch governance | NOT VERIFIED | Prior ruleset/branch-protection limitations |
| Trusted-main no-secret probe | NOT RUN | Required gates unresolved; no dispatch tool available |
| Gemini Agents 1–3 controller batch | NOT RUN | Batch remains disabled; no dispatch tool available |
| Contour A | BLOCKED / NOT QUALIFIED / NOT ACCEPTED | Mandatory gates and runtime evidence incomplete |

## Next safe step

1. Keep `MEDIAHUB_GEMINI_BATCH_ENABLED=false`.
2. From an authorized GitHub Actions UI or approved dispatch-capable integration, run only the controller's trusted-main `probe` mode with `confirm=no` and record its run/job IDs and caller-context outputs. Do not invoke `agents`.
3. Independently establish exact-head controller-contract CI and effective governance, and verify secret/variable identifiers and scopes without exposing values.
4. Only after the probe and all required gates pass, have the owner explicitly enable batch admission and dispatch `agents` through the approved controller with a fixed 40-hex target SHA. Record controller run ID, all three child run/job IDs, statuses, artifacts/digests, tests and independent review.
5. Continue independent read-only schema/queue work under Issue #301 without using a server as Gemini transport.

Final status: **CONTROLLER CONTRACT READ / BATCH FLAG REPORTED FALSE / PROBE NOT RUN / GEMINI BATCH NOT RUN / CONTOUR A NOT ACCEPTED**.
