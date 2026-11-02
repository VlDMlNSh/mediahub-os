# Wave 522 — Colibri / GLM-5.2 suitability assessment (2026-11-02)

## Scope and disposition

Bounded, source-pinned research of [JustVugg/colibri](https://github.com/JustVugg/colibri) following the owner clarification “JustVugg / colibri”. This is a component assessment only: **REUSE-CANDIDATE / NOT ADOPTED / NOT INSTALLED / NOT QUALIFIED**.

**Decision:** Colibri is not a viable deployment target for the ordinary GitHub-hosted Ubuntu runner used by MediaHub's cloud-agent workflows when the intended workload is GLM-5.2. Keep it as a candidate for a separately qualified local-compute host with sufficient fast storage and memory. Do not add it to Runner 1 or Runner 2 yet. GLM-4.7 support is not evidenced by the inspected Colibri model inventory.

## Immutable source boundary

- Colibri repository: https://github.com/JustVugg/colibri
- Inspected upstream `main` commit: `0a5504a1dc64f86fcd0fe7db298b0448c730e7e6`
- Latest release observed: `v2.1.0`, published 2026-10-31; tag object SHA `8579957378ca922ad4340a6392513485cbc50c2c`
- Colibri license: Apache-2.0 (repository LICENSE).
- Upstream README and API documentation were read from that pinned `main` commit. The repository's README identifies GLM-5.2/5.3 engines and does not list GLM-4.7.
- MediaHub main HEAD: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`.
- Canonical documentation branch base: `d9a289b9113f7567711b641a7017eb814d6c259d`.
- This report is stacked on Wave 521 PR #628 branch head `a3e0c26ffb04265ade33057c0bafecb0f22f3f23`; it is not on the canonical branch until the stack is reviewed and integrated.

## Verified upstream capabilities

1. Colibri is a local inference engine for large sparse/MoE models, streaming expert weights from local storage; it is not a hosted model API or a cloud compute service.
2. README model inventory includes GLM-5.2 (744B) and GLM-5.3. GLM-5.2's listed download is approximately **429 GB**; listed RAM is **16 GB minimum / 24 GB recommended**. The upstream table reports 0.05–0.1 tokens/s cold on a 25 GB laptop, 1.83 tokens/s on a 128 GB Ryzen AI Max+ 395, and 9.0–9.2 tokens/s on six RTX 5090 GPUs. These are upstream reported measurements, not MediaHub benchmarks.
3. Colibri documents an OpenAI-compatible API (`/v1/chat/completions`) and Anthropic Messages API (`/v1/messages`); its tool-calling matrix lists GLM-5.2 as supporting both OpenAI `tools` and Anthropic `tool_use`.
4. The gateway serves one generation at a time; concurrent HTTP requests queue. This is a material throughput constraint for concurrent agent workloads.
5. The documented default bind is localhost. API authentication is **off when no `COLI_API_KEY` is configured**; the docs explicitly require configuring it before exposing the server beyond the machine. The API accepts bearer auth and `x-api-key` when configured.
6. The Anthropic-compatible endpoint can be used by clients such as Claude Code, but that is a protocol compatibility statement, not proof of compatibility with MediaHub FCC policy, model behavior, or an accepted Claude Code route.
7. Colibri's software license is Apache-2.0. Model-weight licensing remains separate; the README states GLM-5.2 weights are released by Z.ai under MIT.

## MediaHub fit assessment

| Target | Disposition | Reason |
|---|---|---|
| GitHub-hosted Runner 1 | **NO-GO for GLM-5.2** | A 429 GB model download is incompatible with the normal ephemeral runner disk envelope and lifecycle; no persistent 429 GB fast local volume is part of the accepted runner contract. |
| GitHub-hosted Runner 2 / Gemini controller | **NO-GO** | Runner 2 is reserved for the approved Gemini controller/agents. Colibri is neither required by nor authorized to replace that controller. |
| Separately qualified local-compute host | **REUSE-CANDIDATE** | Potentially viable only after hardware target, free disk, sustained storage throughput, RAM, accelerator, isolation, API auth and measured latency are verified. |
| GLM-4.7 | **NOT VERIFIED / NOT SUPPORTED BY INSPECTED INVENTORY** | No GLM-4.7 engine/model entry was found in the pinned upstream model list. Do not infer compatibility from GLM-5.2 support. |

The cloud-runner conclusion is a resource-fit assessment, not a benchmark against an account-specific runner. No assumption is made about an unverified persistent disk or attached hardware.

## Security and integration gates

- Do not bind Colibri to `0.0.0.0` or expose an unauthenticated API. Keep loopback-only unless a separately accepted network/authentication design supplies TLS, identity, authorization, egress controls and secret handling.
- Do not put `COLI_API_KEY` or model-provider credentials in prompts, artifacts, workflow logs or repository content.
- Do not use Colibri's MCP setup/install actions as an alternate provisioning or authority plane.
- Do not place Colibri on Runner 2 or route Gemini through it.
- Before any adoption: pin a release artifact by digest and verify provenance; inspect the complete license/notice and model-weight terms; qualify a designated local host; measure disk throughput, resident memory, cold/warm tokens/s, cancellation/recovery and concurrent queue behavior; test OpenAI/Anthropic tool-call semantics with non-sensitive fixtures; verify API authentication and network isolation; obtain independent security review.
- No model download, inference, provider call, package installation, host mutation, credential read, agent dispatch, merge, deployment, qualification or acceptance occurred in this wave.

## MediaHub source state and governance

- Issue #301 remains OPEN. Its ordered gates include A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy authority, runner/workspace/network target manifest acceptance, Draft 2020-12 schema meta-validation with positive/negative fixtures, independent schema review, and source-bound hardening before a controlled read-only worker.
- Main controller blob on main: `0a1246f6755020faf8b7e48d07bfff790bbaece3`. It exposes probe/agents/review modes and fixed role tasks; batch admission checks `MEDIAHUB_GEMINI_BATCH_ENABLED`, and dispatch fails closed if `MEDIAHUB_GITHUB_TOKEN` or `MEDIAHUB_DISPATCH_HMAC_KEY` is absent. Effective secret presence/scope was not inspected. The three child workflows are separate `ubuntu-latest` workflow dispatches, not co-located on one persistent Runner 2.
- Main HEAD combined status and PR workflow-run lookup returned empty collections; treat them as **NOT VERIFIED**, not PASS.
- PR #628 exact-head workflow runs/statuses and formal reviews returned empty collections; PR #625 exact-head workflow runs/statuses and formal reviews also returned empty collections. Both remain open and unaccepted. This Wave 522 PR is stacked on #628 and must not be merged ahead of its base.

## Next bounded step

Keep Colibri as a research candidate only. Continue Contour A's higher-priority governance/schema/worker gates; do not spend runner quota downloading GLM-5.2. Once a new local-compute target is formally available, perform the hardware/resource preflight and release-artifact provenance verification before any installation or inference.

## Direct sources

- [Colibri repository](https://github.com/JustVugg/colibri)
- [Colibri v2.1.0 release](https://github.com/JustVugg/colibri/releases/tag/v2.1.0)
- [Colibri README](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/README.md)
- [Colibri API documentation](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/api.md)
- [MediaHub Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [MediaHub canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
