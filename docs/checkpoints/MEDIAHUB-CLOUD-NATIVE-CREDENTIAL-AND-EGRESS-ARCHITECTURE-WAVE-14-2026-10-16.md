# MediaHub OS — Cloud-Native Credential and Network-Egress Architecture, Wave 14

- Date: 2026-10-16
- ID: MH-CAF-EGRESS-14
- Status: **REFERENCE DESIGN / PROPOSED / IMPLEMENTATION AND RUNTIME QUALIFICATION OPEN**
- Contour: A — autonomous development fabric
- Parent: [Wave 08 Cloud-Agent Fabric Reference Architecture](MEDIAHUB-AUTONOMOUS-CLOUD-AGENT-FABRIC-REFERENCE-ARCHITECTURE-WAVE-08-2026-10-16.md)
- Related: [Wave 11 task contract and activation queue](MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json), [Wave 13 registry/evidence schemas](MEDIAHUB-CLOUD-AGENT-REGISTRY-AND-EVIDENCE-SCHEMAS-WAVE-13-2026-10-16.md), [Wave 12 Gemini hardening proposal](MEDIAHUB-GEMINI-WORKFLOW-HARDENING-PATCH-PROPOSAL-WAVE-12-2026-10-16.md)
- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Decision summary

Adopt a GitHub-centered, cloud-hosted, ephemeral-worker design as the default target for Contour A. The user’s device and any user-owned always-on server are outside the provider credential path. Jobs run on GitHub-hosted runners or a separately accepted cloud-agent service; they make outbound HTTPS calls directly from that execution environment to the authorized provider endpoint.

This means:
- no user-owned server is required as a permanent API gateway;
- provider keys are scoped to the provider account/project and are injected only into the authorized job at runtime;
- provider requests originate from the hosted execution environment, not from the ChatGPT conversation or the user’s phone;
- GitHub-hosted runner egress IPs are dynamically assigned/shared by default, so a stable source IP must not be assumed;
- provider account eligibility, terms, billing/quota, data policy and regional availability remain independent of the network route;
- no proxy, VPN, region spoofing, or other location-control mechanism is part of this architecture.

An API key is generally a provider credential, rather than a credential bound to a single physical server. A provider may separately offer IP allowlists, project restrictions, organization policies or regional restrictions. Such controls must be honored exactly as configured.

## 2. Target architecture

```text
Owner / approved GitHub event
        |
        v
GitHub workflow admission
  - fixed workflow revision
  - validated task envelope
  - task-scoped authorization
  - path/data/budget/deadline bounds
        |
        v
Ephemeral hosted worker
  - clean workspace
  - minimum GITHUB_TOKEN permissions
  - persist-credentials: false
  - no long-lived provider key in source or artifacts
        |
        +---- outbound HTTPS ----> authorized provider endpoint
        |                           - exact provider/model allowlist
        |                           - quota bucket and budget
        |                           - data policy and eligibility evidence
        |
        v
Quarantined output + evidence manifest
        |
        v
Independent reviewer / accepted A0 lifecycle
        |
        v
Draft PR or reviewed patch branch
        |
        v
Required checks + authorized promotion
```

This is the reference flow, not evidence of a deployed system. A0 remains the intended authority for mission admission and lifecycle once its ingress/issuer contract is accepted. The documentary queue remains non-operational until that lifecycle exists and is qualified.

## 3. Credential model

### 3.1 Provider API keys

- Store a provider key in a narrowly scoped GitHub Actions secret or environment secret, only after the account owner explicitly adds it.
- Keep secrets out of repository files, task envelopes, model prompts, artifacts, cache entries, step summaries and logs.
- Inject a secret only into the single step that needs it; avoid job-wide environment exposure.
- Restrict workflow execution to trusted refs and approved dispatchers; use environment reviewers where supported.
- Set minimal `GITHUB_TOKEN` permissions and `persist-credentials: false` for checkout.
- Rotate/revoke keys through the provider’s account controls if exposure is suspected.
- Never use a schema field or registry status as proof that a credential exists or that the agent is authorized.
- Treat an absent secret as an explicit blocked status; avoid fallback to another provider unless the task envelope independently authorizes that exact destination.

