# MediaHub OS — GitHub-Hosted Model Coordinator Proposal, Wave 61

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **PROPOSED / DOCUMENTATION ONLY / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACTIVATED**
- Repository: `VlDMlNSh/mediahub-os`
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Predecessors: Wave 44 provider credential reference audit; Wave 45 GitHub Actions-only cloud router ADR; Wave 60 GitHub-hosted key rotation and egress design.

## 1. Decision proposed

Implement the smallest coordinator as a GitHub-hosted Actions workflow, with GitHub Issues as the durable task inventory and a dedicated versioned branch as the redacted quota/cooldown ledger. Use explicit provider adapters and statically reviewed secret mappings. The coordinator runs on GitHub-hosted ephemeral runners only.

This is a design proposal. It grants no authority to dispatch the workflow, call providers, use credentials, activate schedules, run tests or qualification, or promote the router.

## 2. Existing-component fit

- Reuse `ops/qualification/provider_model_registry.json` as the provider/model catalog. It currently describes 24 selection-order entries plus the local Ollama entry; the registry is candidate metadata, not proof of eligibility or quota.
- Reuse the existing Gemini workflows as examples of GitHub-hosted execution and explicit secret mapping. Their per-run concurrency groups do not serialize independent agents and they do not establish shared cross-provider quota failover.
- Keep `ops/qualification/astra-provider-qualification.yml` in its separate self-hosted lane. It is outside the cloud-router execution boundary.
- Do not deploy LiteLLM as a persistent gateway. Do not add a database, serverless runtime, self-hosted runner, or owner-operated server to cloud routing.
- The current map/checkpoint identify A0, MH-12, R-06 and target-manifest admission as open activation gates.

## 3. Proposed workflow topology

1. **Task intake:** an approved issue label identifies candidate tasks. Parse a versioned, bounded task envelope; issue content is untrusted input.
2. **Authorization gate:** validate actor/issuer, task schema, allowed contour, data-egress class, provider/model allowlist, deadline, maximum attempts and output budget. Unknown authorization fails closed.
3. **Coordinator:** one stable global concurrency group for quota-sensitive work; process a bounded batch. A run is a worker, not the durable queue.
4. **Candidate selection:** consult the existing provider registry and a reviewed eligibility manifest. Exclude candidates with unknown cost/quota scope, unverified secret alias, incompatible model, policy mismatch or unknown egress eligibility.
5. **Credential injection:** explicit reviewed workflow/job mappings only. Task content, issue text and model output may never choose secret names or secret values.
6. **Provider adapter:** one provider call per selected attempt, bounded timeout and retry budget. Provider invocation remains disabled until separately authorized.
7. **Outcome and evidence:** write sanitized task status and evidence references; never write credentials, authorization headers, credential-bearing URLs or sensitive raw bodies.
8. **Reconciliation:** a future scheduled/manual reconciliation scan may recover stale tasks and cooldowns after its own activation gate. Scheduled activation is out of scope for this proposal.

## 4. Task envelope — proposed v1

Required fields:
- `schema_version`
- immutable `task_id` and idempotency key
- originating issue number and accepted issuer/authorization evidence
- bounded task description/reference set
- contour and data-egress classification
- explicit allowed provider IDs and model IDs
- deadline, maximum attempts, timeout and output token/byte budget
- permitted result destination (issue comment, artifact reference, or task-scoped PR)
- terminal state and evidence references

Validation rules:
- Reject unknown schema versions, unapproved providers, missing egress classification, excessive budgets, malformed identifiers and unexpected fields.
- Treat repository content, issue text, comments, branches and model output as data, never as executable workflow instructions.
- Do not expose secrets to fork-originated or otherwise untrusted code.
- Engineering agents may create task-scoped branches/PRs only within explicitly granted permissions; merge and release authority remains separate.

## 5. Quota ledger — proposed v1

Suggested record key:
`provider_id + upstream_account/project/organization_scope + model_id + metric + reset_window`

Suggested fields:
- schema version and ledger revision
- provider and upstream quota-scope alias (never a credential value)
- model and metric names (RPM/RPD/TPM/TPD or provider-defined equivalent)
- documented reset/cooldown timestamp and observed Retry-After metadata
- sanitized counters and provenance timestamp
- eligible/quarantined/deferred state and reason code
- task IDs and sanitized outcome references

