# MediaHub Chat Tree Map — Addendum Wave 263 (2026-10-20)

## Provider registry consumer census — findings
- `ops/qualification/provider_model_registry.json` on `main`, blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`, is a 25-entry mixed-scope catalog. It includes a localhost Ollama endpoint and inline static bearer value; this entry must not be eligible for the GitHub-cloud-only Contour A pool.
- `profiles/agent-registry.json` on `main`, blob `993cbbe1b2b2a88da7d8884a897b404f055981a8`, is a separate agent catalog spanning external and local tiers. It is not the provider/model registry or proof of availability/qualification.
- `schemas/ai/ai-provider-registry.schema.json` blob `9537a64bc948b1bea3e2a640670f48e107760a50` and `schemas/ai/ai-provider-adapter.schema.json` blob `e0dab7002222451579e649a7d1d29985393d9a42` describe separate AI contracts. Existing tests check schema shape, but this pass found no proof the ops catalog validates against them or is wired into cloud dispatch.
- This is a path-level census, not exhaustive consumer proof: GitHub code search returned no indexed results. A reproducible full-source scan remains open.
- Next: implement CI-only schema/eligibility checks with negative fixtures and mock providers; keep unknown/local records denied by default. Do not call real providers or access secrets.

## Boundary retained
Contour A cloud pool stays exclusively GitHub-hosted. External model APIs are model endpoints only. Owner-operated servers/local hardware remain reserved for later Jarvis/local compute after Contour A deployment and independent acceptance. No new external router, queue or database without explicit governance.

Full evidence: [Wave 263 report](../checkpoints/MEDIAHUB-PROVIDER-REGISTRY-CONSUMER-CENSUS-WAVE-263-2026-10-20.md)

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
