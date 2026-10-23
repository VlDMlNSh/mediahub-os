# MediaHub OS — Wave 399: owner approval reconciliation and free-route admission boundary

Date: 2026-10-23

## Decision

**OWNER APPROVAL RECORDED / IMPLEMENTATION DESIGN READY FOR ROUTE PINNING / WORKFLOW NOT CREATED / DISPATCH NOT RUN**

The owner approved preparing a separate PR for GitHub-hosted ephemeral Claude Code + FCC with no paid Anthropic fallback in [Issue #301 comment 6354035391](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6354035391). This supersedes the earlier Wave 398 statement that owner approval was still pending. The approval expressly requires only explicitly allowed free provider/model routes and says it does not authorize live dispatch, merge, deployment, or Contour A acceptance.

The approval does **not name an exact provider/model route**. I did not infer that a catalog entry labelled “free” is an authorized MediaHub route, because the canonical route policy was tightened in merged [PR #458](https://github.com/VlDMlNSh/mediahub-os/pull/458) after direct provider routes were found nonconforming. Therefore no workflow was added and no provider was called.

## Immutable source refs and upstream evidence

- MediaHub `main`: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- Canonical docs branch before Wave 399 writes: `35a52ec2915c34fd4c946dc565f7327ec48d285c`.
- Owner authorization: [Issue #301 comment 6354035391](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6354035391).
- Route-policy remediation: [PR #458](https://github.com/VlDMlNSh/mediahub-os/pull/458), merged at `11d04d2f2687e9ba9215e4b67af2e450516960bb). Its stated contract was Gemini cloud agents through the controller, Claude/Ollama on a separately qualified local lane, and no unapproved/paid fallback. The new owner decision authorizes designing a new FCC route but does not erase the need to pin its exact model/provider contract.
- FCC upstream: [repository](https://github.com/Alishahryar1/free-claude-code), license AGPL-3.0-only, current upstream main commit observed `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`, latest release observed `v6.16.16` ([release](https://github.com/Alishahryar1/free-claude-code/releases/tag/v6.16.16), published 2026-10-21). Pin a reviewed release/commit in any implementation; do not pipe an unpinned `main` installer into a runner.
- FCC README provider catalog lists free-labelled model aliases such as `open_router/openrouter/free`, `kilo/kilo-auto/free`, `tokenrouter/moonshotai/kimi-k3-free`, and `nararoute/kimi-k3-free`. These are **candidates only**, not selected/approved MediaHub routes, and their live availability/terms were not verified.
- FCC README states an optional ordered `MODEL_FALLBACKS` list can route failed requests to more than one provider and consume usage across them. The implementation must set no fallback list and add a source-level/tested invariant that rejects configured fallbacks for this worker; it must also verify provider-side aliases cannot silently route to paid models. The latter has not yet been established for any candidate.
- Existing MediaHub worker [mediahub-claude-worker.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mediahub-claude-worker.yml), blob SHA `e1260cfef88ac02bcc9d0cce67bb497820f5f63c`, remains metered Anthropic and is not a substitute.

## Implementation gate

Before creating the workflow, the route must be pinned to one exact provider/model identifier, with evidence for:
1. provider/model eligibility under the free tier and applicable terms;
2. provider-side no-paid-fallback semantics;
3. FCC config that allows exactly that model and no configured fallback list;
4. exact secret names (if any), minimum permissions, and credential-free logs;
5. immutable FCC release/commit and reproducible install;
6. negative tests proving missing route, invalid model, exhausted quota, and provider errors terminate without retrying another provider.

Once a route is pinned, a separate PR can add the disabled-by-default, GitHub-hosted worker and tests. That PR must not dispatch the worker or expose `ANTHROPIC_API_KEY`; it needs independent review and exact-head CI before any separately approved qualification run.

## Verification

- Re-read owner approval comment and current main SHA.
- Re-read FCC README, provider catalog, settings model and fallback validation source; confirmed fallback is an explicit optional list and README documents multi-provider behavior.
- No code or workflow changed; no workflow dispatched; no provider/model invoked; no secret values read.
- Exact route admission: **BLOCKED pending named provider/model and verified no-paid-fallback contract**.
- Execution: **NOT RUN**. Qualification/acceptance: **NOT VERIFIED**. Contour A: **NOT ACCEPTED**.

## Next step

Record the exact provider/model route that should be used (choose one candidate above or name another FCC-supported free route). Then pin and test its no-paid-fallback behavior before implementing the workflow.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
