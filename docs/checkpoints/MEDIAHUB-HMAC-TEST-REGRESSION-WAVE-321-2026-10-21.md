# Wave 321 — merged-controller regression and HMAC test repair (2026-10-21)

## Disposition

**REGRESSION IDENTIFIED / FIX PR OPEN / EXACT-HEAD CI PENDING / GEMINI NOT DISPATCHED / CONTOUR A NOT QUALIFIED.**

This pass rechecked repository refs, PR #432, its review record, the main-branch controller and current CI. It found that PR #432 was merged at 2026-10-21T18:00:07Z even though the previously recorded acceptance gates were not closed and no formal review was present in the queried review API. The merge introduced a Python syntax error in the HMAC interoperability test. A minimal repair was prepared in PR #436; its checks were still running at the time of this report.

## Canonical references

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Current checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Merged controller PR #432: https://github.com/VlDMlNSh/mediahub-os/pull/432
- Regression repair PR #436: https://github.com/VlDMlNSh/mediahub-os/pull/436

## Refs and source evidence

- At inspection, main HEAD was `1a6e5a16ef9950b72dda04abd69a27f019922489`.
- PR #432 merge commit was `33ae44f3ca77337553b97819f5190d57d157fe5e`; GitHub reports merged at `2026-10-21T18:00:07Z`.
- Main controller blob: `9453403bba899a2400ee3fb874d32badd034c704`.
- Main HMAC transport test blob before repair: `c8552721df8ccf65f70387a4a8a95eb941870eef`.
- PR #432 review listing returned zero formal submitted reviews in this check. Branch-protection API returned 403 (`Resource not accessible by integration`), so effective protection/ruleset state remains **NOT VERIFIED**, not presumed disabled or enabled.
- The controller contains the owner-only Issue #301 `/next` bridge and closed-by-default `MEDIAHUB_GEMINI_BATCH_ENABLED` gate. Its API dispatch path remains controller-confined; no child workflow was launched in this pass.

## Failure evidence

- Astra Verify failed on main SHA `1a6e5a16ef9950b72dda04abd69a27f019922489`: [run #39648781086](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648781086), job `119391303690`.
- Gemini workflow contract validation failed on merge commit `33ae44f3ca77337553b97819f5190d57d157fe5e`: [run #39648761390](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761390), job `119391238470`.
- Both logs show `SyntaxError` in `tests/test_gemini_transport_controller_contract.py`: the `next(...)` expression assigning `controller_signature_line` lacked a closing parenthesis; the corresponding `child_expected_line` expression had the same defect. CI failed before HMAC contract assertions ran.

## Repair PR #436

- Branch: `fix/wave321-hmac-test-syntax-20261021`.
- Repair commit: `960a57e6278e28867c5f8ec797f38638a786999e`.
- Updated test blob: `465f9c4a970d6b8a13bc81abfa44d9bc57ac7e1d`.
- The change adds only the two missing closing parentheses; it does not modify runtime workflows, permissions, secrets or dispatch behavior.
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/436
- Exact-head runs observed in progress at report creation: Astra Cloud Runtime Validation `39649269850`, Astra Verify `39649269844`, Gemini workflow contract validation `39649269833`. No passing claim is made until these checks reach terminal success on the exact head.

## Orchestration and executor status

- Gemini controller run ID: **NONE**. Gemini child workflow/run/job IDs: **NONE**. Agent mode was not dispatched.
- Claude on Alamo: **NOT RUN**; current SentinelX inventory exposes only `Voktors-Mini.Dlink` as operational, not Alamo/server 3. Disabled `mh-dev-01` and `mh-dev-02` are not substitutes.
- Browser evidence on Alamo: **NOT RUN**.
- Secret values were not read. The branch-protection endpoint was inaccessible to the connected integration; no governance conclusion is inferred from that denial.
- No paid fallback, runtime route, secret change, batch-gate enablement or deployment occurred.

## Required gates before any agent-mode launch

1. Get PR #436 exact-head CI green and re-read the merged result and test blob SHA.
2. Obtain genuine independent security review of controller/child HMAC, replay suppression, token scope, event guard and provider-secret separation.
3. Verify effective branch protection/rulesets and secret/variable *presence/metadata only*, without reading values; keep the batch gate closed.
4. Run a trusted-main no-secret controller probe and prove that an owner-authored `/next` event causes one replay-safe controller run and **zero** child dispatches while the gate is false.
5. Identify Alamo by host ID/capabilities/allowlist and qualify its permitted free Claude Code route with no paid fallback.
6. Only after all gates pass, run a controlled first batch and record controller ID, three child IDs/statuses, immutable target SHA, artifact digests and independent verification.

Status is **repair implemented / CI pending / controller integration not qualified / agent dispatch NOT RUN / Contour A NOT ACCEPTED**.


## Follow-up correction after the first CI attempt

The first repair commit `960a57e6278e28867c5f8ec797f38638a786999e` fixed the two syntax errors in the primary HMAC interoperability loop, but CI found a third malformed `next(...)` expression in the replay-case block (same test file, line 205). This was a second occurrence of the same defect and was corrected in the same PR branch.

- Latest PR #436 head: `7c45e920982a69169fc856a1739cb73445be904f`.
- Latest test blob: `01ddae5e1d7fd0e49ffa651da9655a5a5ad7a8d5`; read-back confirmed all three `next(...hmac.new(...))` expressions close correctly.
- Latest exact-head runs observed: Cloud Runtime Validation [#39649630864](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649630864) SUCCESS; workflow contract validation [#39649630799](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649630799) and Astra Verify [#39649630775](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649630775) were still running when checked. Therefore CI remains pending and the repair is not yet verified.
