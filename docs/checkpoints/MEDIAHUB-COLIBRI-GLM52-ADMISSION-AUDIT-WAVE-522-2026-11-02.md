# Wave 522 — Colibri / GLM-5.2 admission audit (2026-11-02)

## Scope and disposition

Read-only source and capacity assessment of [JustVugg/colibri](https://github.com/JustVugg/colibri) as a possible local inference backend for MediaHub Contour A. No code, workflow, secret, runner, provider, or host changes were made. No installation, model download, inference, benchmark, or runtime qualification was performed.

**Disposition: RESEARCHED / NOT ADMITTED / NOT RUN.** Colibri is a technically credible local-inference candidate for GLM-5.2, but it is not viable on the standard GitHub-hosted Ubuntu runner. Do not add it to Runner 1 or Runner 2 until a separately authorized resource profile and runtime qualification exist.

## Immutable source evidence

Upstream repository: https://github.com/JustVugg/colibri

- Upstream `main` snapshot inspected: `0a5504a1dc64f86fcd0fe7db298b0448c730e7e6`.
- README blob: `6aec0134be593934df22571c7a7e67665049c01a`.
- API documentation blob: `7951d7e157cfb0778bda9a343e055b0bd4854d5a`.
- API gateway source blob: `6d9b3add7a6d62eea3a73f9b0528ea952d8818c1`.
- Anthropic Messages API test blob: `ac152056e2c0b655ab69d89c6eb4c9161f09abc5`.
- License blob: `17303f1b8e08ef6280318dd81dc418e8c5bfd340`.
- Source license: Apache-2.0. Upstream README separately states GLM-5.2 weights are MIT; this audit did not independently verify the model-card/weight repository's current license or provenance.

Pinned source links:
- [README at inspected commit](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/README.md)
- [API contract at inspected commit](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/api.md)
- [API server source at inspected commit](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/c/openai_server.py)
- [Anthropic API tests at inspected commit](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/c/tests/test_anthropic_messages.py)

## Model and resource fit

Upstream README identifies GLM-5.2 as a 744B-parameter MoE model, with approximately 40B active per token. Its listed int4 package is approximately **429 GB on disk**; memory guidance is **16 GB minimum / 24 GB recommended**. Upstream-reported CPU results include 0.05–0.1 tok/s cold on a 25 GB laptop and 1.83 tok/s on a 128 GB Ryzen AI Max+ 395. These are upstream claims, not MediaHub measurements.

Official GitHub-hosted runner specifications:
- Public standard `ubuntu-latest`: 4 vCPU, 16 GB RAM, 14 GB SSD.
- Private standard `ubuntu-latest`: 2 vCPU, 8 GB RAM, 14 GB SSD.
- Larger Ubuntu runners include 16 vCPU / 64 GB RAM / 600 GB SSD and 32 vCPU / 128 GB RAM / 1,200 GB SSD.

Sources: [GitHub standard runner specifications](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) and [larger runner specifications](https://docs.github.com/en/actions/reference/runners/larger-runners).

Consequences:
1. The standard public runner has only 14 GB SSD; it cannot hold the 429 GB model. Its 16 GB RAM is also below the upstream recommended 24 GB.
2. Standard private runners are further below the minimum memory recommendation.
3. A 16-vCPU / 64-GB / 600-GB larger runner is capacity-plausible on paper, but its availability, price, account entitlement, actual usable disk, throughput and budget have not been verified. It is not an approved free fallback.
4. Larger GitHub-hosted runners are still ephemeral. Model re-download/cache strategy, storage retention, transfer time, and repeated-run cost would need a separate design and evidence.
5. A 429-GB model must not be pulled during ordinary CI or on the Gemini Runner 2.

## API and security contract observations

Static inspection of the pinned source/docs establishes:

- Colibri exposes OpenAI-compatible `/v1/chat/completions` and Anthropic Messages `/v1/messages` endpoints.
- GLM-5.2 is listed as supporting OpenAI `tools` and Anthropic `tool_use`.
- Default bind is loopback (`127.0.0.1`); the API key is optional by default. Non-loopback binding is refused without `COLI_API_KEY`, unless the explicit unsafe override `COLI_ALLOW_INSECURE_BIND=1` is set.
- The API gateway accepts both Bearer and `x-api-key` authentication and compares configured credentials using constant-time comparison.
- `--allowed-host '*'` disables the DNS-rebinding Host-header guard; this must not be used in an admitted MediaHub profile. Wildcard CORS must likewise be excluded.
- API docs describe a bounded FIFO admission queue. The default KV slot count is one; requests queue rather than execute in parallel. The default maximum waiting queue is eight with a 300-second timeout. This is a throughput/latency constraint, not a three-agent parallel inference pool.

Admission requirements if reconsidered:
- Keep the listener loopback-only; never set `COLI_ALLOW_INSECURE_BIND=1`.
- Configure a runtime-only API key even on loopback; do not place its value in repository files, logs, prompts or artifacts.
- Do not use wildcard allowed-host or CORS settings.
- Restrict caller processes/workspaces and outbound network access; do not expose a public listener.
- Set explicit model, context/KV slots, queue and timeout limits; record saturation and cancellation evidence.
- Pin the engine commit, model repository revision, every model shard digest, conversion recipe, compiler/build inputs and runtime binary digest before qualification.
- Verify the model-weight license and provenance separately from the Apache-2.0 engine source.

## Compatibility and architecture decision

| Question | Evidence-based result |
|---|---|
| GLM-5.2 in Colibri | SUPPORTED in upstream README/API matrix |
| GLM-4.7 in Colibri | NOT DOCUMENTED / NOT VERIFIED |
| OpenAI-compatible API | DOCUMENTED |
| Anthropic Messages API | DOCUMENTED; tests exist in upstream source |
| Tool calls for GLM-5.2 | OpenAI tools and Anthropic tool_use documented |
| Standard GitHub-hosted Ubuntu | NOT FEASIBLE for 429-GB model |
| Larger GitHub runner | CAPACITY-PLAUSIBLE, but budget/availability/runtime NOT VERIFIED |
| MediaHub installation or qualification | NOT RUN |

Colibri is a **local inference engine**, not a hosted GLM API provider. It can be evaluated as an optional Runner 1 backend only after a resource/budget decision. It must not be added to Runner 2 or treated as a substitute for the approved Gemini controller. The merged Runner 1 workflow remains source-integrated only; its live Ollama/FCC/Claude runtime is still NOT RUN. Adding Colibri to that same standard runner would exceed available disk and create resource contention.

If the product requirement is to use GLM through a hosted endpoint rather than load local weights, that is a separate provider/API route and must be evaluated under the existing provider, issuer/capability, quota, privacy and no-paid-fallback contracts. Colibri does not solve that route by itself.

## MediaHub state at this pass

- `main`: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`.
- Canonical documentation branch base: `docs/mediahub-chat-tree-map-20261012` at `d9a289b9113f7567711b641a7017eb814d6c259d`.
- Gemini controller on main: blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`; it dispatches three separate `ubuntu-latest` child workflows, not three co-located Gemini workers on a single Runner 2.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN. A0 issuer/ingress/lease/cancel/recovery and R-06 authority gates, authoritative runner/workspace/network target manifest, full Draft 2020-12 validation and independent schema review remain ahead of controlled dispatch.
- PR #628 is OPEN/DRAFT; exact-head CI and formal independent review are NOT VERIFIED.
- PR #625 is OPEN and unmerged; same-host Runner 2 topology remains a proposal, not implementation.
- No Gemini dispatch, provider call, secret access, runner allocation, Colibri installation, model download, inference, merge, deployment, qualification or acceptance occurred.

## Next bounded step

Do not install Colibri yet. If the owner wants local GLM-5.2 on GitHub infrastructure, first verify that a permitted larger-runner configuration is available and within an explicitly approved budget; then prepare a separate resource-isolated proof-of-concept branch with pinned engine/model inputs, checksum/provenance verification, no-secret contract tests, and a loopback-only API smoke test. Otherwise keep Colibri as a researched candidate and leave the current Runner 1/Runner 2 topology unchanged.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
