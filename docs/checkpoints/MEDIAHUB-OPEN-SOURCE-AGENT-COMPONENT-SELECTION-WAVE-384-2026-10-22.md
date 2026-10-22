# MediaHub OS — open-source agent architecture component selection (Wave 384)

Date: 2026-10-22

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

Related engineering work: [PR #483](https://github.com/VlDMlNSh/mediahub-os/pull/483). This research branch is separate from that implementation PR and is not canonical or accepted until reviewed/merged.

## Decision

Do not build a general multi-agent framework from scratch and do not adopt several competing frameworks wholesale. Keep MediaHub's issuer, capability, queue admission, routing, signed dispatch, product-state authority and evidence contracts as the governing layer. Select at most one primary orchestration library; add independent components only where they provide a distinct capability and pass contract, license, security and CI review.

## GitHub versus physical/server installation

- Code, contracts, tests and workflow definitions can live in the GitHub repository.
- GitHub Actions hosted runners can execute bounded jobs without using a permanently running physical server. They are ephemeral workers, not a continuously running daemon.
- GitHub Actions alone does not provide a general-purpose transactional, durable queue with atomic leases, idempotency, cancellation races and long-lived state. Artifacts and Issues alone are not sufficient as a production scheduler/database.
- If the requirement is strict GitHub-hosted execution, the supervisor can run in Actions, but durable state still needs an explicitly qualified store/protocol. A managed database is an option only if an external managed dependency is acceptable; otherwise a GitHub-native append-only ledger needs a separately proven concurrency/recovery design.
- The third server remains an execution-only local worker. It must not become the scheduler, a Gemini transport, an alternate issuer or a way around controller gates.

## Candidate shortlist (not yet approved for installation)

| Candidate | Verified repository facts at review time | Potential component to reuse | Limitations / decision |
|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | MIT; active, non-archived; Python/JS ecosystem; repo metadata showed recent activity on 2026-10-22. | Stateful graph execution, checkpoints, explicit transitions and resumable agent workflows. | Primary orchestration candidate A. Prototype against MediaHub task envelope and recovery contract. Do not let it replace issuer/capability checks or the outer queue. |
| [CrewAI](https://github.com/crewAIInc/crewAI) | MIT; active, non-archived; recent activity on 2026-10-22. | Role-oriented agent team definitions and flow composition. | Primary orchestration candidate B / comparison only. Compare task delegation and auditability against LangGraph; do not adopt both as competing core schedulers. |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | MIT; active, non-archived; Python/.NET; recent activity on 2026-10-22. | Built-in multi-agent workflow patterns and handoffs. | Primary orchestration candidate C / comparison only. Evaluate API and dependency footprint; avoid simultaneously adding three orchestration runtimes. |
| [Temporal](https://github.com/temporalio/temporal) | MIT; active, non-archived; service repository with recent activity on 2026-10-22. | Durable workflow semantics, retries, timers and recovery patterns. | Strong design reference or managed-service candidate, but a full Temporal deployment is additional persistent infrastructure, not a library that makes GitHub Actions permanently stateful. Not a strict GitHub-only fit without a managed service. |
| [Langfuse](https://github.com/langfuse/langfuse) | Repository LICENSE grants MIT to content outside specified EE directories; EE content has a separate license. | Tracing, evaluation and inspection of model/agent runs. | Optional observability layer, not queue/orchestration. Audit the exact directories and transitive dependencies before copying code. |
| [promptfoo](https://github.com/promptfoo/promptfoo) | MIT; active, non-archived; recent activity on 2026-10-22. | CI-driven prompt/agent evaluations and security/red-team tests. | Strong independent test-layer candidate; must run with synthetic/non-secret fixtures by default and never dispatch live agents from tests. |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | Repository LICENSE is Elastic License 2.0 (ELv2), not MIT/Apache-2.0. | Observability/evaluation concepts. | Do not select for code reuse until legal review confirms intended use; ELv2 restrictions make it a weaker fit for an unrestricted open-source component strategy. |

Repo metadata and license files were read directly from GitHub on 2026-10-22. Stars and recent activity are signals, not acceptance criteria. Version pinning, dependency health, security advisories, transitive licenses, maintenance response and integration tests remain to be checked before adoption.

## Proposed target composition

1. Astra Gold A0 / issuer — validates caller, signed task envelope, immutable target SHA, capabilities, scope, provider/model policy, budget, expiry, cancellation and idempotency.
2. GitHub-hosted supervisor — owns task state transitions, dependency resolution, scheduling, retry/backoff, timeouts, cancellation, audit and result collection. No permanent runner hostname is assumed for control-plane logic.
3. Existing signed Gemini controller — remains the only permitted Gemini dispatch route. It dispatches only the three allowlisted child workflows and verifies HMAC/provenance. The current controller's task text is fixed to general role prompts; it has not been verified to accept arbitrary topic-specific work items from this chat. A reviewed controller change is required before passing these research sub-tasks.
4. Primary agent framework — initially evaluate LangGraph, CrewAI and Microsoft Agent Framework with the same synthetic workload and acceptance tests; choose one or choose none if the existing runtime is smaller and safer.
5. Durable state — explicitly select and test a persistent store/ledger for leases and idempotency. Do not treat workflow artifacts, caches or an Issue checklist as a transactional queue.
6. Verification layer — promptfoo and/or existing Python contract tests for replay, invalid signatures, wrong target SHA, scope escape, duplicate dispatch, provider/budget mismatch, cancellation races and poisoned artifacts.
7. Observability layer — evaluate Langfuse only after data-retention, privacy, license and secret-redaction requirements are established.
8. Local worker on Voktors-Mini.Dlink — executes only an authorized task addressed to its registered identity, with lease/expiry and signed result evidence. It does not host the supervisor or route Gemini.
9. Jarvis and Product State Authority — remain separate authority domains; no framework receives authority by configuration accident.

## Shared acceptance workload for future comparison

Run each candidate against the same deterministic, non-secret fixture and immutable target SHA:
- create a two-step task dependency;
- resume after a simulated process interruption;
- reject a stale target SHA and replayed dispatch;
- enforce capability/scope and cancellation;
- collect a result manifest with provenance;
- show a complete audit trace without exposing secrets;
- demonstrate no live provider dispatch in unit/PR tests.

Compare recovery correctness, inspectability, extension points, dependency footprint, testability, license, security posture and integration cost. Do not select by stars or marketing claims alone.

## Three proposed parallel research tasks

These are task specifications only; they were NOT DISPATCHED in this pass.

- Agent 1 — implementation research: compare LangGraph, CrewAI and Microsoft Agent Framework integration seams against the current MediaHub task envelope and queue runtime; produce a file/contract mapping and minimal prototype proposal. No code changes to canonical branches.
- Agent 2 — independent verification: verify licenses, releases, dependency and maintenance signals; define a reproducible, secret-free comparison fixture and test matrix; report exact repository refs and evidence.
- Agent 3 — security/provenance audit: threat-model importing third-party orchestration code, identify authority/secret/logging boundaries, review ELv2/EE licensing distinctions, and propose negative tests.

The existing controller contains fixed task prompts for generic implementation, contract verification and security audit. It does not currently accept these three topic-specific prompts as independently selected jobs. Do not claim they were delivered to agents or bypass the controller. Controller admission, exact-head CI, independent review and effective secret/governance checks must pass before a real batch.

## Status and next step

- Candidate research: INITIAL SCREEN COMPLETE / NOT QUALIFIED FOR ADOPTION.
- Framework selected for production: NONE.
- Component copied or installed: NONE.
- Three research agents: PLANNED / NOT DISPATCHED.
- PR #483 exact-head CI after the hygiene-test parser fix: VERIFIED PASS on head 9d55150cc6ec5fdff14a6c6b798faf30601c8b22. Astra Verify run [39816945698](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39816945698), job 119957782575, completed with 469 tests OK; Cloud Runtime Validation run [39816945791](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39816945791), job 119957784151, completed successfully with 12 admission/failover tests passed. This is CI evidence only, not independent review or acceptance.
- PR #483 formal independent review: NOT VERIFIED.
- Contour A / production supervisor: NOT QUALIFIED / NOT ACCEPTED.

Next: build the same deterministic, non-secret benchmark fixture for LangGraph, CrewAI and Microsoft Agent Framework, then compare recovery, auditability, dependency footprint, license and integration cost. Do not merge this research branch or install dependencies before review.
