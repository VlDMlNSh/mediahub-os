# MediaHub Chat Tree Map Addendum — Wave 59

- Date: 2026-10-17
- Status: **PER-WORKFLOW KEY MAPPING CONFIRMED / RUNTIME ROTATION UNPROVEN / CONSUMER TRACE OPEN**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Primary evidence report: [Gemini Secret Wiring and Agent-Fabric Consumer Trace — Wave 59](../checkpoints/MEDIAHUB-GEMINI-SECRET-WIRING-AND-AGENT-FABRIC-CONSUMER-TRACE-WAVE-59-2026-10-17.md)

## Evidence delta

- Current `main` HEAD at final refresh: `4f2788058a98d84a6189651364e154dfb21c2899`, commit title `feat(agents): add two Gemini agent workflows and router plan (#314)`.
- Branches remain **DIVERGED**: docs ahead 2078 / behind 21; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Original Gemini workflow SHA `09523d809530ae5b7bf528eab5fa53bc5deaf92d` references `secrets.GEMINI_API_KEY`. Agent 2 workflow SHA `6c59d42f0777ffbe4528594a756f9839e81a6726` maps `GEMINI_API_KEY_2`; Agent 3 SHA `44ef9aeb8bcc8607bc4c07fe62fc4c56baa69d1e` maps `GEMINI_API_KEY_3`. Source-level wiring is confirmed; runtime dispatch, credential validity, and quota-aware rotation/failover remain unverified.
- Registry SHA `0317d1e794aa80cd0fa22bd953b95921b26aafd3`; direct loader remains OPEN. Claim/lease primitives SHA `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` expressly model coordination state.
- Authorization scheme SHA `5ae1182511486c2961e28c489ce891b74f1252f1` remains `FAIL_CLOSED`, with empty `authorized_pass` and topology `BLOCKED`; direct consumer remains OPEN.
- Agent-fabric workflow SHA `2cec0ba1f02018f7037417363c707a13bc673117` enforces legacy A0 coordination wording and claim-boundary language.
- Canonical map blob SHA `0141454f29b3da6c84488f9464be30812e0b13a3`; exact-path fetch returned an empty body in final read-back. No map mutation was attempted.

## Navigation and disposition

- Keep DEC-DEV-02 Option C and qualification fail-closed.
- Preserve the secret-wiring finding as source-level evidence only; repository secret existence and runtime rotation are unverified.
- Use append-only addenda while canonical map path/blob retrieval is reconciled.
- Tests, qualification, provider calls, workflow dispatch, credentials, host/runtime inspection, infrastructure change, deployment and branch integration: NOT PERFORMED.
