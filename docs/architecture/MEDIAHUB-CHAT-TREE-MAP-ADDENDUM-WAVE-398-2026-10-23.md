# Chat tree map addendum — Wave 398: Claude GitHub-hosted route feasibility

Date: 2026-10-23

- Report: [Claude GitHub-hosted execution route feasibility](../checkpoints/MEDIAHUB-CLAUDE-GITHUB-HOSTED-ROUTE-FEASIBILITY-WAVE-398-2026-10-23.md).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).
- Immutable target observed: `main` `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`; canonical docs branch before this addendum: `222528d30ace88ed7ab4bf75152a35b5bfcf126c`.
- Existing hosted worker `.github/workflows/mediahub-claude-worker.yml` blob SHA `e1260cfef88ac02bcc9d0cce67bb497820f5f63c` is gated on `MEDIAHUB_ALLOW_METERED_ANTHROPIC=true` and `ANTHROPIC_API_KEY`; it does not satisfy a free-route requirement.
- Current route governance recorded in [Issue #301 Wave 369](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6342174085) distinguishes controller-only Gemini cloud dispatch from local Claude/FCC/Ollama. A hosted FCC/free-provider path requires explicit route-contract reconciliation; no alternate route was created.
- FCC is a candidate integration, not evidence of a currently free/authorized provider or guaranteed no-paid-fallback.
- **Disposition:** requested architecture **PLANNED**; implementation **NOT STARTED**; route governance **OPEN**; execution/qualification **NOT RUN / NOT VERIFIED**; Contour A remains **NOT ACCEPTED**.