### 3.2 Short-lived credentials

Prefer OIDC federation and short-lived tokens for cloud resources that support GitHub Actions OIDC. OIDC does not automatically replace a Gemini API key or another provider key unless that provider explicitly supports the relevant federation method. Do not invent a keyless flow for a provider whose documented API requires a key.

### 3.3 Authorization layers

Keep these independent:
1. GitHub identity and workflow dispatch permission.
2. Task-envelope admission authority.
3. Provider account/project credential and provider-side access policy.
4. Provider/model/data-route authorization for this specific task.
5. Repository write and pull-request permissions.
6. Independent verification and promotion authority.

Success at one layer does not grant permission at another.

## 4. Network-egress model

### Default: direct hosted-runner egress

- Use GitHub-hosted ephemeral runners for read-only audit and bounded engineering tasks.
- Allow only required outbound HTTPS destinations where the runner environment supports enforceable egress controls.
- Record runner class, workflow SHA, run/job IDs and available runner metadata in the evidence manifest.
- Assume egress IP can vary between runs. Do not build provider authorization around a fixed user IP.
- Do not route provider traffic through the user’s device or a persistent home server.

### Fixed-IP exception

If an upstream provider or enterprise policy requires source-IP allowlisting, the design must explicitly choose an accepted option: a supported hosted runner class with static egress, an approved managed egress gateway, or a provider-side credential restriction that avoids IP allowlisting. Each option needs a separate cost/security/privacy decision. It is outside the default zero-server profile and remains blocked pending authorization.

### Regional controls

Network egress location is not a substitute for provider account eligibility or contractual regional rules. The system must use the provider only where the account, workload and service are eligible under the applicable terms. If a provider returns an eligibility or region denial, record the sanitized denial and stop that route; do not rotate egress location to evade it.

## 5. Provider adapter contract

Each provider route in the task envelope must bind:
- provider ID and exact model ID;
- credential reference name only, never the secret value;
- task purpose and data classification;
- eligibility/policy evidence reference and revision;
- quota bucket, attempt budget, request deadline and output bound;
- data retention/training/logging constraints;
- fallback mode: `disabled` or `preauthorized_only`;
- sanitized error classes and retryability;
- output and request digests where supported;
- independent reviewer disposition.

Retry transient rate limits and selected server errors with bounded exponential backoff and jitter. Authentication, authorization, policy and region denials are terminal for that route. A quota event may trigger another route only when that exact alternate provider/model is already authorized for the same task and data class. Paid fallback remains disabled unless a task-specific budget and authorization explicitly permit it.

## 6. Agent admission and immediate onboarding

When an agent becomes available or the owner authorizes a provider:
1. record its identity, exact workflow/ref SHA and task capability;
2. confirm the provider route and model allowlist;
3. bind the allowed data classes, paths, effects and resource bounds;
4. reference a valid issuer/grant and independent review;
5. define expiry, revocation and evidence requirements;
6. begin with read-only source audit or documentation tasks;
7. review one complete evidence manifest and output artifact;
8. expand to isolated patch proposals only after review;
9. permit draft PR creation only after repository governance and A0 admission are accepted;
10. keep merge, release, deployment and Contour B access separately gated.

This is a design-time onboarding procedure. It does not register or authorize an agent by itself.

## 7. Free-tier and quota behavior

- Maintain per-provider/model quota buckets and bounded concurrency.
- Classify quota exhaustion, temporary service errors, authentication errors, policy denials and malformed output separately.
- Use free-tier routes only where their data policy is approved for the task’s data class.
- If all preauthorized routes are unavailable, place the task in a durable waiting state once the queue is implemented; preserve its immutable task envelope and reason.
- Never silently switch to a paid route or expand data sharing.
- Keep the current successful Gemini read-only workflow as the existing integration; preserve it while addressing source-hardening findings.

