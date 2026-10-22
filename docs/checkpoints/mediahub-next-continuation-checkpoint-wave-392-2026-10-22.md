# Continuation checkpoint addendum — Wave 392 (2026-10-22)

This is a dated continuation addendum; it does not replace the canonical checkpoint file.

- Wave report: [MEDIAHUB-NEXT-OPENROUTER-CATALOG-AUTH-WAVE-392-2026-10-22.md](MEDIAHUB-NEXT-OPENROUTER-CATALOG-AUTH-WAVE-392-2026-10-22.md).
- Map addendum: [MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-392-2026-10-22.md](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-392-2026-10-22.md).
- Main HEAD at observation: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf` (merge commit for PR #492).
- PR #492: merged. Workflow `.github/workflows/openrouter-github-hosted-catalog-auth-probe.yml` blob SHA `356bc73120819f8a23df731dc97141740e345de1`.
- Actions run [39847014875](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875): SUCCEEDED; job `120062857263`: SUCCEEDED; target SHA matches main.
- Artifact `12454669532`, digest `sha256:8e95e32e1ebe6d36ae4047424c9a3de12af00c8cc9bd7b37c7533a3db36defe1`: sanitized evidence read-back confirmed HTTP 200 / AUTH_SUCCESS / one catalog GET / no inference / 468 models / zero Qwen IDs ending `:free`.
- Status: catalog authentication VERIFIED for one request; Qwen free-model availability through this filter NOT FOUND; inference NOT RUN; provider qualification NOT VERIFIED.
- Issue #301 remains open. Gemini controller dispatch remains NOT RUN; its admission gates are independent and unresolved. Contour A remains NOT ACCEPTED.
- Next: reconcile provider/model registry and public free-model policy against the observed catalog, without repeating the GET or invoking inference absent separate authorization.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
