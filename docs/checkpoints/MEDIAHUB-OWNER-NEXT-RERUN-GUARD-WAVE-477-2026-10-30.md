# Wave 477 — prevent owner /next workflow rerun redispatch (2026-10-30)

## Summary

Added a fail-closed rerun guard to the Issue #301 owner /next controller path. GitHub Actions keeps the workflow run ID across a rerun; therefore, the existing history check excluding CURRENT_RUN_ID could allow a rerun of the same owner-comment workflow run to proceed as though it were its first dispatch attempt.

For issue-comment-originated controller runs, the dispatcher now requires github.run_attempt == 1 before querying workflow-run history. Attempts 2+ or a missing/malformed attempt value stop with exit code 2 before any dispatch-related GitHub API call. Manual workflow_dispatch remains unaffected because this guard runs only when SOURCE_COMMENT_ID is non-empty.

## Immutable target / changes

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/587
- Branch: fix/next-idempotency-complete-history-wave463
- Base/main: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7
- Exact PR HEAD: 8c3f6754e3f1e5ae2a688735987466117aebb37f
- Compare to main: 6 commits ahead, 0 behind.
- Changed files:
  - .github/workflows/gemini-batch-dispatch-controller.yml — blob cf77ed19b8944657b7f029ac40a92cc9e62353f8
  - tests/test_gemini_transport_controller_contract.py — blob e5b734a44a4520a34563b1edd85e2bc8903ffb74
- Controller guard: injects CURRENT_RUN_ATTEMPT from github.run_attempt; if an Issue #301 comment-triggered run is not attempt 1, exits before history GET. It does not change the manual workflow_dispatch route.
- New regression: test_issue_comment_rerun_fails_closed_before_history_api_call. Tests attempt values missing, 0, 2 and malformed fail before API call; attempt 1 reaches the mocked history GET; incomplete history still fails closed.

## Exact-head CI evidence

All relevant workflows reached terminal success on exact head 8c3f6754e3f1e5ae2a688735987466117aebb37f:

| Workflow / evidence | Run | Job | Result |
|---|---:|---:|---|
| Gemini workflow contract validation (Wave 284) | 41017855973 | 123938151264 | SUCCESS |
| Astra Verify | 41017855994 | 123938151700 | SUCCESS |
| Astra Cloud Runtime Validation | 41017856039 | 123937753519 | SUCCESS |
| AI Factory verification | 41017856155 | 123938152189 | SUCCESS |
| provider contract verification | 41017856090 | 123938151911 | SUCCESS |
| Non-launching controller probe | 41017856138 | 123938153624 / 123938176537 | SUCCESS |

Gemini contract validation:
- actionlint: SUCCESS;
- legacy caller-context, Wave 292, reusable-workflow contracts: SUCCESS;
- controller transport tests: SUCCESS (14 tests, including the new attempt guard);
- executable child HMAC suite: SUCCESS;
- trigger-path coverage: SUCCESS.

Astra Verify:
- compile: SUCCESS;
- full unittest discovery: SUCCESS (477 tests);
- signed-command smoke: SUCCESS.

Controller probe 41017856138:
- no-secret probe / observation: SUCCESS;
- caller-context assertion: SUCCESS;
- admission guard: SKIPPED;
- dispatch_and_monitor: SKIPPED.

No Gemini child workflow, Agent 1/2/3, provider inference or secrets were invoked/read.

## Important merge qualification

The five currently active required ruleset contexts are:
1. Astra Cloud Runtime Validation
2. AI Factory verification
3. provider contract verification
4. Astra Verify
5. Gemini workflow contract validation (Wave 284)

On PR #587, the checks API currently publishes generic job names such as verify, validate, Verify AI factory policy and secret boundaries, and Verify approved executor routing boundaries. Although the corresponding workflows above succeeded, those names do not equal the five exact required ruleset contexts. Therefore the exact required-check gate on PR #587 remains NOT VERIFIED. Do not mark ready or merge on the basis of the workflow successes alone.

PR #587 remains OPEN / DRAFT / UNMERGED. Formal reviews: 0. Inline review threads: 0. Independent A3 review: NOT VERIFIED.

## Scope limits / next step

- History completeness guard still fails closed if total_count is missing or the first-page result count differs; pagination for histories larger than the queried page is not implemented. This is an availability limitation, not permission to bypass idempotency.
- This change blocks GitHub workflow reruns of the same issue-comment controller run. It does not replace a durable cross-run idempotency receipt for concurrent/separately-created duplicate events; that remains a separate control-plane requirement.
- Next: keep PR #587 Draft; align its five published check contexts with the active ruleset only through a reviewed, separately governed branch change; obtain independent A3 review; rerun exact-head required contexts before considering merge.
- No merge, deployment, qualification, or Contour A acceptance occurred. Contour A NOT ACCEPTED; Contour B GATED.

## References

- PR #587: https://github.com/VlDMlNSh/mediahub-os/pull/587
- PR #588 (separate branch for required context alignment): https://github.com/VlDMlNSh/mediahub-os/pull/588
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
