# Wave 471 — PR-scoped read-only review child (2026-10-29)

## Status

- Implementation: **PLANNED / proposed in draft PR #588**; not integrated.
- Exact-head CI: **RUNNING / NOT VERIFIED** at report creation. Astra Verify run `40843918527` was queued; no successful full CI qualification is claimed.
- Independent review: **NOT VERIFIED** (0 formal review submissions; 0 inline review threads at initial inspection).
- Agent dispatch: **NOT RUN**. The new child is not yet connected to the controller and must not be dispatched.
- Contour A: **NOT ACCEPTED**. Contour B: **GATED**.

## Immutable target and evidence

- Base `main`: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #588 head: `8ecc8941c079e83d6d1c356a0ffbaf3c73c8f70b`.
- Workflow commit: `8746936c35564ba1284b74dbd8a24cd0a8bee83c`.
- Test commit: `8ecc8941c079e83d6d1c356a0ffbaf3c73c8f70b`.
- Workflow blob SHA: `85174e24b7d213ce7d90a4bd215ec4fbac32c605`.
- Test blob SHA: `5d06c6ce0e647ca0f19ebef71400d0b2fa935a46`.
- Compare `main...feat/pr-scoped-readonly-review-wave471`: ahead 3, behind 0; exactly two files added.

## Work performed

Added `.github/workflows/gemini-pr-readonly-review-wave471.yml` as a dedicated PR-scoped child; did not modify or reuse the FCC-specific child. The workflow contract requires a numeric PR number, UUIDv4 correlation ID, immutable base/head SHA, fixed task, and HMAC signature. It validates repository and dispatch ref, signature, PR open state, base `main`, exact base/head SHA equality, and same-repository PR head before model credentials are referenced. It then checks out the immutable head without persisted credentials, computes the exact base..head diff, writes a manifest and changed-file list, invokes Gemini with read-only file tools, and uploads review inputs/provenance.

Added `tests/test_gemini_pr_readonly_review_wave471_contract.py` with static structural assertions. This is not behavioral testing and does not prove the GitHub API/HMAC runtime path works.

## Explicit limitations / safety gates

1. The controller does not yet generate/sign the new payload or dispatch this child. Do not manually dispatch it. Integration is a separate step and must verify current PR metadata immediately before signing/dispatch.
2. Behavioral tests are still needed for malformed PR numbers, wrong/changed base and head SHA, invalid HMAC, duplicate requests, inaccessible PR, and rejected/ambiguous dispatch.
3. Review artifact digest/run/job provenance must be independently verified before the result can be treated as accepted review evidence.
4. Exact-head CI and independent review are pending. Do not merge or mark qualified.

## Next step

Review CI results on exact head `8ecc8941c079e83d6d1c356a0ffbaf3c73c8f70b`. Fix any YAML/contract/test failures. Then add behavioral tests and a narrowly scoped controller path that signs and dispatches PR number + base SHA + head SHA, with duplicate/idempotency handling and reconciliation of ambiguous dispatch outcomes. Require independent review before enabling the route.

## Links

- PR #588: https://github.com/VlDMlNSh/mediahub-os/pull/588
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
