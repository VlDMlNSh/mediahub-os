# Wave 392 — OpenRouter catalog authentication evidence (2026-10-22)

## Scope and immutable target

- Repository: [mediahub-os](https://github.com/VlDMlNSh/mediahub-os)
- Workflow run: [39847014875](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875)
- Target/main merge commit: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`
- Merged implementation PR: [#492](https://github.com/VlDMlNSh/mediahub-os/pull/492)
- Workflow blob SHA at main: `356bc73120819f8a23df731dc97141740e345de1`
- Job: [120062857263](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875/job/120062857263)
- Artifact: [openrouter-catalog-probe-39847014875-1](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875/artifacts/12454669532)
- Artifact ID: `12454669532`; GitHub-reported digest: `sha256:8e95e32e1ebe6d36ae4047424c9a3de12af00c8cc9bd7b37c7533a3db36defe1`
- Evidence schema: `mediahub.openrouter.catalog-auth-probe.v1`

## Observed sanitized result

The artifact was downloaded and read back. Its JSON reported:

- `status=AUTH_SUCCESS`
- `http_status=200`
- `credential_present=true` (presence only; no secret value read or recorded)
- `configured_model=openrouter/free`
- `request_count=1`, request kind `GET /api/v1/models; no inference`
- `catalog_model_count=468`
- `qwen_free_model_count=0`, `qwen_free_model_ids=[]`
- `latency_seconds=0.349`
- `target_sha=3b054cc8fac38d2fbd58305e9d185d307c6a18bf`
- Artifact explicitly marks secret values as suppressed.

## Interpretation and limits

- **Catalog authentication is VERIFIED for this single GET at the recorded target.**
- The workflow and its only job both concluded `success`.
- **No inference was performed.** This is not evidence that a chat-completion request works, that a particular Qwen model can be invoked, or that any model is permanently free.
- At this catalog snapshot, the workflow's filter found no Qwen model IDs ending in `:free`. This is a bounded observation, not proof that no Qwen model is accessible through every route or that the catalog is static.
- No retries, redirects, paid fallback, or second provider request were performed by the workflow.
- No Gemini controller run was started in this pass. Issue #301 remains open and its governance gates remain separate from this provider catalog check.
- The artifact's GitHub digest is recorded as returned by the Actions API. No independent recomputation of that digest from the ZIP bytes was performed.

## Status

**CATALOG AUTH: VERIFIED / QWEN :FREE CATALOG MATCH: ZERO / INFERENCE: NOT RUN / PROVIDER ROUTE QUALIFICATION: NOT VERIFIED / CONTOUR A: NOT ACCEPTED**

## Next bounded step

Do not repeat the catalog GET solely to reproduce this result. First reconcile the provider registry and documented free-model selection policy with the observed empty Qwen `:free` subset, using public catalog/docs or existing repository evidence. Any inference probe requires separate explicit authorization and its own budget/route gate.

## Project navigation

- [Canonical chat tree map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Current continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
