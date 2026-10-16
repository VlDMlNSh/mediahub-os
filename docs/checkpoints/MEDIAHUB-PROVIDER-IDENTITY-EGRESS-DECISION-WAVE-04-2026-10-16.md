# MediaHub OS — Provider Identity, Age Eligibility and Egress Decision Packet, Wave 04
Date: 2026-10-16
Repository: https://github.com/VlDMlNSh/mediahub-os
Documentation ref: `docs/mediahub-chat-tree-map-20261012`
Status: DOCUMENTARY DECISION PACKET / PROPOSED / RUNTIME-UNVERIFIED

## 1. Decision

The free-cloud-agent route remains gated by provider eligibility, task-level authorization, data classification and explicit destination selection. A free quota alone is insufficient for admission. No provider may receive repository context until its account eligibility, current terms, data-use policy, destination, retention, and task class are approved and recorded.

This packet resolves a material gap in Wave 03: automatic quota fallback is allowed only when the task authorization already names the exact alternate provider/model destinations and permits the data class to reach each one. A generic instruction to “use any free provider” is insufficient. Each attempted destination is recorded as a separate provider decision.

## 2. Primary-source constraints

### 2.1 Canonical architecture and functional authority

- Unified architecture/deployment contract: `docs/checkpoints/mediahub-unified-architecture-and-deployment-contract-v0.1.md`, blob `71ae0e68cc6ad494f85f33f64cde09ef5c4273d7`. It requires local-by-default handling for personal/sensitive data; external calls are opt-in per task; every fallback is a new provider/destination decision; and the invocation record includes task ID, provider/model identity, policy decision, data class, destination, budget, provenance and validation outcome.
- Functional Baseline 2.0: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. It is the accepted functional authority and governs the privacy boundary.
- Unified System Traceability Matrix v0.1: blob `6127e600544a9c007685cd06e6aeb276026bf262`. Its cross-domain controls require default-deny external egress, classification, purpose, minimization/redaction, authorization, bounded transfer, audit, retention, and explicit fallback decisions.

These constraints take precedence over the proposed router behavior. This packet records a compatible design refinement; it does not amend or accept the architecture contract.

### 2.2 Provider terms and data use

| Provider path | Official source evidence | Design consequence | Current admission |
|---|---|---|---|
| Gemini API unpaid quota | https://ai.google.dev/gemini-api/terms — Additional Terms effective 2026-03-23. Google states that unpaid-service inputs and outputs may be used to improve/develop products and machine-learning technologies; human reviewers may process inputs/outputs. The same terms state API users must be 18 or older and access is limited to available regions. | Do not send confidential, sensitive, personal or private repository content through unpaid Gemini. Verify account-holder age eligibility and available-region status through the official terms. Never bypass age or regional restrictions. | BLOCKED until an eligible adult account owner and project governance provide documented evidence; account state remains UNKNOWN |
| GroqCloud inference | https://console.groq.com/docs/your-data and https://console.groq.com/docs/legal/services-agreement. Official docs describe default non-retention for ordinary inference, with limited reliability/abuse-monitoring retention unless Zero Data Retention is enabled and available. | Verify current account controls, service terms, model policy and allowed region. Treat stated defaults as provider policy evidence, not proof of account configuration. | CANDIDATE / account and eligibility evidence UNKNOWN |
| OpenRouter | https://openrouter.ai/privacy/ and https://openrouter.ai/docs/guides/privacy/provider-logging.mdx. OpenRouter transmits prompts to the selected/routed model provider; providers have different retention/training practices. Routing can be constrained by data-collection policy; endpoint-level policy must be checked. | Pin both the OpenRouter route and permitted underlying provider policy. For sensitive data, require an enforceable data policy such as ZDR where supported; otherwise deny egress. A free model label alone does not qualify a destination. | CANDIDATE / route-level data policy and account eligibility UNKNOWN |
| GitHub Models / Cerebras | No account-specific terms, entitlement, model access, or runtime evidence established in this pass. | Keep disabled until official current terms, minimum-age/eligibility, data handling, region, quota and model identity are evidenced. | DEFERRED / UNKNOWN |

Age and regional eligibility are hard admission controls. The router must stop with `POLICY_DENIED` when the provider terms or account eligibility are unmet or unknown. Account ownership, age or location must never be falsified or bypassed to obtain API access.

## 3. Task authorization contract

Each task that may invoke a hosted provider must carry a versioned authorization envelope:

- `task_id`, requester/approver identity and policy revision;
- immutable source commit SHA and explicit file-path allowlist;
- data classification and permitted transformations/redactions;
- exact allowed provider IDs, model IDs and, where applicable, underlying routed provider IDs;
- explicit allowed destinations and regions;
- provider-specific terms/data-use review reference and expiry;
- maximum request count, input/output token budget, deadline and concurrency;
- hard cost ceiling `USD 0` and explicit prohibition of paid fallback;
- whether fallback is allowed and the exact ordered alternatives;
- output-handling, artifact-retention and independent-review requirements.

