# MediaHub AI Routing / Network Architecture Checkpoint

Date: 2026-09-29
Repository: VlDMlNSh/mediahub-os
Branch: main

## Purpose

Checkpoint for continued investigation of a ready-made distributed AI gateway + private server mesh architecture for Astra/MediaHub.

## Immutable constraints

- Current canonical GOLD run #176 must not be touched, restarted, killed, or duplicated.
- Immutable R4 baseline: 471f709f5633feab7aeb62dd3ea52effad6d2bc584.
- Desktop Commander is prohibited.
- API secrets must never be exposed.
- API secrets are to remain exclusively in GitHub Secrets; do not persist provider keys on servers/disks.
- OpenAI Direct is excluded because it is not usable from the user's environment.
- UnoRouter and ZeroRouter remain in the provider pool; prior instructions to exclude them are obsolete.
- The desired network architecture must not depend on VPN/geographic circumvention as a way to defeat a provider's regional or contractual restrictions. VPN/mesh is for connecting infrastructure and selecting legitimate network paths.

## Architecture under investigation

Preferred conceptual stack:

GitHub Secrets -> GitHub Actions/Astra -> AI Gateway (existing OmniRoute first; LiteLLM/AIGate alternatives) -> private mesh/network layer (Headscale/WireGuard, NetBird, Netmaker, or simpler WireGuard) -> qualified upstream AI providers.

Key principle:
- GitHub is the only secret store.
- Servers hold routing/configuration, not persistent API keys.
- Runtime access to a secret, if technically required for an API request, must be ephemeral and non-persistent.
- AI Gateway should provide one endpoint, provider/model routing, health checks, retry/fallback, rate-limit handling, and token accounting.

## GitHub repositories investigated

AI gateway candidates:
- artzy/OmniRoute — already installed on mh-dev-01 as OmniRoute 3.8.50; first candidate to test rather than introducing another gateway.
- BerriAI/litellm — mature multi-provider gateway candidate.
- broven/AIGate — multi-provider gateway/fallback candidate.
- adcwb/ai-gateway — compact self-hosted gateway with multi-provider balancing/failover.
- songquanpeng/one-api / related forks — unified multi-provider API gateway candidates.
- qingchunnh/new-api — broader gateway/project candidate; requires security/repository provenance review before adoption.

Network candidates:
- juanfont/headscale — self-hosted WireGuard mesh control plane.
- SagerNet/sing-box — policy routing/DNS/networking layer; use only if complex routing is actually needed.
- netbirdio/netbird — self-hosted WireGuard-based mesh candidate.
- gravitl/netmaker — WireGuard mesh/network management candidate.
- WireGuard itself remains the simplest possible private tunnel layer.

## Current provider evidence relevant to this architecture

Previously qualified:
- Cloudflare Workers AI: 2 provider accounts/models passed inference qualification in provider qualification evidence. This is not by itself proof of regional/contractual suitability; that must be checked separately.
- Local Ollama: qwen2.5-coder:3b generation qualified.
- UnoRouter: latest dedicated live catalog showed 252 models; credential/catalog access worked, but latest gpt-oss-120b:free inference evidence returned HTTP 503. Do not treat inference as currently confirmed without a fresh test.
- ZeroRouter: latest dedicated catalog showed 36 models; credential/catalog access worked, but gpt-5.4 and claude-sonnet-5 inference returned HTTP 402 BLOCKED_BILLING. Current usable inference capacity is therefore 0 based on that evidence.
- SiliconFlow current SILICON_KEY_2 replacement: isolated curl probe received HTTP 401. Do not claim usable authentication.

## Important design distinction

A gateway/proxy/VPN can:
- centralize API access;
- route requests through selected infrastructure;
- provide failover and load balancing;
- connect private servers securely.

It cannot legitimately turn a provider-rejected regional/account credential into an accepted credential. Each upstream must be independently qualified for actual use and applicable provider terms.

## Target

Investigate whether existing open-source components can provide:
1. AI multi-provider routing;
2. provider/model fallback;
3. private server-to-server mesh;
4. DNS/policy routing where needed;
5. ephemeral secret use sourced from GitHub Actions/GitHub Secrets;
6. token/latency/error accounting;
7. automatic failover;
8. measurable aggregate daily capacity.

The earlier 50M tokens/day figure is a target/hypothesis, not yet verified capacity. It must be calculated from fresh observed quotas/throughput of qualified providers.

## Next work

Do not modify GOLD #176.

Run a read-only compatibility comparison of:
- OmniRoute 3.8.50 (first choice because already installed)
- LiteLLM
- AIGate / adcwb/ai-gateway

Then compare network options:
- Headscale + WireGuard
- NetBird
- Netmaker
- plain WireGuard

Acceptance checks:
- no persistent API secrets on server disk;
- one gateway endpoint for Astra;
- at least two independently qualified upstreams;
- deterministic fallback;
- streaming/API compatibility required by Astra;
- observable token counts and latency;
- isolated test environment;
- no impact to canonical GOLD #176.

Only after the comparison should installation/activation be considered.
