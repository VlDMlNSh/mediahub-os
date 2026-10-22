# MediaHub — FCC remote-access source audit follow-up (Wave 369)

Date: 2026-10-23

## Status
**SOURCE/DOCUMENTATION AUDIT VERIFIED BY READ-BACK / REMOTE ADMIN BLOCKED / DEPLOYMENT NOT RUN / NOT QUALIFIED / NOT ACCEPTED**

## Current refs and governance
- Repository [main](https://github.com/VlDMlNSh/mediahub-os/tree/main) HEAD observed this pass: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Canonical documentation branch HEAD observed this pass: `343eeb760b1d49df8371db674e51ffc5942701a9`.
- Candidate documentation PR: [#500](https://github.com/VlDMlNSh/mediahub-os/pull/500), branch `docs/fcc-admin-ui-remote-access-wave-367-2026-10-22`, exact head observed before this report: `7907ec0158e366686e5f48d165ccb53ec919dd65`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) continues to prohibit assuming a persistent owner-operated server or public inbound listener in the default cloud lane.
- [Issue #499](https://github.com/VlDMlNSh/mediahub-os/issues/499) owns FCC Admin UI access qualification; [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296) owns FCC/FreeLLMAPI/Alamo routing qualification.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md), blob `f04873c9cbbf1ba8d45ccbfd3f6afc8cee916a41`. Its Contents API response remains empty; no claim is made that the canonical map was rewritten.

## Bounded source/documentation pass
Pinned upstream FCC commit: `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- [README](https://github.com/Alishahryar1/free-claude-code/blob/3d2ae2306752dbdf504714a5489bcfcf69b2d04a/README.md), blob `3f77b4a72d816efa1efa1125bb952cfaef026924): documents the normal `fcc-server` start flow and local Admin UI usage; the prior pinned README/source audit identifies the Admin UI URL as `http://127.0.0.1:8082/admin (local-only)`.
- [Admin guard](https://github.com/Alishahryar1/free-claude-code/blob/3d2ae2306752dbdf504714a5489bcfcf69b2d04a/src/free_claude_code/api/admin_security.py), blob `f389104b5f53ba4d505433dfeace1423c3ae3088`, checks loopback client IP, Host authority, and Origin.
- [Admin tests](https://github.com/Alishahryar1/free-claude-code/blob/3d2ae2306752dbdf504714a5489bcfcf69b2d04a/tests/api/test_admin.py), blob `889d6c16d8625a4cdb08baf5ea6f17564a607e77`, assert local Admin access succeeds while a remote client and non-local Origin return 403. These tests were inspected, not executed.
- The inspected upstream tree did not surface a supported remote-admin deployment recipe or common deployment manifests (Docker/Compose, reverse-proxy, systemd, Helm) that establish a compliant access path. This is a bounded tree/README observation, not proof that no external deployment method exists. Release endpoint retrieval was unavailable through the current connector; release-note status is **NOT VERIFIED**.
- Prior source audit of `paths.py` / `env_migrations.py` established managed config at `~/.fcc/.env`; credentials persist as plaintext values, with POSIX mode `0600`, no at-rest encryption in the inspected writer, and no equivalent explicit chmod in that path on Windows.

## Decision
No supported remote Admin UI path has been established that satisfies the pinned loopback security contract and Issue #301's default hosting constraints. Keep FCC Admin UI local-only. Do not expose port 8082, weaken or spoof client/Host/Origin checks, or build a replacement UI. Do not enter production provider keys into a remote instance without a separately accepted host, access, storage/backup, rotation/deletion, egress, and provider-policy design.

Job-scoped GitHub Actions secret injection is a separate possible credential-delivery mechanism for specifically authorized ephemeral jobs; it does not qualify FCC integration or any provider/model route. Issue #296 gates remain applicable.

## Verification and status
- Main and canonical docs refs: **READ / VERIFIED** for this snapshot.
- Pinned README, security guard and test source: **READ / VERIFIED**.
- Upstream test execution: **NOT RUN**.
- Release notes: **NOT VERIFIED** (connector retrieval unavailable).
- PR #500 candidate head checked during this pass: `6380b80a9b41315935d926a964ba5d1e0ab3f1ee`: status endpoint returned `pending` with zero status contexts; PR-triggered workflow query returned zero runs; formal review list was empty. CI and independent review are **NOT VERIFIED**, not PASS.
- No workflow dispatch, secret-value read, provider/model call, deployment, port exposure, merge, qualification, or acceptance occurred.

## Next step
Keep PR #500 draft pending real exact-head CI and independent review. Continue Contour A independently through Issue #301's next open implementation gate; do not turn this blocked FCC UI investigation into a persistent service or bypass the approved Gemini controller.
