# MediaHub Contour A — Wave 231: signed-command verifier proposal

- Date: 2026-10-20
- Status: **PROPOSED / ISOLATED / NOT AN EXECUTION ADMISSION GATE**
- Branch: `work/contour-a-command-verifier-wave231`
- Base `main` SHA at start: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Change

Added `verify_signed_command()` to `ops/control/sign_command.py`. The proposed pure verifier:
- checks required command shape and freshness;
- rejects unknown fields and malformed HMAC-SHA256 signatures;
- uses `hmac.compare_digest` for signature verification;
- binds the command to separately supplied expected node, operation and target commit SHA;
- requires workflow-only commands;
- rejects unsafe, duplicate, or unauthorized owned paths;
- documents that key resolution, expected bindings and allowed paths must come from authenticated policy context, never from model/command claims.

Added `tests/control/test_verify_signed_command.py` with positive and negative coverage for valid admission context, payload tampering, wrong node/operation/target, unapproved path, traversal, unknown fields, missing signature, and stale commands.

## Verification

- Focused signer + verifier tests: **15 passed**.
- `py_compile`: passed.
- `git diff --check`: passed.
- Full suite using the declared development dependencies in an isolated `/tmp/mediahub-wave231-venv`: **506 passed, 2 failed**.
- The two failures are in untouched existing surfaces:
  1. `tests/test_distributed_local_worker.py::test_23wave_codex_qualification_is_not_unbounded` expects `--sandbox workspace-write` in `.github/workflows/mh25-dual-local-23wave.yml`.
  2. `tests/test_distributed_local_worker.py::test_distributed_selection_allows_one_claim_per_executor_lane` expected the Codex lane in a distributed-selection result, but got only the two Claude lanes.
- These two failures were observed on the working branch. A separate baseline execution was not completed, so do not label them conclusively pre-existing.

## Security limits / next gates

- This is a standalone verifier proposal; the worker does **not** call it yet.
- The verifier does not implement issuer authentication, capability/policy evaluation, key rotation/revocation, replay ledger, command cancellation, or an independently authorized publisher.
- The `allowed_paths`, expected node/operation/target and key are trusted inputs only if supplied by an authenticated caller. This function does not create that authority.
- No worker was dispatched, no secret values were read, no workflow permissions were changed, and no merge/deployment/gate promotion occurred.
- The existing worker's direct Git commit/push path remains a SEV-1 blocker.

## Next step

Review the verifier API and negative tests independently. Then define issuer/capability/key-lifecycle and replay semantics under governance before any execution-path integration. Keep the production worker disconnected until those authority inputs and the artifact-only publisher boundary are accepted.

Contour A remains **NOT_PROVEN / BLOCKED**; G0–G11 remain blocked and G11 is human-only.
