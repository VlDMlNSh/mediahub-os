# Map addendum — Wave 392 OpenRouter catalog evidence (2026-10-22)

- Report: [Wave 392 OpenRouter catalog authentication evidence](../checkpoints/MEDIAHUB-NEXT-OPENROUTER-CATALOG-AUTH-WAVE-392-2026-10-22.md).
- Workflow run [39847014875](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875), job [120062857263](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875/job/120062857263), target SHA `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Artifact [12454669532](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875/artifacts/12454669532), digest `sha256:8e95e32e1ebe6d36ae4047424c9a3de12af00c8cc9bd7b37c7533a3db36defe1`.
- Verified: one OpenRouter `GET /api/v1/models`, HTTP 200, sanitized `AUTH_SUCCESS`, 468 catalog entries. The Qwen ID filter ending `:free` returned zero entries.
- Not tested: inference/chat completion, a specific Qwen invocation, permanent free availability, provider route qualification.
- No Gemini controller dispatch or Issue #301 action occurred. Do not conflate this catalog check with Contour A acceptance.
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
