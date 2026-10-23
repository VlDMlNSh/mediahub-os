# MediaHub — FCC remote-access decision record (Wave 368)

Date: 2026-10-23  
Status: **SOURCE AND TEST-CONTRACT AUDIT VERIFIED / REMOTE ADMIN ACCESS BLOCKED / DEPLOYMENT NOT RUN / NOT QUALIFIED / NOT ACCEPTED**

## Canonical and governing refs
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md), branch `docs/mediahub-chat-tree-map-20261012`, observed blob `f04873c9cbbf1ba8d45ccbfd3f6afc8cee916a41`. The Contents API returned empty content for this >1 MB file; map itself remains unchanged.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical docs branch HEAD: `343eeb760b1d49df8371db674e51ffc5942701a9`.
- Main HEAD: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301): no owner-operated always-on server or public inbound listener in default cloud lane; hosted workers are ephemeral.
- [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296): FCC/FreeLLMAPI/Alamo route still requires component/runtime qualification.
- [Issue #499](https://github.com/VlDMlNSh/mediahub-os/issues/499): bounded FCC Admin UI access qualification.
- [Draft PR #500](https://github.com/VlDMlNSh/mediahub-os/pull/500), candidate branch `docs/fcc-admin-ui-remote-access-wave-367-2026-10-22`, head before this report `a1ca6b9861aac818ab92e9f8df5802e96045cb61).

## Exact upstream source/test refs
FCC upstream tree commit: `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- `src/free_claude_code/api/admin_security.py`, blob `f389104b5f53ba4d505433dfeace1423c3ae3088`.
- `src/free_claude_code/api/admin_routes.py`, blob `fa2abc40bb7841027de43592050126ce7869053f`.
- `tests/api/test_admin.py`, blob `889d6c16d8625a4cdb08baf5ea6f17564a607e77`.
- `src/free_claude_code/config/paths.py`, blob `aa50864662b26ab08eaf35fdba9843e37a75cc8c`.
- `src/free_claude_code/config/env_migrations.py`, blob `c67943bdf9902fd4f25e1ecce7e69867e2abe2a6`.
- `pyproject.toml`, blob `6b252ac571681a37f635f1f3e9c36fb72dacc5ba` (AGPL-3.0-only, Python `==3.14.7`).

## Test/source findings
1. `require_loopback_admin` requires the request client IP to be loopback, `Host` authority to be localhost/loopback, and `Origin` to be absent or localhost/loopback. The guard is applied to Admin UI/API routes.
2. Upstream test `test_admin_page_is_loopback_only` in `tests/api/test_admin.py` asserts local requests return 200 and remote client `203.0.113.10` returns 403. A separate test asserts a non-local web Origin (example `https://example.com`) returns 403. These are source/test assertions read from the pinned commit; this pass did not run upstream tests.
3. A conventional hosted public URL, browser-origin access, or ordinary reverse proxy is not established as supported. Rewriting forwarded headers/client identity to simulate loopback would defeat the guard's trust assumption and is not an acceptable shortcut.
4. A client-side SSH/local tunnel may preserve local browser Host/Origin only when the user device can create and maintain the tunnel to a reachable remote host. That still requires a persistent/reachable host and tunnel lifecycle, and is not compatible with Issue #301's default “no owner-operated always-on server/public inbound listener” route without an explicit architecture exception. It is not qualified here.
5. FCC stores managed provider configuration at `~/.fcc/.env`. The inspected writer applies POSIX mode `0600` but persists actual credential values in plaintext; this write path does not implement at-rest encryption and does not apply an equivalent explicit chmod on Windows. UI masking is not encryption.

## Decision
**Do not deploy the FCC Admin UI as a persistent remote service in the default Contour A lane.** There is no source/test evidence of an upstream-supported authenticated remote-admin mode at the pinned commit. Do not expose port 8082, weaken or bypass loopback checks, spoof client/Origin/Host, or build a replacement UI.

Recommended technical path:
- Keep FCC Admin UI local-only if FCC is used interactively on a trusted machine; do not treat this as cloud-hosted access.
- For GitHub-hosted ephemeral execution, use provider credentials only through approved GitHub Actions runtime secret injection, scoped to the exact job/environment and never copied into artifacts/logs/prompts. This does **not** itself complete FCC integration or authorize any provider route; Issue #296 still governs provider/model identity, quota, terms, fallback and evidence.
- If owner requires a persistent remotely accessible FCC UI, it is a separate product/security architecture exception requiring an accepted threat model, host/storage/backup/credential lifecycle controls, private authentication, provider-policy review, and new acceptance gates. Do not infer that exception from the request to reuse the existing UI.

## Verification/status matrix
- Pinned FCC source refs and test assertions: **VERIFIED by read-back**.
- Upstream test execution in this pass: **NOT RUN**.
- Upstream-supported remote-admin mode: **NOT FOUND in inspected source/docs; NOT QUALIFIED**.
- Remote hosting / key entry: **BLOCKED / NOT RUN**.
- Exact-head CI for PR #500 before this report: combined status returned no checks and PR-triggered workflow query returned no runs; **NOT VERIFIED**, not PASS.
- Independent review of PR #500: no submitted reviews; **NOT VERIFIED**.
- No secrets read, provider/model calls, workflow dispatch, deployment, port exposure, tests, or merge occurred.

## Next bounded step
Finish documentation-only source qualification by checking upstream release notes and config/key redaction/backup behavior, then submit PR #500 for exact-head CI and independent review. Keep the deployment decision blocked unless a compliant private-access architecture and credential-storage controls are separately accepted.
