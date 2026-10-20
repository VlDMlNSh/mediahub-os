# MediaHub OS — Wave 278: worker secret-gate regression restoration

- Date: 2026-10-20
- Status: **PATCH PROPOSED IN DRAFT PR / SOURCE READ-BACK VERIFIED / TEST EXECUTION NOT VERIFIED**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Triggering audit: [Wave 277 tree-drift and A0 authority crosswalk](MEDIAHUB-CONTOUR-A-TREE-DRIFT-AND-A0-AUTHORITY-CROSSWALK-WAVE-277-2026-10-20.md)
- Proposed change: [Draft PR #424](https://github.com/VlDMlNSh/mediahub-os/pull/424)

## Finding and evidence

The exhaustive tree comparison in Wave 277 identified that `ops/qualification/run_distributed_local_worker.py` differed by one source line between main and the documentation ref:
- `main` blob: `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`
- previous documentation blob: `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`

The main expression uses actual whitespace escapes, `\s*`, to detect assignments such as API-key or bearer-token labels followed by `:` or `=`. The docs version over-escaped the pattern (`\\s*` in the raw regex) and therefore expected literal backslash-plus-s characters rather than ordinary whitespace. This was confirmed by a source-line diff; no tests were executed in this pass.

The docs tree also lacked `tests/test_worker_security_gate.py`. The main version is blob `53098d1755518bc9fcd67a2236d874534aeb8fd5` and contains mock/temp-file tests for API key assignment, bearer token assignment, PEM private-key marker detection, and allowing ordinary non-secret text.

## Bounded change

Draft PR #424: https://github.com/VlDMlNSh/mediahub-os/pull/424
- Base: `docs/mediahub-chat-tree-map-20261012`, base SHA observed when opened: `7349fbf0b94d0accab8593bbdf57a0c7c62a5cc3`.
- Head: `contour-a/fix-docs-worker-secret-regex-wave278`, `1538eb2c11f0336186fec0962dec7896a73cab7b`.
- Changed paths only: `ops/qualification/run_distributed_local_worker.py` and `tests/test_worker_security_gate.py`.
- Read-back confirmed the patched worker's regex line now has the same blob SHA as the main worker (`dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1)); the restored test file's SHA equals the main source (`53098d1755518bc9fcd67a2236d874534aeb8fd5`).
- PR is OPEN / DRAFT / UNMERGED; no submitted reviews were returned. `fetch_commit_workflow_runs` returned no workflow runs for this exact PR head at the time of the check. That means CI is **not yet evidenced here**, not that it failed or passed.

## Scope and safety

This is a narrowly scoped fix to the canonical documentation branch's source/test mirror; it does not change `main`, resolve general branch drift, or authorize a broad rebase. No host/provider/secret operation, workflow dispatch, merge, deployment, release, qualification or acceptance occurred. The regression fix is proposed, not integrated.

## Next gates

1. Inspect exact-head Actions/check status for PR #424; run the restored tests in the repository's supported CI environment.
2. Obtain independent review of the two-file patch.
3. Merge only into the documentation ref if required checks and review pass; any promotion to `main` is a separate source-reviewed decision.
4. Preserve main-only transport files and do not mix this PR with the two-workflow retirement proposal (#423) or Gemini controller proposal (#421).

Contour A remains NOT_PROVEN / BLOCKED; Contour B remains gated on deployment and independent acceptance of Contour A.
