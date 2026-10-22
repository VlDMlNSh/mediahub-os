# MediaHub — FCC Admin UI remote-access qualification (Wave 367)

Date: 2026-10-22  
Status: **SOURCE AUDIT VERIFIED / DEPLOYMENT NOT RUN / REMOTE ACCESS BLOCKED / NOT QUALIFIED / NOT ACCEPTED**

## Canonical references
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on `docs/mediahub-chat-tree-map-20261012`; observed blob SHA `f04873c9cbbf1ba8d45ccbfd3f6afc8cee916a41`. Contents API returned empty content for this >1 MB file, so the canonical map was not modified.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical docs branch HEAD observed before this candidate: `343eeb760b1d49df8371db674e51ffc5942701a9`.
- Main HEAD read directly from Git ref API: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Governing cloud lane: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Existing FCC route tracker: [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296).
- Bounded access qualification: [Issue #499](https://github.com/VlDMlNSh/mediahub-os/issues/499).
- Related cloud Claude/ECC proposal: [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496) and [draft PR #497](https://github.com/VlDMlNSh/mediahub-os/pull/497).

## Upstream source evidence
FCC upstream `main` resolves to commit `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- `README.md` blob: `3f77b4a72d816efa1efa1125bb952cfaef026924`.
- `src/free_claude_code/api/admin_security.py` blob: `f389104b5f53ba4d505433dfeace1423c3ae3088`.
- `src/free_claude_code/api/admin_routes.py` blob: `fa2abc40bb7841027de43592050126ce7869053f`.
- `pyproject.toml` blob: `6b252ac571681a37f635f1f3e9c36fb72dacc5ba`.

The README documents the default Admin UI as `http://127.0.0.1:8082/admin (local-only)`. Source confirms the UI page and Admin API routes call `require_loopback_admin`. The guard rejects non-loopback client hosts, non-loopback Host authority, and non-loopback Origin with HTTP 403. Changing only the bind address or placing an ordinary public reverse proxy in front is not a verified supported remote-access path.

The inspected package metadata declares AGPL-3.0-only and Python `==3.14.7`; deployment/redistribution planning must account for these requirements. This pass did not audit every dependency, configuration persistence path, or upstream release policy.

## Findings
1. Reusing FCC's existing Admin UI is the selected direction; no replacement UI was created.
2. A GitHub Actions runner is ephemeral and does not provide a stable, owner-accessible Admin URL after the job ends. GitHub Pages cannot host FCC's Python backend.
3. FCC's current Admin UI contract is deliberately loopback-only. No upstream-supported authenticated remote-admin mode was established in this bounded audit.
4. MediaHub Issue #301 requires GitHub-hosted ephemeral workers as the default cloud lane and says not to assume an owner-operated always-on server or public inbound listener. A persistent public FCC deployment would be a separate architecture/security decision.
5. Provider keys must not be entered into an exposed service until hosting, admin access, secret persistence/redaction/rotation, provider terms/quota, egress, and recovery are qualified.

## Decision
**BLOCKED for remote Admin UI deployment as-is.** Preserve FCC upstream loopback security. Do not deploy publicly, expose port 8082, change upstream guard behavior, or claim a stable GitHub-hosted URL. A private tunnel/forwarding option remains unqualified until its actual request path is shown to satisfy FCC's loopback guard and MediaHub security requirements.

## Bounded next steps
1. In Issue #499, inspect upstream release docs and tests for a supported remote-admin capability; record exact source refs.
2. Verify FCC configuration/key persistence, redaction and file permissions at the pinned commit.
3. Compare a strictly private access method against the actual loopback guard, Origin/Host checks, authentication, CSRF exposure, and GitHub-hosted runtime constraints.
4. If no supported method exists, stop and request an explicit product/security decision rather than creating a custom UI or silently modifying FCC.
5. Only after approval, add non-launching contract tests and an independent security review; deployment and provider-key entry remain separate gates.

## Execution evidence
- Repository main HEAD and canonical docs branch HEAD were read directly from Git refs.
- FCC upstream source refs and relevant blob SHAs were read back.
- No tests, workflow dispatch, provider/model call, secret-value access, remote service deployment, port exposure, merge, or qualification occurred.
- Issue #499 created as an open bounded tracker. This report is documentation evidence only.

## Status matrix
- Source audit: **VERIFIED** for the named refs/files above.
- Existing Admin UI remote access: **BLOCKED / NOT VERIFIED**.
- Persistent hosting: **NOT RUN / NOT QUALIFIED**.
- Provider key storage on a remote host: **NOT VERIFIED**.
- Deployment and acceptance: **NOT RUN / NOT ACCEPTED**.