Rules:
- Credential aliases sharing an upstream quota scope share the same ledger entry.
- Distinguish provider-reported usage, locally estimated usage and unknown usage; do not present estimates as authoritative provider counters.
- On 429, honor documented Retry-After/reset metadata and persist a scope-level cooldown.
- Authentication, authorization, billing, policy, unsupported-model and transient transport failures have distinct classifications.
- Missing, stale, malformed, corrupt or conflicting ledger state quarantines that scope and defers the task.
- Update the state branch against observed ref/blob SHA with bounded optimistic-concurrency retries. A conflict never permits fail-open routing.
- Serialize quota-sensitive calls in the first implementation. Per-provider parallelism requires separate concurrency evidence.
- GitHub Actions concurrency is a guardrail, not a FIFO queue. Issues remain the durable task inventory; reconciliation rescans all eligible tasks.

## 6. Routing and fallback rules

1. Prefer the first policy-approved candidate whose model, account scope, quota window, cost class and data-egress conditions are evidenced.
2. Use another provider only when its quota scope is independently eligible and the task explicitly permits that provider and its retention/data-egress policy.
3. When all allowed routes are exhausted, record `QUOTA_EXHAUSTED` and defer to the earliest evidenced reset or a later reconciliation pass.
4. Paid routes remain disabled unless separately approved for the specific task and scope.
5. Local Ollama is a separate execution target, never cloud capacity. Cloud-to-local switching requires an explicit route decision and separate data-egress review.
6. Do not rotate credentials, accounts, IP addresses or egress paths to evade upstream limits or eligibility controls.
7. Check existing task/branch/PR evidence before retries to reduce duplicate engineering work.

## 7. Provider admission manifest

Before a provider enters the runtime allowlist, record:
- stable provider ID and exact API/model identifiers
- authoritative pricing/free-tier source and access expiry/conditions
- actual upstream quota scope, metrics, reset semantics and 429 behavior
- GitHub-hosted runner egress eligibility under provider terms
- credential secret *name reference* and confirmed owner-side presence status; never record the secret value
- retention/training/privacy terms and approved data-egress classes
- request/response redaction rules and bounded retry policy
- evidence revision, review date, status and reviewer

The SiliconFlow alias discrepancy remains open: probe workflows reference `SILICON_KEY_2`, while the registry/qualification path references `SILICONFLOW_API_KEY_2`. Keep both routes quarantined until owner-side alias reconciliation is evidenced.

## 8. Activation gates

Runtime activation requires separate evidence and authorization for all of the following:
- A0 task ingress/lifecycle and issuer authorization accepted.
- MH-12 tool and role enforcement accepted.
- R-06 audit, privacy, retention and data-egress disposition accepted.
- Target manifest explicitly confirms GitHub-hosted runners for every cloud job.
- Provider/model/account/free-tier and GitHub-runner egress admission complete.
- Secret alias mapping and secret-presence status reconciled without exposing values.
- Task and ledger schemas reviewed, including negative/invalid fixtures.
- Concurrency, idempotency, stale leases, duplicate PRs, corrupt state and recovery independently reviewed.
- Explicit approval for provider calls, workflow dispatch, tests, qualification, schedules and activation.

Until then, the coordinator is documentation-only and any runtime entry point must remain unavailable or fail closed.

## 9. Review checklist for a future implementation PR

- [ ] Only GitHub-hosted runners appear in cloud jobs.
- [ ] No provider call is reachable before authorization and admission checks.
- [ ] No arbitrary issue text enters shell source, YAML, secret selection or executable prompts.
- [ ] Provider IDs and secret mappings are static, reviewed and allowlisted.
- [ ] Ledger writes use expected revision/ref and fail closed on conflict.
- [ ] Secret redaction covers logs, annotations, artifacts, issue comments and URLs.
- [ ] 429/reset, auth, policy, billing, unsupported-model and transient failures are handled distinctly.
- [ ] Retries are bounded and idempotent; duplicate branch/PR detection exists.
- [ ] Paid fallback and cloud-to-local fallback are disabled by default.
- [ ] Manual dispatch, provider calls, scheduled reconciliation and activation each have explicit gates.
- [ ] Independent verification evidence is attached before any qualification claim.

## 10. Evidence boundary and next step

This pass used GitHub source and metadata reads only. No secret values were read; no provider/model calls, workflow dispatch, tests, qualification, installations, host/runtime inspection, infrastructure changes, deployment or merge occurred.

**Next bounded step:** source-map the A0, MH-12, R-06 and target-manifest acceptance clauses to concrete paths and evidence fields. Once those gates and separate authorization are satisfied, prepare a distinct implementation PR. Do not bundle runtime activation into this proposal.

Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
