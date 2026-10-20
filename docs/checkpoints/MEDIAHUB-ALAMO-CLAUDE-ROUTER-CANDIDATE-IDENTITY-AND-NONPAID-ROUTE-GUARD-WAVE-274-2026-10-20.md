# Wave 274 — Alamo Claude router identity and non-paid route guards (2026-10-20)

## Status and authority

**Owner-clarification follow-up / source identity review / documentation only.** This report supplements the binding Wave 273 requirements; it does not create a second architecture decision, amend Functional Baseline 2.0, select a router, approve an authentication mode, qualify a route, or authorize provider/host/secret operations.

## Owner's routing clarification

ASTRA GOLD A0 remains the single coordinator for authorized hybrid missions. A0 decomposes work into bounded, dependency-aware subtasks and dispatches only to admitted destinations: the independent GitHub-hosted cloud pool, admitted user-owned MediaHub devices/instances, and admitted local executors. A0 owns DAG scheduling, queue/claim/lease, retry, cancellation, recovery, handoff/fencing, cross-route reconciliation, and evidence aggregation. A3 independently verifies completed work.

For this target, Claude Code on Alamo is a local executor/client only. The Alamo route MUST NOT use the Anthropic API directly or indirectly, paid Anthropic API credentials/authorization/billing, any paid backend hidden behind a proxy/router, paid fallback, or silent rerouting. It must not repurpose subscription credentials, bypass provider authentication/terms/quota/account eligibility/identity controls, or misrepresent third-party inference as Anthropic Claude. Running the Claude Code client on Alamo does not prove that inference is local.

## Candidate identity findings

These names are a candidate list for source-bound evaluation, **not approved routes**:

