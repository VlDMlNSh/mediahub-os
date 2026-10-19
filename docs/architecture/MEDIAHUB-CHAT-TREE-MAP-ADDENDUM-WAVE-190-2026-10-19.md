# MediaHub OS — project map addendum, Wave 190 (2026-10-19)

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 190 report: [Capability admission negative-test matrix](../checkpoints/MEDIAHUB-CONTOUR-A-CAPABILITY-ADMISSION-NEGATIVE-TEST-MATRIX-WAVE-190-2026-10-19.md)
- Wave 189 report: [Issuer/lifecycle crosswalk](../checkpoints/MEDIAHUB-CONTOUR-A-MESH-CAPABILITY-ISSUER-LIFECYCLE-CROSSWALK-WAVE-189-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Wave 190 adds a proposed, unapproved negative-test matrix for capability issuer trust, signature verification, principal/operation/resource binding, scope attenuation, time validity, revocation freshness, replay, qualification evidence, auxiliary restrictions, algorithm downgrade, canonical parsing, and fail-closed dependency errors. Positive/property tests cover a valid bound envelope, signed-field tampering, cross-operation reuse, attenuation, and concurrent replay.

A source-review clarification: mesh heartbeat validation has a separate HMAC/time/sequence path; Wave 190 does not claim that replay protection is absent everywhere. The specific unresolved gap is that inspected capability admission does not authenticate a signed capability envelope or bind it to the exact requested operation/resource. No tests were run and no implementation changes were made. Protocol and key lifecycle choices remain subject to independent governance review.

Issue #301 remains open; PR #374/#375/#376 remain Draft. Gemini workflow authority and MCP OCI digest/provenance remain blocked. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
