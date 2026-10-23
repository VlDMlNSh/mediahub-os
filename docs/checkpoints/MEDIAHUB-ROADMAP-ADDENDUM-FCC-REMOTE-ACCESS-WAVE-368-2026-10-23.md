# Master Roadmap addendum — FCC remote access (Wave 368)

Date: 2026-10-23

## Decision and state
**BLOCKED / NOT DEPLOYED / NOT QUALIFIED / NOT ACCEPTED**

- Main objective remains [Issue #301 — Contour A cloud-agent development fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301): GitHub-hosted ephemeral workers; no default owner-operated always-on server or public inbound listener.
- FCC access qualification remains [Issue #499](https://github.com/VlDMlNSh/mediahub-os/issues/499).
- FCC routing qualification remains [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296).
- Evidence: [Wave 368 decision report](MEDIAHUB-FCC-REMOTE-ACCESS-DECISION-WAVE-368-2026-10-23.md) and [continuation checkpoint](MEDIAHUB-NEXT-CONTINUATION-WAVE-368-2026-10-23.md).

## Source-backed disposition
At FCC upstream commit `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`, Admin UI/API use a loopback-only guard and upstream tests assert 403 for remote client/non-local Origin. The managed `~/.fcc/.env` contains actual provider key values; the inspected POSIX writer sets mode `0600` but does not implement at-rest encryption. The tests were inspected, not run.

## Roadmap sequencing
1. Keep remote FCC Admin UI deployment and remote key entry blocked.
2. Complete source-based qualification of the provider route in Issue #296, including actual provider identity, terms, quota, no-paid-fallback, secret injection, redacted logs and immutable evidence.
3. Prefer approved job-scoped GitHub Actions secret injection for ephemeral execution where explicitly authorized; do not treat this as proof that FCC route is qualified.
4. Any request for persistent remote Admin UI requires a separate accepted product/security exception with a threat model and storage/access lifecycle controls.
5. Keep PR #500 draft until exact-head CI and independent review are evidenced.

Canonical roadmap remains [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); this addendum is a candidate on the non-canonical branch pending review/merge.


## Wave 369 follow-up
- [Wave 369 source audit](MEDIAHUB-FCC-REMOTE-ACCESS-SOURCE-AUDIT-WAVE-369-2026-10-23.md) records README/test source inspection and the current PR #500 verification state.
- No supported remote Admin mode was established. Tests inspected only; release-note retrieval NOT VERIFIED. Remote UI deployment and production key entry remain BLOCKED.
- PR #500 remains draft until exact-head CI and independent review are evidenced. Canonical roadmap remains unchanged on the canonical docs branch; this addendum is a candidate-branch record.