## 8. Current implementation status

| Component | Current evidence | State |
|---|---|---|
| Gemini read-only integration | Historical GitHub Actions run 38952885501 completed successfully; job 117148417231 reports successful Gemini API step; artifact 12069128185 uploaded | HISTORICAL EXECUTION VERIFIED |
| Gemini workflow hardening | Wave 12 exact-source patch proposal; source unchanged | REVIEW REQUIRED |
| Task envelope | Wave 11 proposed JSON Schema | REVIEW REQUIRED / A0 CONTRACT OPEN |
| Agent registry | Wave 13 proposed schema | REVIEW REQUIRED / NO LIVE REGISTRY |
| Evidence manifest | Wave 13 proposed schema | REVIEW REQUIRED / NO GENERAL WORKER PROVENANCE PIPELINE |
| Activation queue | Wave 11 JSON file | DOCUMENTARY ONLY / NO LIVE SCHEDULER |
| A0 issuer and lifecycle | WB-14AA/AB/AC proposals and crosswalks | ACCEPTED CONTRACT OPEN |
| R-06 audit/privacy | Governance disposition template | OPEN |
| Target runner/workspace/network manifest | Source discovery still open | UNKNOWN |
| Agent auto-onboarding | Procedure specified here | NOT IMPLEMENTED |
| Fixed egress IP | Unneeded for default direct API-key pattern unless provider policy requires it | NO DEFAULT FIXED-IP DEPENDENCY |

## 9. Public-source basis

- GitHub Actions secure-use guidance: least-privilege tokens, secret handling, hosted-runner isolation and OIDC options: https://docs.github.com/en/actions/reference/security/secure-use
- GitHub-hosted runner reference: hosted runner egress IP ranges are dynamic/shared by default and are documented through the GitHub API: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub OIDC: short-lived cloud credentials where the target provider supports federation: https://docs.github.com/en/actions/concepts/security/openid-connect
- Gemini API Additional Terms: service eligibility, regional availability and different data treatment for unpaid versus paid services: https://ai.google.dev/gemini-api/terms
- OpenRouter provider logging: provider-specific data retention and training policies must be considered per route: https://openrouter.ai/docs/guides/privacy/provider-logging
- OpenRouter provider selection: request-level routing/data-policy controls vary by plan and endpoint: https://openrouter.ai/docs/guides/routing/provider-selection

## 10. Acceptance criteria

- No user-owned always-on server is required for the default route.
- No fixed egress IP is assumed for hosted runners.
- Secrets are scoped to the smallest possible runtime step and absent from logs/artifacts.
- Provider, model, task purpose, data class, budget and fallback destinations are explicitly authorized.
- Unknown provider eligibility, missing credentials, policy denials and unapproved fallback fail closed.
- Task input and source are bound to immutable revisions and file digests.
- Outputs remain quarantined until independent review.
- The workflow creates no direct product-state mutation and has no automatic merge/deploy authority.
- Cancellation, timeout, quota exhaustion, retries and ambiguous outcomes are represented in evidence.
- Independent source review, full schema validation, targeted workflow tests and authorized execution evidence are retained before qualification.

## 11. Disposition

Wave 14 establishes the reference design for serverless-from-the-owner-perspective provider access: hosted workers call providers directly, while API credentials remain provider-scoped and are injected at runtime. This avoids dependency on the user’s phone or a user-owned permanent server. It does not promise zero network egress, a fixed source IP, region independence, or live autonomous scheduling.

No secrets were accessed, no provider call or workflow dispatch was made, no workflow source was edited, and no test or deployment was executed in this documentary pass. Implementation must follow the accepted A0 lifecycle, R-06 policy, target manifest and separate execution authorization.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
