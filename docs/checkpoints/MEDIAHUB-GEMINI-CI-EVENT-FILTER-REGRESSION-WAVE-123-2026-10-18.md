# MediaHub OS — Wave 123: precise Gemini CI event-filter regression (2026-10-18)

## Scope

Bounded follow-up to Wave 122. Reviewed the newly added path-filter assertion and tightened it so each helper/test path must appear exactly once in each individual event block, rather than merely twice across the whole workflow. Re-read exact files and checked all CI runs for the resulting code HEAD.

## Finding and change

Wave 122 required the HTTP helper and test paths to appear twice in the contract workflow, which normally represented one entry in `push.paths` and one in `pull_request.paths`. A total-count assertion could nevertheless pass if both entries were accidentally duplicated in one event and omitted from the other.

The regression now isolates the `push:` and `pull_request:` sections and asserts, for each of:
- `scripts/gemini_http_response.js`
- `scripts/test_gemini_http_response.js`

that the exact path entry appears **once in push** and **once in pull_request**.

## Exact source evidence

- Code branch: `security/gemini-readonly-hardening-20261017`.
- Final HEAD: `16b3b2ee73bc12ac213818cf0ad22abedafd50ad`.
- Updated test blob SHA: `b130261a2c12608614780a1ab2f8f05483e1180e`; read-back length: 11,824 characters.
- Validation workflow blob SHA remains `fcbe964602bff7e03ed38632dc18066efad4d99c`; read-back length: 2,571 characters. Each helper/test path is present in both event path filters.
- The final Python assertion block was re-read from GitHub. The workflow file and test file were read back after the write.

## Exact-head CI

All three runs completed successfully on `16b3b2ee73bc12ac213818cf0ad22abedafd50ad`:
- [Gemini Read-only Workflow Contract #39074978642](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39074978642) — actionlint, immutable checkout SHA verification and security-contract regression tests succeeded.
- [Astra Cloud Runtime Validation #39074978634](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39074978634) — success.
- [Astra Verify #39074978856](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39074978856) — success.

The run/job records show the contract test and both generic validation jobs completed successfully. Combined commit status was empty, so workflow-run records are the evidence; no branch-protection conclusion is inferred.

## PR and governance state

- [PR #334](https://github.com/VlDMlNSh/mediahub-os/pull/334) remains OPEN / DRAFT / UNMERGED at `16b3b2ee73bc12ac213818cf0ad22abedafd50ad`.
- Latest compare previously observed: 65 ahead / 2 behind `main`, merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`. The two behind commits have a zero cumulative tree delta, but history remains divergent.
- Existing review submissions are source-bound COMMENTs by the repository owner, not independent security approval. No independent reviewer approval or authorized branch-protection/ruleset read-back is evidenced.
- No provider/model invocation, secret access, manual dispatch, queue admission, merge, deployment, or acceptance occurred.
- Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED**.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Next step

Obtain independent security review of exact HEAD `16b3b2ee73bc12ac213818cf0ad22abedafd50ad` and authorized branch-protection/ruleset evidence. Keep PR #334 Draft until those gates are evidenced; rerun required checks after any further code or base change.
