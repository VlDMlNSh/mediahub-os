# Wave 261 — Ready-made cloud pool components and multi-agent platforms (2026-10-20)

## Outcome
Expanded the accepted development plan: the cloud pool must not be implemented as a bespoke collection of provider adapters alone. The work must actively select, evaluate and integrate mature existing multi-agent orchestration platforms, reusable agent skills/workflows, provider gateways, job/queue and evidence components, and later the components needed for a controlled agent corporation. The rule is **reuse first, custom code only for gaps**.

This is an inventory/architecture decision. No third-party software was installed or integrated, no provider was called, and no agent was dispatched.

## Evidence checked
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Cloud-fabric governing Issue #301 remains OPEN: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Existing provider/model registry on `main`: `ops/qualification/provider_model_registry.json`, blob SHA `62328126fd2cd8879a73bb6812adcacd3e2abe84`. It contains 25 provider records (24 selection-order entries plus local Ollama), but entries are candidates/configuration, not proof of entitlement, valid credentials, current model availability or operational qualification. Do not create a duplicate registry.
- Functional Baseline 2.0 on `main`: `docs/checkpoints/mediahub-functional-baseline-2.0.md`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; it remains accepted/canonical. This plan does not modify it.
- Upstream candidate found: [Microsoft Agent Framework](https://github.com/microsoft/agent-framework), MIT license per GitHub repository metadata, description states framework for building, orchestrating and deploying agents and multi-agent workflows in Python/.NET. Candidate only; version/security/release maturity and compatibility with MediaHub contracts still require review.
- “ECC” is ambiguous. A possible meaning is [Everything Claude Code](https://github.com/affaan-m/everything-claude-code), but the requested abbreviation has not been authoritatively resolved in project artifacts during this wave. Keep it as a candidate pending exact project/repository identification; do not silently assume it is the intended system.
- Repository search results surfaced other orchestration candidates, including [OpenSwarm](https://github.com/VRSEN/OpenSwarm), [Agency Swarm](https://github.com/VRSEN/agency-swarm), [Microsoft Agent Framework](https://github.com/microsoft/agent-framework), and [OpenAI Swarm](https://github.com/openai/swarm). Search discovery alone is not a recommendation or security review.

## Required component workstreams

### A. Existing multi-agent systems / agent harnesses
Create a shortlist and evaluate upstream stability, license, recent maintenance, installation footprint, provider flexibility, task isolation, human approval gates, cancellation/recovery, observability, prompt-injection handling, reproducibility, CI, secret handling and ability to run on ephemeral GitHub-hosted workers. Evaluate ECC after its identity is confirmed. Prefer integration as a bounded subsystem over granting a framework authority over MediaHub state.

### B. Provider gateway and model routing
Compare using the existing provider registry and its consumers first. A gateway/router can standardize OpenAI-compatible endpoints, provider health/quota signals, per-task model selection and fallback policy, but cannot bypass the registry, provider terms, budget, issuer/capability or data-route controls. Validate the existing provider records before adding more: several names and model identifiers are time-sensitive and must be verified against official sources at admission time.

### C. Durable job orchestration and queue
Reuse a mature queue/workflow component only if it supports idempotency, bounded retries, lease/expiry, cancellation, replay-safe transitions, dead-letter handling, and auditable terminal states. GitHub Actions remains the approved initial execution surface; do not add a second scheduler/dispatch path that bypasses the controller. A future queue service must be explicitly authorized and qualified.

### D. Evidence, observability and policy enforcement
Select or build around existing standards for task envelopes, provider registry, evidence manifests, structured logs, run/job IDs, artifact digests, policy decisions, redaction, quota/cost accounting, and audit. Enforce strict allowlists, isolated workspaces, immutable source SHA, pinned actions/dependencies, output quarantine, and independent verification before patch promotion.

### E. “Agent corporation” capabilities
Treat corporation as a governed organizational model, not unconstrained autonomous access. Evaluate ready-made components for role/team definitions, task decomposition, delegation, dependency tracking, shared workspaces, review/approval, memory with provenance, budget and quota allocation, escalation, rollback, and auditable decision logs. Each role gets least privilege and a bounded capability; no agent can grant itself new authority or mutate canonical product state outside its designated authority.

## Architecture guardrails
- Reuse the existing `ops/qualification/provider_model_registry.json`; establish its full consumer map before schema changes.
- One approved controller and issuer/capability boundary; no direct provider/agent dispatch through SentinelX, ad-hoc scripts or side workflows.
- Separate provider adapters from orchestration frameworks; avoid coupling the canonical product state to any one vendor/framework.
- Provider routes remain disabled/unqualified until official access/terms/quota/model evidence, schema/negative tests, security review, runtime evidence and revocation/failure drills pass.
- Never infer “free forever” from a `cost_class` field. Record observed tier, limits, expiry/reset semantics and evidence date separately.
- Local executors and Jarvis component selection begins only after the cloud pool is deployed and independently operationally accepted. Their deployment needs separate full qualification. Contour B remains gated until Contour A independent acceptance.

## Next bounded action
Build a source-backed candidate comparison matrix and map all consumers of the existing provider registry. Resolve the intended “ECC” repository by exact name/URL from the project's prior source artifacts, then evaluate the smallest integration seam that can be tested without provider calls or agent execution.

## Non-actions
No package install, third-party code import, provider call, credential access, Gemini launch, workflow dispatch, merge, deployment or qualification occurred.
