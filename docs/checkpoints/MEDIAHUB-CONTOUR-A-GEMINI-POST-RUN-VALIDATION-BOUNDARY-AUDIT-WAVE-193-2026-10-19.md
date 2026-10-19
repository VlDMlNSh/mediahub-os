# MediaHub OS Contour A — Gemini post-run validation boundary audit (Wave 193)

- Date: 2026-10-19
- Scope: source-level review of the three Gemini workflows and PR #376's static parity test. Documentation-only; no implementation edits or test execution.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous readiness report: [Wave 192](MEDIAHUB-CONTOUR-A-PR-376-EXACT-HEAD-CI-AND-INTEGRATION-READINESS-WAVE-192-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- PR #376: https://github.com/VlDMlNSh/mediahub-os/pull/376

## Frozen refs

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical docs branch before Wave 193: `ec0641f59e8ee417eb014371df9205c150e31cb6`.
- `.github/workflows/gemini-autonomous-engineering.yml`: blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d`.
- `.github/workflows/gemini-agent-2.yml`: blob `259c8c82b8d90a39e1c90e65390e469b241b5581`.
- `.github/workflows/gemini-agent-3.yml`: blob `91b5397001e088dfae2f450ee77c9c23118b5601`.
- PR #376 head: `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`; single added file `tests/test_gemini_workflow_parity.py`.
- PR #376 exact-head checks previously verified successful: Astra Verify run `39231107074`, Astra Cloud Runtime Validation run `39231107098`. This wave did not rerun CI.

## Findings

1. All three workflows grant job-level `contents: write`, `pull-requests: write`, and `issues: read`, despite a read-only top-level permissions stanza. Their only explicit GitHub MCP tools are branch creation, create/update file, PR creation, and file read. This is a constrained tool surface, but it is not a server-enforced allowed-path/allowed-ref policy.
2. The prompt asks Gemini to create a dedicated branch and PR against the selected base, and forbids merge/deploy. These are prompt instructions, not enforcement at the GitHub mutation boundary.
3. The post-run shell validation checks that the stdout artifact exists, parses as JSON, contains a non-empty response, reports at least one successful tool call, and reports a successful `create_pull_request` call. It does not retrieve the resulting PR to verify base ref, branch prefix, changed paths, draft status, or whether any direct write targeted a protected ref.
4. The parity test in PR #376 asserts workflow text and detects nine mutable dependency references. It does not assert that post-run PR metadata is checked or that mutation authorization is constrained by a broker. A passing parity test therefore does not prove the workflow's effective write authority is bounded.
5. Each workflow sets `continue-on-error: true` on the Gemini step and the validator is gated by `if: success()`. Source review alone does not establish the precise runner outcome for every failure path; add an explicit failure-path test/experiment in an authorized isolated candidate before relying on that interaction.
6. The workflow allows an arbitrary task string. The prompt says task text is untrusted, but this alone is not a capability/issuer decision. Dispatch must remain disabled until the governance decision and server-side controls are explicit.

## Proposed acceptance contract (not approved or implemented)

- Use a broker or equivalent server-side mutation boundary with an allowlisted branch prefix, exact allowed base, allowed path set, and no direct writes to protected refs.
- After PR creation, fetch PR metadata and fail closed unless base, branch naming, changed paths, and expected status meet policy; do not trust tool-call counters as evidence of correct output.
- Keep job permissions at the minimum required by the chosen broker design; document why each permission exists and how the token is scoped.
- Add tests for wrong base, unexpected branch, disallowed file path, empty change, direct protected-ref write attempt, malformed/missing PR metadata, Gemini step failure, and validator execution on every relevant failure path.
- Pin actions and container image by immutable, provenance-verified references; exact MCP OCI digest/provenance remains unresolved.
- Preserve separate approval for governance protocol changes and separate human/independent acceptance authority. Passing CI is not qualification.

## State and next action

Issue #301 remains open. PR #374/#375/#376 remain Draft/unmerged. Branch protection API previously returned 403, so protection/review settings are unverified. SentinelX currently has zero connected hosts; the Mac mini is offline and two development hosts are user-disabled. Codex Tasks has no registered environments. No Gemini dispatch, secret access, test execution, host command, merge, deployment, or qualification occurred.

Next: request independent governance/security review of this explicit acceptance contract; only after approval should a small isolated remediation candidate implement the server-side mutation/PR validation boundary and failure-path tests. In parallel continue exact MCP OCI digest/provenance verification. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
