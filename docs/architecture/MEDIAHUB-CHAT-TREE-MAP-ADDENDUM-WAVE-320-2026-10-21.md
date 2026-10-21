# Map addendum — Wave 320 UUID validation hardening

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)

- Report: [Wave 320 UUID validation hardening](../checkpoints/MEDIAHUB-PR432-UUID-VALIDATION-HARDENING-WAVE-320-2026-10-21.md).
- PR #432 current head: `8a6bc17180ff8027edb5c628f8092a4c527212b5`, OPEN/DRAFT/UNMERGED.
- All three Gemini child workflows now use canonical lowercase UUIDv4 validation for dispatch IDs. Added valid/invalid fixture contract test. Read-back Blob SHAs: Agent 1 `155a02159912ca371e6f826c51325ca269857aad`; Agent 2 `fff1820a6b97d379b23674f36bd62227b7d4dec2`; Agent 3 `781df56e8aa7c75ba453c08378611857862b2e44`; test `65bc0c4b9a7eb58a71bb1b8123cf1ff4305f52af`.
- Exact-head CI run IDs: 39648235100, 39648235554, 39648235456, 39648235621, 39648235821. They were still running/queued at report time; do not call them passing until terminal.
- Agent dispatch remains NOT RUN. Next: verify terminal CI, formal independent review, permissions/secret/governance gates and Alamo route before any runtime dispatch.
