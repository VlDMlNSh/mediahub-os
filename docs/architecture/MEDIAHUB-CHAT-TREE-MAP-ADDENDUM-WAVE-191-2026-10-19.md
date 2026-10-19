# MediaHub OS — project map addendum, Wave 191 (2026-10-19)

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 191 report: [Authorization-layer boundary and integration gaps](../checkpoints/MEDIAHUB-CONTOUR-A-AUTHORIZATION-LAYER-BOUNDARY-AND-INTEGRATION-GAPS-WAVE-191-2026-10-19.md)
- Wave 190 matrix: [Capability admission negative-test matrix](../checkpoints/MEDIAHUB-CONTOUR-A-CAPABILITY-ADMISSION-NEGATIVE-TEST-MATRIX-WAVE-190-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Wave 191 cross-references mesh capability admission, heartbeat HMAC, Astra command HMAC, runtime explicit-grant authorization, and the Security/Trust/Authorization and MH-12 contracts. These layers serve different purposes and must not be treated as interchangeable. Astra command tests do bind a signature to the command operation; that does not prove mesh capability admission uses the same trust decision. The mesh admission test currently accepts a structurally valid qualified EXECUTION capability without issuer-signature or exact operation/resource fields.

The addendum proposes ten cross-layer negative tests. This is source-level design evidence only: no tests run and no implementation changed. Cryptographic choices, trust-root lifecycle, revocation, replay storage and compatibility remain subject to independent governance review. Issue #301 remains open; PR #374/#375/#376 remain Draft. Gemini workflow authority and MCP OCI digest/provenance remain blocked.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
