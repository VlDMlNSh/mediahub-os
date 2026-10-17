# MediaHub OS — Chat tree map addendum, Wave 123 (2026-10-18)

## Precise Gemini CI event-filter regression

- Report: [Wave 123 — precise event-filter regression](../checkpoints/MEDIAHUB-GEMINI-CI-EVENT-FILTER-REGRESSION-WAVE-123-2026-10-18.md).
- Candidate HEAD: `16b3b2ee73bc12ac213818cf0ad22abedafd50ad`.
- Tightened `scripts/test_gemini_readonly_workflows.py`: for both `scripts/gemini_http_response.js` and `scripts/test_gemini_http_response.js`, assert exactly one entry in `push.paths` and exactly one in `pull_request.paths`, rather than a combined count.
- Test blob: `b130261a2c12608614780a1ab2f8f05483e1180e`; validation workflow blob: `fcbe964602bff7e03ed38632dc18066efad4d99c`.
- Exact-head CI passed: contract #39074978642, Astra Cloud Runtime Validation #39074978634, Astra Verify #39074978856.
- PR #334 remains OPEN / DRAFT / UNMERGED. Independent security review and authorized branch-protection/ruleset read-back remain outstanding.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
