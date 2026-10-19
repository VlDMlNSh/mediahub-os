# MediaHub OS Contour A — Gemini workflow parity tests (Wave 183)

- Date: 2026-10-19
- Status: one-file test candidate opened as Draft PR #376; CI was still running at the observation timestamp.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior source audit: [Wave 182](MEDIAHUB-CONTOUR-A-GEMINI-WORKFLOW-SUPPLY-CHAIN-AND-DISPATCH-AUDIT-WAVE-182-2026-10-19.md)
- Runner/Gemini readiness: [Wave 181](MEDIAHUB-CONTOUR-A-RUNNER-MANIFEST-AND-GEMINI-POOL-READINESS-WAVE-181-2026-10-19.md)
- Governing issue: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Change made

Created `tests/test_gemini_workflow_parity.py` on branch `codex/wave-183-gemini-workflow-parity-tests`. The test module adds static regression checks for:
- existence of the three manual Gemini workflow definitions and distinct secret references;
- manual dispatch, required task/base/scope input markers, hosted runner selection, 30-minute timeout, and `persist-credentials: false`;
- exact, ordered GitHub MCP tool allowlist parity;
- documented no-merge/no-deploy intent and artifact-output validation setup;
- a finding detector for currently mutable action and MCP container references (3 per workflow, 9 total).

The tests intentionally do not claim that secrets are configured, a model can be called, the workflow has run safely, or any qualification gate has passed. They do not change workflow permissions, action refs, container refs, credentials, or governance policy.

## 2. GitHub evidence

- PR: [#376 — Draft: add Gemini workflow parity checks (Wave 183)](https://github.com/VlDMlNSh/mediahub-os/pull/376)
- Branch head/commit: `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`
- Test file blob after read-back: `a65796d5d8ae258b26b95a9fe8a50d1b06382fd0`
- Base branch SHA: `c06015e0b1526e0aaa6a522306052b077455aba5`
- PR created at 2026-10-19T09:34:36Z, one file changed, 96 additions.
- Read-back confirmed the file exists and contains the parity class and mutable-reference detector.
- At the last check, two CI jobs were `in_progress`: [validate](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39231107098/job/117988998804) and [verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39231107074/job/117988998688). Do not treat them as passed until final conclusions are fetched.

## 3. Scope and security boundary

This is a Draft PR and is not merged. No Gemini workflow was dispatched, no provider API was invoked, no secret was read, no SentinelX host command was run, and no test was executed manually in this session. CI is the first execution of this test candidate and its result must be independently checked.

The test codifies present workflow invariants, including current mutable-reference findings; it does not resolve the supply-chain issue. The next separate remediation should pin actions and the MCP image only after trusted upstream commit/digest and provenance are verified. Keep the manual dispatch and least-authority review boundary; do not enable persistent scheduling or self-hosted dispatch as a workaround for offline hosts.

## 4. Current qualification truth

The latest observed `docs/qualification/CURRENT-TRUTH.generated.md` remains blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`, with ASTRA GOLD G0–G11 blocked and overall NOT_PROVEN / BLOCKED. PR #374 and #375 remain open Draft candidates; PR #376 is also Draft. SentinelX has zero connected hosts; the Mac mini is offline and `mh-dev-01`/`mh-dev-02` are user-disabled. Codex Tasks currently has no registered remote environments.

## 5. Next step

Fetch final CI results for PR #376. If both checks pass, retain Draft and request independent review of test quality; if a check fails, use the exact logs to correct the test in a follow-up commit. Only after the workflow parity test is accepted should a separate immutable-reference remediation PR be prepared from verified upstream evidence. Continue to treat issuer, trusted publisher, live runner, and independent acceptance as separate Contour A blockers.
