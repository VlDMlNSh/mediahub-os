# FCC Admin UI persistence follow-up — Wave 367

Date: 2026-10-22

## Status
**SOURCE AUDIT VERIFIED / REMOTE ACCESS BLOCKED / NOT DEPLOYED / NOT QUALIFIED / NOT ACCEPTED**

## References
- [Canonical chat tree map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 367 report](MEDIAHUB-FCC-ADMIN-UI-REMOTE-ACCESS-QUALIFICATION-WAVE-367-2026-10-22.md)
- [Map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-FCC-ADMIN-UI-WAVE-367-2026-10-22.md)
- [Issue #499 — safe remote FCC Admin UI access](https://github.com/VlDMlNSh/mediahub-os/issues/499)
- [Governing Contour A Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Documentation PR #500](https://github.com/VlDMlNSh/mediahub-os/pull/500)

## New source finding
FCC upstream commit `3d2ae2306752dbdf504714a5489bcfcf69b2d04a` stores managed configuration at `~/.fcc/.env` (blob `aa50864662b26ab08eaf35fdba9843e37a75cc8c`). Atomic dotenv writer blob `c67943bdf9902fd4f25e1ecce7e69867e2abe2a6` applies mode `0600` to the temporary and final files on POSIX; the inspected path does not explicitly chmod on Windows. The Admin masks credentials in UI projections, but provider keys remain plaintext in the persisted dotenv file. This writer does not implement at-rest encryption.

## Decision and constraints
- Do not enter production provider keys into a remote FCC Admin UI.
- Do not expose port 8082 or weaken FCC's loopback guard.
- GitHub-hosted Actions workers are ephemeral; they are not a persistent Admin host.
- Remote hosting requires separate qualification of host trust, filesystem permissions/encryption, backups/snapshots, access control, rotation/deletion, egress and provider policy.
- No deployment, provider calls, secret-value reads, workflow dispatch, tests, or port exposure were performed.

## Next bounded step
Continue Issue #499 by inspecting upstream tests/release deployment guidance and documenting whether any upstream-supported private access path can satisfy the loopback guard without a public listener or custom UI. If none exists within Issue #301's constraints, leave remote Admin deployment BLOCKED and record the exact unresolved product/security boundary.
