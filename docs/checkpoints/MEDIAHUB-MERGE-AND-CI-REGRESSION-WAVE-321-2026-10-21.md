# Wave 321 — post-merge verification and HMAC contract test regression (2026-10-21)

## Disposition

**PR #432 MERGED / UUID AND HMAC CONTRACT SOURCE PRESENT ON MAIN / POST-MERGE CI FAILED / MINIMAL FIX PR #434 OPEN / AGENT DISPATCH NOT RUN.**

This pass revalidated repository state after the owner reported completing prior actions. It found a merged controller candidate, but also found the newly added HMAC interoperability test contains a syntax error. The post-merge exact-head CI run failed on this defect. A one-line correction is proposed separately in Draft PR #434; no runtime behavior changed and no agents were dispatched.

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Merged PR: https://github.com/VlDMlNSh/mediahub-os/pull/432
- Follow-up fix PR: https://github.com/VlDMlNSh/mediahub-os/pull/434
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`

## Ref / SHA state

- PR #432 is CLOSED / MERGED (observed merged_at 2026-10-21T18:00:07Z).
- PR #432 final head: `33ae44f3ca77337553b97819f5190d57d157fe5e`.
- PR #432 merge commit / observed base for follow-up PR: `1a6e5a16ef9950b72dda04abd69a27f019922489`.
- Main controller blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
- Main child workflow blob SHAs:
  - Agent 1: `155a02159912ca371e6f826c51325ca269857aad`
  - Agent 2: `fff1820a6b97d379b23674f36bd62227b7d4dec2`
  - Agent 3: `781df56e8aa7c75ba453c08378611857862b2e44`
- Main transport test blob SHA: `65bc0c4b9a7eb58a71bb1b8123cf1ff4305f52af`.
- PR #434 head: `04442fe0aac243499231b1233e0a84eff0a33ede`; test blob SHA after one-line fix: `785618fad51ecf898b35132f6e43b196a18f7eae`. PR #434 remains OPEN / DRAFT / UNMERGED.

## Failure evidence and correction

Post-merge runs on PR #432 head `33ae44f3ca77337553b97819f5190d57d157fe5e`:
- [Controller probe 39648761507](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761507): success; probe only.
- [Cloud Runtime Validation 39648760929](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648760929): success.
- [Caller-context probe 39648761566](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761566): success.
- [Astra Verify 39648761007](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761007): failure at `python -m compileall -q .`.
- [Workflow contract validation 39648761390](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761390): failure at transport contract suite import.

Both failures point to `tests/test_gemini_transport_controller_contract.py:140`: `controller_signature_line = next(line for line in controller_lines if line.startswith("sig=hmac.new(")` was missing the closing parenthesis for `next(...)`. This prevented all tests in that module from loading.

Correction on PR #434 adds the missing final parenthesis only. No secrets or provider credentials were read. PR #434 exact-head CI was still in progress at report creation; its final status must be checked before integration.

## Current controller security review / governance evidence

- Source read-back on `main` confirms the controller uses GitHub API dispatch with `MEDIAHUB_GITHUB_TOKEN`, separate HMAC signing, fixed three child workflows, shared immutable target SHA and canonical UUIDv4 checks in each child.
- The test suite now contains an executable HMAC canonicalization/interoperability test with tampered-task and cross-workflow-signature rejection cases, once its syntax defect is corrected.
- GitHub's formal review API returns **zero submitted reviews** for PR #432. Its merge status alone is not evidence that the independent-review criterion was met. Do not retroactively mark this gate satisfied.
- No positive trusted-main agent dispatch was performed or evidenced. Probe runs are not agent runs.
- Current SentinelX host inventory has one operational host, `Voktors-Mini.Dlink` (`host_5f7264034bdf0b51`), with working capability/ping calls, but it is not verified as Alamo/server 3. The other enrolled hosts `mh-dev-01` and `mh-dev-02` are disabled. Free plan has one active host slot. No Claude or browser session was launched.
- A ChatGPT `/next` message does not itself create a GitHub issue-comment event. The repository's owner-only `/next` trigger applies to comments on Issue #301; an event bridge from this chat remains unimplemented/unproven.
- Issue #301's ordered gates remain: A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, accepted runner/workspace/network manifest, Draft 2020-12 schema validation and negative fixtures, semantic reference resolution, independent review and controlled runtime evidence.

## Per-/next executor evidence

| Executor | Status | Evidence |
|---|---|---|
| Gemini Agent 1 | NOT RUN | No controller run ID or child run ID |
| Gemini Agent 2 | NOT RUN | No controller run ID or child run ID |
| Gemini Agent 3 | NOT RUN | No controller run ID or child run ID |
| Claude Code / Alamo server 3 | NOT RUN | Alamo identity and approved free-only route not verified |
| agent-browser / Alamo | NOT RUN | Alamo host and browser capability not verified |

Controller run ID: **NONE**. Three child run IDs: **NONE**. Shared agent target SHA: **NOT ASSIGNED**. Agent artifact digests: **NONE**. No secrets were read, no provider/model invocation occurred, and no controller dispatch was attempted.

## Next bounded step

Wait for PR #434 exact-head CI to complete; inspect the specific HMAC contract test result and exact-head compile result. If green, keep the fix PR Draft until governance/independent-review criteria are explicitly resolved. Do not trigger `/next` on Issue #301 while the batch-enable variable and remaining admission gates are not independently evidenced.


## Follow-up CI reconciliation — 2026-10-21 18:08 UTC

- PR #434 first syntax correction head `04442fe0aac243499231b1233e0a84eff0a33ede` still failed at a second missing parenthesis in the HMAC replay test (`tests/test_gemini_transport_controller_contract.py:205`). This was found by the next exact-head compile/contract run.
- Subsequent commit `d5862c939daea07c00136600965bfb2b2336b081` corrected all three `next(...)` expression lines. On that head, workflow contract validation [39649699990](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649699990) passed, Cloud Runtime Validation [39649701394](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649701394) passed, but Astra Verify [39649700215](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649700215) failed in the cloud-admission test suite.
- Runtime test logs identified fixture bugs in `tests/test_gemini_child_signed_dispatch_runtime_contract.py`: `SIGNED_FIELDS` are lowercase payload keys while `values` uses uppercase environment names; additionally, `signed_overrides` must be uppercased before creating the signed payload, or malformed UUID/base/scope fixtures are not actually applied.
- The current PR #434 branch has since advanced to head `3bb9448d4899aa73ca1bb5b1114f68e824526c4d`; read-back confirms the fixture now maps `signed_overrides` to uppercase keys. No workflow runs were returned for this latest head at the time of this update. Exact-head CI therefore remains **PENDING / NOT VERIFIED**.
- PR #434 remains OPEN/DRAFT/UNMERGED. Do not integrate until the current head has green exact-head compile, transport contract, runtime HMAC/negative tests and all required checks.
