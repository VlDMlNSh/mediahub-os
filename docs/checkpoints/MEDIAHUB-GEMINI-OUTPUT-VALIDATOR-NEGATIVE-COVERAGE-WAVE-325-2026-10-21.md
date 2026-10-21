# Wave 325 follow-up — Gemini child output-validator negative coverage (2026-10-21)

## Disposition

**TEST IMPLEMENTATION COMMITTED TO DRAFT PR #437; EXACT-HEAD CI NOT VERIFIED.** This follow-up adds secret-free regression coverage for the output-validation shell scripts embedded in all three Gemini child workflows. It does not claim tests passed, does not dispatch Gemini, and does not qualify the transport.

## Source and commit evidence

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Existing implementation PR: https://github.com/VlDMlNSh/mediahub-os/pull/437
- Commit: https://github.com/VlDMlNSh/mediahub-os/commit/e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14
- Changed file: `tests/test_gemini_child_signed_dispatch_runtime_contract.py`
- Read-back blob SHA: `43016c501e80ea665e6707f7e2381e9918aededc`
- PR head after update: `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`

## Change

The new unittest extracts the actual `Validate Gemini produced an actionable PR result` shell step from each child workflow and executes it with synthetic temporary files. It checks:
- valid non-empty JSON with successful tool and PR-creation calls is accepted;
- missing output is rejected;
- malformed JSON is rejected;
- blank response is rejected;
- no successful tool call is rejected;
- no successful PR-creation call is rejected.

The fixture uses no repository or provider secrets and performs no network/provider/model requests. The existing Wave 284 contract-validation workflow explicitly includes this test file and its path filter, so a normal PR-triggered validation run should include it if the workflow event is actually admitted.

## Verification and limits

- GitHub read-back confirmed the commit, PR head and blob SHA above.
- The PR's changed-file list confirms the test is included alongside the contract workflow and transport test.
- Immediately after the update, the PR-only workflow-run connector returned an empty list for the new commit and combined status returned no statuses. Therefore **CI remains NOT VERIFIED**. This connector only returns PR-triggered runs; an empty result is not exhaustive evidence about other event types.
- Local execution was not possible in this environment because outbound DNS resolution for github.com failed and no repository checkout was available. No passing-test claim is made.
- PR #437 remains Draft/open/unmerged; the formal review list remains empty and mergeability is false in the latest PR snapshot.
- No controller or child workflow was dispatched; Gemini Agents 1–3 are NOT RUN. No secret values were accessed.

## Next bounded action

Obtain a real exact-head contract-validation run for `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14` and inspect job logs. If the update did not trigger checks, diagnose the repository's Actions event/permission configuration rather than treating empty status as green. Then obtain independent security review and verify the remaining admission gates before any controller dispatch.
