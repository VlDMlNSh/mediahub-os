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


## Follow-up fixture failure found by Astra Verify

After the syntax errors were corrected, Astra Verify reached the child authorization runtime tests and found a second independent test-harness defect: `make_environment()` declared lowercase canonical signed fields (`workflow_file`, `dispatch_id`, etc.) but indexed a dictionary containing uppercase environment names (`WORKFLOW_FILE`, `DISPATCH_ID`, etc.). This caused KeyError before the negative event/ref assertions could execute. The fixture was corrected to build the canonical signed payload from the uppercase runtime environment values and to map lowercase signed overrides onto their corresponding environment fields.

- Failing evidence: Astra Verify [#39649630775](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649630775), job `119394233707`; the run reported 460 tests with 46 errors, all rooted in missing `workflow_file` key.
- Latest PR #436 head observed: `95080b43782f9464f05869f08cf7a9f47680a233`.
- Fixture blob: `dd9bc5cd3c917414fe55f9d439428f6496e2429d`; transport test blob remains `01ddae5e1d7fd0e49ffa651da9655a5a5ad7a8d5`.
- GitHub Actions query and commit-check API returned no runs/checks for latest head at the time of this update. Therefore no CI result is available for the latest candidate; this is **NOT VERIFIED**, not a pass. Earlier exact-head checks on intermediate commits do not qualify the latest head.


## Wave 322 — HMAC regression test fixture repair and automation readiness (2026-10-21)

### Verified state
- Current \`main\` HEAD: \`79196054d84b1197cea1447dd1db5ad075302834\`. Commit message: \`fix: repair Gemini HMAC contract tests\`; it corrects Python compilation and maps canonical signed-field test overrides to the expected environment names. Exact-main Astra Verify run [#39649841150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649841150) is SUCCESS.
- Candidate PR #437 remains Draft/open at \`7f491729bab024a72dc20f5d7a3e107a4393ba3b\`, not merged. Its exact-head contract validation [#39649822358](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649822358), Astra Verify [#39649822366](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649822366), and Cloud Runtime Validation [#39649822570](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649822570) all passed. PR adds executable, secret-free HMAC tests against the three child authorization scripts. No formal review was returned by the review-list check.
- On the latest PR #437 branch, the fixture maps \`workflow_file\`, \`dispatch_id\`, \`target_sha\`, \`task\`, \`base_ref\`, and \`scope\` to the corresponding environment keys before recomputing the test signature. This fixes a false-positive test fixture that had left invalid signed overrides unapplied. The runtime test is synthetic only and does not read repository/provider secrets or dispatch agents.
- Current main controller blob: \`9453403bba899a2400ee3fb874d32badd034c704\`. It includes the owner-only Issue #301 \`/next\` comment bridge, duplicate-comment suppression and \`MEDIAHUB_GEMINI_BATCH_ENABLED\` fail-closed admission. Three task prompts are distinct: bounded implementation, independent contract/test verification, and security/provenance audit. Controller source and runtime test blob were re-read.

### Qualification boundary
- Gemini dispatch: **NOT RUN**. A successful test run does not prove that the HMAC secret and repository variable are configured correctly, nor does it satisfy independent security review, trusted-main no-secret probe, branch protection/governance, or runtime provenance gates. Repository secret values were not accessed. Secret/variable metadata access was not established in this pass.
- Claude on Alamo and browser inspection: **NOT RUN**. SentinelX inventory still exposes only the operational host \`Voktors-Mini.Dlink\` (\`host_5f7264034bdf0b51\`); no host is identified as Alamo/server 3. Do not route Gemini through Alamo.
- No controller workflow-dispatch was triggered. The admission flag is not enabled by this pass. PR #437 remains Draft until independent review and the residual gates are resolved.

### Next step
Independently review PR #437's HMAC canonicalization and child-side fail-closed behavior, verify branch protection and required checks, establish secret/variable presence without reading values, and prove trusted-main non-launching caller context. Only then decide whether the batch admission flag may be enabled. Keep Gemini and Claude routes separate.


### Concurrent branch advance after Wave 322 verification
- PR #437 advanced after the three successful CI runs from \`7f491729bab024a72dc20f5d7a3e107a4393ba3b\` to \`531ed07d1fd8ad474587f5af0e4a5f3364461b6d\` with a further test-only guard rejecting unsupported signed fixture override fields. At the latest check, no workflow runs were yet listed for this new head. Therefore the three green checks are evidence for the previous exact head only, not qualification of the latest PR head.
- PR #437 remains Draft/open/unmerged. Keep its status distinct: prior head CI VERIFIED; latest head PLANNED/UNVERIFIED pending exact-head CI. Main remains \`79196054d84b1197cea1447dd1db5ad075302834\`.


## Superseding state check — fix landed on main outside PR #436 (2026-10-21)

A subsequent ref check supersedes the earlier “latest candidate lacks checks” snapshot. PR #436 was closed unmerged at 18:11:05Z. Main advanced to `79196054d84b1197cea1447dd1db5ad075302834`, whose commit message is `fix: repair Gemini HMAC contract tests`. The main test blobs now contain the syntax and signed-field mapping repairs:

- `tests/test_gemini_transport_controller_contract.py`: blob `01ddae5e1d7fd0e49ffa651da9655a5a5ad7a8d5`; all three HMAC `next(...)` expressions were read back with balanced closing parentheses.
- `tests/test_gemini_child_signed_dispatch_runtime_contract.py`: blob `64d55eb2a78dd1ea015dae80a838dc44ad592f7e`; it now maps canonical signed field names to uppercase runtime environment keys and applies signed overrides through that mapping.
- Exact-main Astra Verify succeeded: [run #39649841150](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39649841150), whose reported SHA is `79196054d84b1197cea1447dd1db5ad075302834`.
- The commit/check API returned no combined statuses and no associated PR workflow runs for this SHA, so **exact-main workflow-contract validation is not independently confirmed** by the current evidence. The commit message cites prior PR-head checks, but those are not a substitute for post-merge exact-main checks.

This resolves the syntax and fixture regressions at source level, but does not qualify the controller. PR #432 remains merged without a formal submitted review in the review listing; branch protection/governance API access remains blocked. Gemini children, Claude/Alamo and browser work remain NOT RUN. The batch gate must remain closed until exact-main contract validation, independent security review, effective governance verification and trusted-main no-secret probe are evidenced.