| Candidate family | Public source evidence found | Current disposition |
|---|---|---|
| FCC / `fcc-claude` | [Factix/fcc](https://github.com/Factix/fcc) describes an Anthropic-compatible client proxy with free, paid, and local provider options. Public forks also exist. | Candidate only. An explicit provider/model allowlist and disabled paid/unknown fallback are mandatory; exact upstream/fork and version are not selected. |
| FreeLLMAPI | [lov0u/freellmapi](https://github.com/lov0u/freellmapi) and separate similarly named repositories exist; [freellm-claude-code-router](https://github.com/RobinHoodO/freellm-claude-code-router) describes a distinct adapter that depends on a FreeLLMAPI backend. | Candidate only. Neither the name nor an Anthropic-compatible API shape proves the backend, authorization basis, zero cost, policy permission, or locality. Exact project and upstream graph remain unresolved. |
| OmniRoute | Public repositories/forks with the same or similar name exist, including [rgplvr/omniroute](https://github.com/rgplvr/omniroute) and [artzy/OmniRoute](https://github.com/artzy/OmniRoute). Their descriptions include multi-provider routing and fallback. | Candidate only. Canonical upstream/fork/version must be pinned. Any mixed free/paid provider pool must be constrained so the Alamo route can reach only admitted non-paid endpoints and cannot fall back to paid or unknown providers. |
| OpenFlux | The name is ambiguous in available public search results. Examples found include [sdmeth/openflux](https://github.com/sdmeth/openflux), described as a network-stack/tunnel research tool, and [the PyPI openflux package](https://pypi.org/project/openflux/), described as local Claude Code usage/cost tracking. Neither result establishes the intended free-auth/router capability. | **UNIDENTIFIED / NOT ADMITTED.** Do not infer the intended project or role from the name. A precise repository URL, owner/project identity, version and relevant source must be established before review. This finding does not claim that no other project with this name exists. |

## Admission requirements for every router path

Before any route can be admitted, evidence must pin: exact upstream repository/ref or release digest; installed build/configuration identity; actual authentication mechanism and its explicitly permitted basis; applicable terms and account/automation restrictions; provider/model allowlist; the entire transitive upstream and fallback graph; verified zero-cost/non-paid class and quota semantics; credential source/scope/handling; network egress and data retention; Alamo host binding; and fail-closed behavior on missing, revoked, ambiguous, or paid route state.

The configuration and tests must **deny by default**: direct/indirect Anthropic API access; paid Anthropic API authorization/credentials/billing; all paid or unknown backend/fallback paths for the Alamo route; ambiguous router/upstream identities; unsupported or terms-incompatible account-auth flows; silent failover; credentials in logs/artifacts; and a claim of local inference without evidence. A free tier or provider-issued credential may be considered only where the provider's applicable terms expressly permit the intended use. No account, identity, subscription, quota, access-control or billing bypass is permitted.

## Source and project state

- Canonical architecture requirements: [A0 hybrid dispatch and Alamo Claude routing hard requirements](../architecture/MEDIAHUB-A0-HYBRID-DISPATCH-AND-ALAMO-CLAUDE-ROUTING-HARD-REQUIREMENTS.md), updated in this wave to name the additional candidate families.
- Prior binding owner clarification: [Wave 273 report](MEDIAHUB-A0-FREELLMAPI-FCC-ALAMO-CLAUDE-HARD-ROUTE-REQUIREMENTS-WAVE-273-2026-10-20.md).
- Current routing candidate `ops/agent-fabric/providers/local-executor-routing-v2.yaml` on `main`, blob `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`, lists FCC and OmniRoute candidate lanes but is qualification-gated; it does not include an explicit FreeLLMAPI lane or prove runtime admission.
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`; observed branch HEAD before Wave 274 writes: `1b116bc1af3398a786644b36b10fed55e3da7928`. Observed `main` HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) is OPEN. PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421) is OPEN/DRAFT at head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`. Branch protection remains unverified from the prior documented 403; this Wave does not alter PR/CI gates.

## Work performed and not performed

Performed: public source identity search, current repository ref/file read-back, and documentation planning. The source descriptions establish candidate features only, not security, policy, route-cost, Alamo binding or production behavior.

Not performed: tests, package installation, router/provider invocation, credential access, host inspection, agent dispatch, merge, deployment, live qualification, or acceptance. Runtime enforcement remains **NOT VERIFIED**; the Alamo route and Contour A remain **NOT_PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.

## Write/read-back evidence — Wave 274

- Initial report creation commit: `dd6f6456a42b153aaeef38853421bd3849152428`.
- Map addendum commit / read-back blob: `004f76541c0d9f6b3dd87af5aa7bf08d9f4bf40e` / `168e5ad76ca9ce453fc576eb851454ef530353ce`.
- Architecture contract update commit / read-back blob: `e4c4aef22076a79a8580d6b1821c974ab781cd65` / `66aeb9c5521a698fc2ff1faba46c35906ea52bcf`.
- Canonical map update commit / read-back blob: `ad8dd327e0fd3120b2c5ee395ba4477c5cf84486` / `e3adde9ebf53d46e9a355ece400dedc16b9ee588`. The full map blob was read by SHA because the file endpoint returned empty content; read-back preserved the prior content and added Wave 274.
- Master roadmap update commit / read-back blob: `744d0aa5e5fa1122dab09c751398932476d4d252` / `8b8d273fc703c769d571abcb7cb3a6af1177c9f3`.
- Before checkpoint reconciliation, canonical documentation branch HEAD was `744d0aa5e5fa1122dab09c751398932476d4d252`; `main` HEAD was `80be45a70732b1d568164571d4273a6397792c3b`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301): OPEN. PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421): OPEN/DRAFT, head `84e2d0bbb4163942f5ba010591cb5d3c9d6a7581`, base `80be45a70732b1d568164571d4273a6397792c3b`.
- Contract and map read-backs confirm the named candidate families and the no-paid/unknown-route boundary. These are documentation identities only, not runtime proof.

## Next bounded step

Trace the authoritative A0 task-contract writer and trusted issuer/admission lifecycle; map destination, router identity, auth/cost class, upstream graph and fallback restrictions to existing contracts; then add schema/static/mock-only negative tests. Do not use live routers/providers or inspect Alamo until their applicable capability, security, provider-policy and qualification gates pass.

## Navigation

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 274 map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-274-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
