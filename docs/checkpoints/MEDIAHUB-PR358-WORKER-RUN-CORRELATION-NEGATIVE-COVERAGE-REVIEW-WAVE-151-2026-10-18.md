# MediaHub OS — PR #358 worker-run correlation negative-coverage review, Wave 151

- Date: 2026-10-18
- Status: **EXACT-HEAD CI PASS / NARROW CORRELATION FIX VERIFIED / SECURITY AND QUALIFICATION GATES OPEN**
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Candidate: [PR #358 — Fail closed on ambiguous distributed worker run correlation](https://github.com/VlDMlNSh/mediahub-os/pull/358)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Ref and workflow evidence

- Main HEAD observed: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- PR #358 head: `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`; base: `main`; GitHub reports open, Draft, mergeable=true.
- Astra Verify run [39117896120](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117896120), job `verify` ID `117647309406`, completed successfully.
- Exact job log confirms the full suite: `Ran 429 tests ... OK`; dedicated correlation suite: `Ran 7 tests ... OK`.
- Astra Cloud Runtime Validation run [39117895925](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117895925) completed successfully.
- Test file blob SHA at candidate head: `8f57133b7afe14415adf9a6e629cfae44316ae77`.

## 2. What the code and tests establish

The change replaces substring title matching with exact matching of the command/task/node/executor title, requires a parseable timezone-aware `createdAt` not older than the dispatch start, validates a positive integer `databaseId`, and fails closed on multiple exact fresh matches. It validates command/task/node identifier shape and currently supports only executor `claude`. The docstring explicitly says run-title metadata is correlation only, not authorization.

Seven dedicated tests pass for: one exact fresh match, empty command ID, substring collision, stale run, duplicate exact runs, zero run ID, and unsupported executor.

## 3. Remaining negative-coverage gaps

The source rejects several invalid inputs for which the dedicated tests do not yet have direct cases:
- malformed (non-empty) command ID; invalid task ID and node ID;
- malformed timestamp, timezone-naive timestamp, and malformed row shape;
- boolean `databaseId` (Python's `bool` is an `int` subclass and production code explicitly rejects it);
- exact-title candidate with invalid run ID alongside a valid candidate.

These are test-coverage gaps, not observed functional failures. Add compact table-driven negative cases before calling the helper fully regression-covered.

## 4. Security boundary — still not proven by this PR

The helper correlates a run but does not authenticate it. Before any worker result can be trusted, the caller must independently verify GitHub-derived workflow identity, event type, source SHA, job/attempt/artifact provenance and the signed A0 command envelope, under the accepted issuer/authority contract. Run title, freshness and uniqueness are not substitutes for authorization or provenance.

The WB-05 issuer-owner choices and R-06 audit/privacy decisions remain unresolved in the canonical governance record. This pass does not infer or create those decisions.

## 5. Disposition

- Keep PR #358 Draft while the remaining trust/provenance and governance gates are open. Although GitHub currently reports mergeable=true and both workflows pass, that does not establish acceptance of the end-to-end worker path.
- No production code, tests, credentials, provider calls, dispatch, deployment, merge, rebase, or qualification were changed/performed in this review.
- Docs branch remains divergent from main; do not merge the documentation branch wholesale. Record this report through the canonical map navigation.

**Next bounded step:** add the missing pure unit-test cases on the PR branch, rerun both workflows at the resulting exact HEAD, then separately review the caller's post-run provenance and signed-envelope checks. Keep Contour A **NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED** and Contour B gated.
