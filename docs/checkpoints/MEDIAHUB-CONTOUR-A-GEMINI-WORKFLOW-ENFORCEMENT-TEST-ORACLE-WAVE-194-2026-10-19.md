# MediaHub OS Contour A — Gemini workflow enforcement test oracle (Wave 194)

- Date: 2026-10-19
- Scope: bounded follow-up to Wave 193; define observable acceptance tests for the workflow mutation boundary and check whether governance approval is evidenced.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous report: [Wave 193](MEDIAHUB-CONTOUR-A-GEMINI-POST-RUN-VALIDATION-BOUNDARY-AUDIT-WAVE-193-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- PR #376: https://github.com/VlDMlNSh/mediahub-os/pull/376

## Baseline evidence

- `main` HEAD remains `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation branch HEAD before this wave: `c275365974517901615c859d4d5133b94e254fb8`.
- Issue #301 is open. PR #374, #375 and #376 are open Draft/unmerged.
- Issue #301 comments were reread; latest relevant documented evidence remains Wave 192 comment `6265270600`. No later governance approval for workflow mutation-boundary changes was found in the retrieved comments. This is an evidence-bound observation, not proof that no decision exists elsewhere.
- Previous exact-head CI for PR #376 passed at SHA `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`; no new CI was run for this documentation-only wave.
- Source blobs and the source-level findings are listed in Wave 193.

## Proposed test oracle (not implemented or approved)

The workflow candidate must fail closed if any of these cases occurs:

1. PR base differs from the single approved base, even if PR creation call counter reports success.
2. Head branch fails the approved prefix/identity policy.
3. Changed file is outside the explicitly approved path set, including mixed allowed/disallowed changes.
4. The agent attempts direct content mutation against a protected/default ref; broker/server policy must reject the write before mutation.
5. PR metadata lookup fails, returns missing fields, or references an unexpected repository/number.
6. PR has no changes, unexpected commit ancestry, or does not match the branch/ref used for the task.
7. The tool response says PR creation succeeded but the PR cannot be fetched or the returned metadata disagrees.
8. Gemini returns malformed/missing stdout, no successful tool calls, or no successful PR creation; the validation gate must run deterministically and the job must finish non-successfully.
9. A validation step itself fails; the overall workflow must not report success.
10. A task prompt requests broader scope than the server-side capability allows; the write boundary must deny it regardless of prompt wording.

For each case, record the precondition, attempted mutation, authoritative observed GitHub state, expected deny/allow outcome, and CI run tied to the exact candidate SHA. A mock/unit test of parsing alone is not sufficient evidence of server-side enforcement. Never exercise a destructive direct-write case against a real protected ref; use a mock or isolated disposable repository.

## Decision and blocker

The retrieved issue discussion does not show approval of the proposed broker/validation contract. Therefore this wave does not change workflow YAML, permissions, tests, or production behavior and does not dispatch Gemini. Governance/security review remains a prerequisite. Branch protection/review settings remain unverified due to the previously observed API 403. Immutable action/container provenance, including exact MCP OCI digest, remains unresolved.

## Next action

Obtain a recorded independent security/governance decision on the proposed enforcement contract. Once approved, implement the smallest isolated candidate with brokered ref/path enforcement and PR metadata validation, then add the above negative/failure-path tests. Pin dependencies only after provenance verification. Do not promote PR #376 or dispatch Gemini based on static parity CI alone.

No secrets accessed, no tests run, no workflow dispatch, no host commands, no merge/deploy/qualification. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
