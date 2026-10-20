# Wave 248 — worker/publisher boundary review with exact source references

- Date: 2026-10-20
- Status: **SOURCE REVIEW COMPLETE; IMPLEMENTATION/QUALIFICATION NOT COMPLETE; CONTOUR A NOT PROVEN / BLOCKED**
- Main HEAD audited: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`
- Worker blob SHA: `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`
- Workflow blob SHA: `f650f2416c19dc75b4a0eeec037661c0c6169910`
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Governance issue #378: https://github.com/VlDMlNSh/mediahub-os/issues/378
- Parent issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md

## Findings

### P0 — worker owns publication authority (verified)
In `ops/qualification/run_distributed_local_worker.py`:
- Lines 64–74: `load_task()` parses `ASTRA_MICRO_TASK_JSON`, verifies object type and required fields only. There is no cryptographic issuer/signature verification, capability evaluation, expiry, revocation or replay ledger in this function.
- Lines 387–401: worker reads `ASTRA_COMMAND_ID`, checks node/executor and a 40-character target SHA, and requires checkout HEAD to match. A matching SHA binds the workspace to a revision; it does not authenticate who issued the task or whether it is authorized.
- Lines 411–412: worker creates its own task branch.
- Lines 663–680: worker stages all changes with `git add -A`, commits, pushes directly to `origin`, and checks the remote branch SHA. The remote SHA check proves the pushed branch matches the local commit; it does not establish approval by a separate authority.
- Line 695: evidence digest is computed over a JSON serialization of the worker record. This is a content digest, not a signature or tamper-resistant external audit record.

### P1 — ambient environment inherited (verified)
- Lines 116–124: `start_fcc()` starts from `os.environ.copy()` before adding values from the local FCC env file.
- Lines 176–218 (including line 197): `exec_claude()` similarly copies the process environment and then injects FCC/model transport values. The worker therefore does not use a strict allowlisted subprocess environment.
- This review did not read secret values or inspect host files. Whether a specific secret is present in the workflow process environment is not asserted.

### P1 — workflow credential controls help, but are not the publisher boundary (verified)
On `main`, `.github/workflows/astra-distributed-local-worker.yml`:
- Lines 34–35 grant workflow-level `contents: write`.
- Lines 56, 97 and 138 set checkout `persist-credentials: true`.
- The workflow executes the worker in each selected self-hosted job (first occurrence line 67). The worker itself uses Git publication commands above.

PR #375 changes workflow-level permissions to `contents: read` and changes all three checkouts to `persist-credentials: false`. Its added regression tests parse YAML and test the workflow's declared permission/checkout policy. Exact-head CI for PR #375 is green (Astra Verify run 39295373907; Cloud Runtime Validation run 39295373833). Those tests do not remove worker-side `git add/commit/push`, authenticate the task issuer, validate a signed manifest, or prove an isolated publisher exists. Do not infer those properties from green CI.

### P1 — path/security gates are not a complete artifact contract (verified)
- `scope_paths()` begins at line 235; `security_gate()` begins at line 354. The current code checks declared boundary/forbidden roots and scans selected regular files for a small set of secret patterns.
- Source review did not find a signed, strict artifact manifest that rejects path traversal, symlink escapes, duplicate manifest keys, mode/type abuse, oversize artifacts, digest mismatch, stale base refs, or unapproved path sets before a separate publisher acts. These are gaps in the reviewed worker path, not a claim that no other repository component can ever implement such checks.

## Minimum safe architecture proposal (not implemented)

1. Worker receives a verified immutable task envelope and a read-only source snapshot. Validate issuer, capability/scope, expiry, revocation and replay **before** model execution; fail closed.
2. Worker writes only a bounded artifact bundle plus manifest. It has no Git push credential and no branch-publication API. Use a strict path allowlist and reject symlinks/traversal, duplicate keys, non-regular files, unexpected modes, oversized files and digest/base-SHA mismatches.
3. A separate trusted publisher independently validates issuer/capability and artifact manifest, re-checks current base SHA and allowed paths, then creates a candidate branch/PR with a narrowly scoped GitHub App or equivalent short-lived credential. It never merges automatically.
4. Emit audit evidence to an independently controlled append-only sink. A worker-computed SHA alone is insufficient for tamper resistance.
5. Add negative tests for forged/expired/revoked/replayed envelopes, missing/invalid capabilities, base SHA drift, path escape/symlink, duplicate manifest keys, secret leakage, oversized artifacts, changed permissions, remote SHA mismatch, and proof that worker credentials cannot push.

## Governance and qualification

Issue #378 remains OPEN and had no comments when checked in this wave; its requested independent-review deliverable has not been posted in that issue. This report is an additional source-based review, not a claim that Gemini Agent 1 ran. No code, secrets, host configuration, workflow dispatch, merge or deployment was changed by this review.

PR #375 remains Draft/unmerged. Keep it that way until a separate artifact-only worker/publisher design has explicit issuer/capability ownership and is tested with negative cases. Current state: **NOT PROVEN / BLOCKED**.