Missing, expired or contradictory fields produce a closed outcome. A quota event alone does not authorize a new destination.

## 4. Corrected failover algorithm

1. Validate task authorization, requester/approver authority, provider eligibility, region, data class, destination, budget and source SHA before reading files into model context.
2. Select the first provider/model explicitly listed in the task envelope and eligible under the current policy.
3. On HTTP 429, honor `Retry-After` and cool down the correct quota bucket. Consider an alternate only if that exact alternate was authorized for this task and data class before the first call.
4. On transient 5xx/network failure, retry within the task's bounded attempt budget. Then consider only an already-authorized alternate.
5. On 401/403, age/region failure, data-policy mismatch, model-policy rejection or any authorization denial, stop the route and emit a sanitized blocked record. Never rotate credentials to circumvent a refusal or account restriction.
6. When no authorized provider remains, persist the task as `PAUSED_PROVIDER_POLICY_OR_QUOTA`; resume only after policy-valid quota or authorization changes.
7. Bind the output to the task ID, source SHA, provider/model, route, policy revision, request status, output digest and reviewer outcome. Treat model output as untrusted advisory material.

## 5. Data-class admission matrix

| Data class | Hosted free-tier default | Required evidence for any exception |
|---|---|---|
| Public, already-published project documentation | BLOCKED until task and destination are explicitly approved | Exact paths, immutable SHA, provider/model/route, terms and eligibility review, minimization, budget, output retention |
| Private source code, unpublished architecture, security findings | DENY by default | Explicit owner/governance authorization plus provider terms that permit the transfer, route-level data-use controls, minimization, audit and retention approval |
| Secrets, credentials, tokens, private user data, raw personal data | DENY; redact or keep local | A hosted free-tier route is not admitted for these inputs by this packet |
| Runtime logs, incident evidence, security alerts | DENY by default | Classification, redaction, purpose limitation, destination and retention approval; exclude secret-bearing lines |

A repository being publicly accessible does not make all attached context public. Workflow inputs, issue content, logs, artifacts, private branch names and connected account metadata may contain confidential material.

## 6. No-server and network-boundary decision

GitHub-hosted runners can provide an ephemeral cloud execution environment without a developer-owned always-on server. That fact does not establish a guaranteed physical egress IP, fixed country, provider-accepted region, or a stable registration location. The runner's network route and provider processing region are separate properties and must be evidenced by official service documentation or approved account controls.

For this architecture:
- use GitHub-hosted runners for the initial cloud job only after authorization;
- do not add self-hosted runner labels or legacy node names to the new cloud path;
- do not depend on a personal device's location or use location/identity changes to bypass provider restrictions;
- record the GitHub execution environment and provider processing-region evidence separately;
- if an approved region or data route cannot be established, fail closed.

## 7. Rollout gate updates

| Gate | Evidence required | State |
|---|---|---|
| EGRESS-01 — provider eligibility | Current official terms, minimum-age/account eligibility, available region, owner-controlled account proof | BLOCKED / UNKNOWN |
| EGRESS-02 — data policy | Retention/training controls and underlying route policy for each provider/model | PARTIAL; current terms found, account settings UNKNOWN |
| EGRESS-03 — per-task authorization | Versioned task envelope with exact destination allowlist and explicit alternate list | DESIGNED; implementation absent |
| EGRESS-04 — quota failover | 429/Retry-After, shared quota bucket, provider refusal, all-routes-exhausted behavior | DESIGNED; tests/runtime evidence absent |
| EGRESS-05 — first-provider proof | Authorized bounded run, source SHA, run ID, HTTP status, artifact digest and redaction review | NOT RUN |
| EGRESS-06 — independent review | Reviewer confirms destination authorization, zero paid usage, no sensitive data egress and provenance integrity | OPEN |

## 8. Actions completed and limits

- Read current bootstrap, map, master roadmap, continuation checkpoint, Wave 03 router design, unified architecture/deployment contract, Baseline 2.0, existing traceability matrix and canonical source registry.
- Reviewed current official provider terms and data-policy documentation through the linked primary pages.
- Resolved the design conflict: quota failover requires prior task-level authorization for each exact alternate destination; no generic silent fallback.
- No credentials or provider account settings were accessed. No provider/model calls, workflow dispatches, tests, scanners, installations, host/runtime inspection, infrastructure changes, deployment or branch integration occurred.
- This packet is documentary evidence and proposed policy; it is not an implementation, provider approval, qualification or acceptance.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
