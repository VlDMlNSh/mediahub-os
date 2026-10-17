# MediaHub OS — GitHub-Hosted Key Rotation and Egress Design, Wave 60

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE TRACE COMPLETE / ROUTING DESIGN PROPOSED / RUNTIME UNQUALIFIED**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Related Wave 59: [Gemini Secret Wiring and Agent-Fabric Consumer Trace](MEDIAHUB-GEMINI-SECRET-WIRING-AND-AGENT-FABRIC-CONSUMER-TRACE-WAVE-59-2026-10-17.md)
- Related architecture: [GitHub Actions-only Cloud Router ADR — Wave 45](../architecture/MEDIAHUB-GITHUB-ACTIONS-ONLY-CLOUD-ROUTER-ADR-WAVE-45-2026-10-17.md)

## 1. Owner constraint recorded

All cloud-model work, provider API calls, credential selection, quota accounting, retries, and agent orchestration run exclusively on GitHub-hosted Actions runners. No owner-operated server, self-hosted runner, always-on proxy, external database, or serverless runtime participates in the cloud lane.

The user's physical location, mobile carrier, home/office network and local public IP are not routing inputs. Outbound provider requests originate from the GitHub-hosted runner's network path. Provider-side account, region, IP and terms restrictions remain relevant: a provider that rejects that egress path is quarantined for this route. No proxy or egress rotation may be used to evade provider restrictions.

Servers remain available for local inference and local computation only. Switching a task from cloud execution to local execution requires an explicit route decision and data-egress review.

## 2. Exact workflow evidence

| Workflow | Runner | Credential mapping | Source SHA | Finding |
|---|---|---|---|---|
| [Gemini Autonomous Engineering](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-autonomous-engineering.yml) | ubuntu-latest | GEMINI_API_KEY | 09523d809530ae5b7bf528eab5fa53bc5deaf92d | One explicit key; no cross-key rotation logic observed |
| [Gemini Agent 2](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-2.yml) | ubuntu-latest | GEMINI_API_KEY_2 | 6c59d42f0777ffbe4528594a756f9839e81a6726 | One explicit key; no shared quota ledger observed |
| [Gemini Agent 3](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-3.yml) | ubuntu-latest | GEMINI_API_KEY_3 | 44ef9aeb8bcc8607bc4c07fe62fc4c56baa69d1e | One explicit key; no shared quota ledger observed |

All three workflows declare a concurrency group containing both workflow identity and github.run_id. That provides no global mutex across independent runs or agents. A shared coordinator requires a stable concurrency group, while the durable queue remains an issue inventory because Actions concurrency does not guarantee FIFO preservation.

Credential references are source-confirmed. Secret existence, validity, project/account relationships, free-tier status, and runtime behavior remain unverified. The provider registry's cost/persistence labels are candidate metadata, not live qualification evidence.

## 3. Routing contract

1. Accept a bounded task with immutable task ID, allowed provider/model set, data-egress class, deadline, max attempts, output budget and idempotency key.
2. Validate authorization and task schema before selecting a credential.
3. Resolve a provider candidate only from the reviewed allowlist and canonical provider registry.
4. Inject only the selected credential through an explicit, statically reviewed workflow mapping. Never accept a secret name or secret value from issue text, task payload, model output or branch content.
5. Track quota at the actual upstream scope: provider, account/project/organization, model, metric and reset window. Credential aliases sharing a scope share the same quota state.
6. On HTTP 429, honor documented Retry-After and reset headers, persist cooldown, and defer or choose another independently eligible route.
7. Classify errors: authentication/authorization failures quarantine the credential or provider pending review; billing and policy failures stop that route; unsupported model/endpoint errors trigger configuration review; transient transport/5xx errors use bounded backoff; quota errors use reset-aware cooldown.
8. Cross-provider fallback requires explicit task data-egress permission and accepted retention/security terms for the destination. Paid routes remain disabled unless separately approved.
9. When quota state is missing, stale, corrupt or conflicting, fail closed and defer. Never rotate keys/accounts to evade a provider limit.
10. Use task idempotency and duplicate branch/PR detection before retrying engineering work. Redact secrets, auth headers, credential-bearing URLs and raw sensitive payloads from logs, comments and artifacts.

## 4. GitHub-native durable state

- **Task inventory:** approved GitHub Issues with a dedicated label and versioned task envelope.
- **Executor:** GitHub-hosted Actions only; no self-hosted labels on the cloud lane.
- **Coordinator:** one stable concurrency group for quota-sensitive work; bounded batch processing.
- **Recovery:** scheduled/manual reconciliation rescans every eligible issue and recovers stale leases. Do not treat one pending Actions run as a durable queue.
- **Quota ledger:** versioned JSON on a dedicated state branch; store provider scope aliases, counters, cooldown/reset timestamps, task IDs and sanitized outcomes only.
- **Concurrency safety:** optimistic updates using current ref/blob SHA with bounded conflict retry. A conflict or failed read/write defers the affected scope. Start with serialized quota-sensitive calls; add parallelism only after independent concurrency qualification.
- **Evidence:** redacted Actions artifacts plus issue/PR references. Artifacts are evidence, not authoritative task state.
- **Secrets:** GitHub Actions Secrets remain the cloud credential store. Each provider is explicitly mapped; no secret value is written to state branches or artifacts.

This is a proposed GitHub-native design. It has no always-on router process; scheduled reconciliation is best-effort and recovery latency follows the configured schedule and GitHub Actions availability.

## 5. Authorization and governance boundary

The source-reviewed ops/qualification/authorized-schemes.yaml remains FAIL_CLOSED, with authorized_pass empty and a blocked three-node local topology. It governs the ASTRA Gold qualification path; it does not constitute authorization to activate a cloud model router. Keep the existing scheme unchanged.

The Gemini agent-fabric registry and claim/lease primitives describe coordination state, while direct runtime loading and enforcement remain open per Wave 59. This report adds a routing design only and grants no execution authority.

## 6. Admission and activation gates

- A0 ingress/task lifecycle accepted.
- MH-12 tool/role enforcement accepted.
- R-06 audit, privacy and data-egress disposition accepted.
- Exact target manifest confirms GitHub-hosted runner execution for every cloud job.
- Provider identity, model ID, free-tier eligibility, quota scope, reset semantics, data retention and GitHub-runner egress eligibility evidenced.
- Secret reference aliases reconciled, including SILICON_KEY_2 versus SILICONFLOW_API_KEY_2.
- Typed task/state schemas and negative fixtures independently reviewed.
- Atomic state conflict handling, stale-lease recovery, idempotency and duplicate-PR prevention independently verified.
- Explicit separate authorization for implementation, workflow dispatch, provider calls, tests, qualification and activation.

## 7. Work completed and boundary

- Read-only source inspection of the three Gemini workflows, authorization scheme, provider registry, and Wave 59 report.
- Confirmed explicit per-workflow key mapping and absence of source-level shared key rotation in the inspected workflow definitions.
- Recorded GitHub runner egress and location-independence boundary.
- No provider calls, workflow dispatches, tests, qualification, credential reads, infrastructure changes, deployments, merges or branch integration occurred.

## 8. Next bounded step

Prepare a manual-dispatch-only coordinator implementation proposal with one task ID per run, an explicit provider allowlist, statically mapped secrets, redacted quota ledger and fail-closed state conflict handling. Keep scheduled reconciliation and provider execution disabled until A0, MH-12, R-06 and the target manifest are accepted.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
