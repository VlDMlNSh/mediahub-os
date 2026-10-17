# MediaHub OS — Wave 122: Gemini HTTP helper CI path coverage (2026-10-18)

## Scope

Bounded contract-CI coverage repair on the Gemini read-only workflow candidate. Reviewed the exact current validation workflow and its Python contract tests, corrected the missing path filters for the shared HTTP response helper and its local regression harness, then read both files back from GitHub and inspected exact-head CI.

## Finding

The validation workflow's test job reads and checks `scripts/gemini_http_response.js` and executes `scripts/test_gemini_http_response.js`, but neither path was present in `push.paths` or `pull_request.paths`. Changes to either file alone therefore could leave the contract workflow untriggered.

## Change

- Added `scripts/gemini_http_response.js` and `scripts/test_gemini_http_response.js` to both push and pull-request path filters in `.github/workflows/gemini-readonly-workflow-validation.yml`.
- Added a regression assertion to `scripts/test_gemini_readonly_workflows.py` requiring each of those two paths to occur exactly twice in the workflow filters.
- No provider calls, credentials, secrets, dispatches, or runtime tasks were used.

## Source and commit evidence

Candidate branch: `security/gemini-readonly-hardening-20261017`.
- Final candidate HEAD for this pass: `b6ef967590a5e9cdaa4800a17e10e3c5b3ab6b66`.
- Validation workflow blob SHA: `fcbe964602bff7e03ed38632dc18066efad4d99c`; read-back length 2,571 characters; each new path appears twice.
- Contract test blob SHA: `e1f6995cad1b0fece8ce02b31d50d2f82dcfd5c3`; read-back length 11,544 characters; regression assertions are present.
- Previous validation workflow blob: `d031dfdff90e11fcd42f793cda33ce9dd038bdae`.
- Previous contract test blob: `f6acbdc6a05eae821b297df61be1aa16aad21fb1`.

## Exact-head CI

All three checks completed successfully on `b6ef967590a5e9cdaa4800a17e10e3c5b3ab6b66`:
- [Gemini Read-only Workflow Contract #39074597908](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39074597908) — actionlint and security-contract regression step succeeded.
- [Astra Cloud Runtime Validation #39074597910](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39074597910) — success.
- [Astra Verify #39074597915](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39074597915) — success.

## Live PR and governance state

- [PR #334](https://github.com/VlDMlNSh/mediahub-os/pull/334) remains OPEN / DRAFT / UNMERGED at the candidate SHA above.
- Current compare against `main`: 65 ahead / 2 behind; merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`. The prior Wave 121 finding still applies: the two commits on main after that merge base add then remove a report, yielding zero cumulative changed files when comparing that base to main. Do not treat this as a substitute for independent review or branch protection.
- No independent security approval or authorized protection/ruleset read-back is evidenced.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Next step

Run an independent security review against exact HEAD `b6ef967590a5e9cdaa4800a17e10e3c5b3ab6b66` and obtain authorized branch-protection/ruleset evidence. Keep PR #334 Draft until those gates are met; rerun required checks after any further source or base changes.
