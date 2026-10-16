# MediaHub OS — Cloud-Agent Fabric Traceability Matrix Addendum, Wave 35

- Date: 2026-10-17
- Parent matrix: [Unified System Traceability Matrix v0.1](mediahub-unified-system-traceability-matrix-v0.1.md)
- Architecture: [Cloud-Agent Autonomous Queue Reference Architecture, Wave 35](MEDIAHUB-CLOUD-AGENT-AUTONOMOUS-QUEUE-REFERENCE-ARCHITECTURE-WAVE-35-2026-10-17.md)
- Master-roadmap addendum: [Wave 35 roadmap execution](MEDIAHUB-MASTER-ROADMAP-EXECUTION-ADDENDUM-WAVE-35-2026-10-17.md)
- Status: **PROPOSED TRACEABILITY ADDENDUM / NOT ACCEPTED / NOT FROZEN / RUNTIME UNVERIFIED**

## 1. Requirement-to-evidence crosswalk

| Requirement ID | Requirement / invariant | Responsible authority | Reused artifact / evidence | Current state | Acceptance evidence required |
|---|---|---|---|---|---|
| CAF-35-01 | Cloud-agent admission must be explicit, revocable, and bound to a repository/account/service identity | Owner-governed admission; A0 consumes the accepted decision | Wave 11 enrollment direction; Wave 35 agent admission record | PROPOSED | Accepted non-secret registry schema and account/repository permission evidence |
| CAF-35-02 | Credential material remains outside source, task payloads, model context and logs | MH-12 secret lifecycle plus A0 job boundary | Wave 30 secret-flow/egress review, blob `28a5152b60b0809a90a0c938b81439b8a19852b7` | OPEN / HIGH PRIORITY | Provider-scoped secret reference; redaction tests; evidence that unrelated secrets are absent from each job |
| CAF-35-03 | Each provider request must pass purpose/data-class/destination/eligibility policy | R-06 + MH-21 provider/egress contract | Wave 30 crosswalk; Wave 04 provider identity/egress decision | PROPOSED / OPEN | Exact route policy, permitted destination/region, privacy/terms evidence, route-denial evidence |
| CAF-35-04 | API credentials must be decoupled from a fixed owner-operated server | Developer Fabric architecture | Wave 11 enrollment and topology direction | OWNER DIRECTION RECORDED / DESIGN PROPOSED | One task-scoped hosted-runner/provider route; secret stays provider/account/project scoped |
| CAF-35-05 | System must represent actual runner egress and provider-permitted region | MH-21 egress controls | GitHub-hosted runner network/IP documentation; Wave 35 architecture | OPEN | Exact execution service, its egress class and accepted provider region policy |
| CAF-35-06 | One authoritative queue owns task lifecycle and admission decisions | A0 / ASTRA within accepted boundary | Existing 23-lane manifest, blob `b948f0beb510f24399d82aaefcb7f95584e99cab` | OPEN / MANY FIELDS UNKNOWN | Accepted queue authority, dependency order, issuer lifecycle, durable task schema |
| CAF-35-07 | Concurrent cloud workers require atomic distributed claim, lease fencing and recovery | A0 queue owner; persistence source subject to accepted target manifest | Existing `agent_fabric.py`, blob `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | BLOCKED FOR MULTI-WRITER CLOUD USE | Cross-runner atomic claim design, monotonic generation/fencing, lease recovery and fault-injection evidence |
| CAF-35-08 | Worker input is immutable and path-scoped | A0 task authorization + independent validator | Existing claim primitive supports path overlap checks; source SHA fields remain UNKNOWN in many lanes | PARTIAL PRIMITIVE / INCOMPLETE GLOBAL EVIDENCE | Source-SHA pin, path allowlist, symlink/traversal rejection and independent diff-manifest verification |
| CAF-35-09 | Read-only admission precedes patch-worker capability | Agent admission and least-privilege policy | Existing Agent Fabric verification workflow and GitHub Actions permissions model | PROPOSED | Read-only run evidence; write capability is absent until a separate admission revision |
| CAF-35-10 | Provider quota failover is pre-authorized destination-by-destination | R-06 route policy | Wave 04 provider identity/egress decision | PROPOSED | Task envelope lists exact routes/models/data classes and USD ceiling before first invocation |
| CAF-35-11 | Agent output cannot self-promote into verification, qualification, release or production | Independent verifier and existing governance gates | `CURRENT-TRUTH.generated.md`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` | BLOCKED / NOT PROVEN | Exact-SHA independent review; fresh G0–G11 evidence; separate owner acceptance |
| CAF-35-12 | Agent onboarding must wait for explicit route/probe authorization | Owner approval + A0 | Wave 11; Wave 35 enrollment flow | PROPOSED | An audit trail proves task-specific approval before a provider invocation |
| CAF-35-13 | Model and tool outputs are untrusted data and cannot grant capability or product-state mutation | MH-04/MH-07/MH-10/MH-21 plus Product State Authority | Unified matrix invariants | EXISTING INVARIANT TO PRESERVE | Negative tests and independent review on the exact target revision |
| CAF-35-14 | Existing workflow/components must be reviewed before new framework or scheduler adoption | Canonical component manifest and project reuse-first rule | Agent Fabric, 23-lane manifest, existing workflow/test sources | REQUIRED | Gap-to-component statement; no duplicate scheduler unless accepted evidence proves a gap |
| CAF-35-15 | Queue remains auditable and recoverable across auth revocation, quota exhaustion, cancellation and worker crash | A0 queue state authority | Existing manifest currently has UNKNOWN global dependency order and broad UNKNOWN claims | OPEN | Versioned transition table, idempotency proof, cancel/expiry/recovery evidence and sanitized audit artifacts |

## 2. External evidence pointers

- GitHub Actions OIDC: https://docs.github.com/en/actions/concepts/security/openid-connect
- Workflow-dispatch permissions: https://docs.github.com/en/rest/actions/workflows#create-a-workflow-dispatch-event
- Hosted-runner IP/network behaviour: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub Agentic Workflows security model: https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-github-agentic-workflows
- Jules GitHub/VM task lifecycle reference: https://jules.google/docs/

External product documentation proves only the described platform capability at its stated revision. It does not grant MediaHub authorization, qualify the account, or establish runtime behavior.

## 3. Verification boundary

Source reads were performed against GitHub refs and identified blob SHAs. No tests, workflow dispatch, provider invocation or credential access occurred in this pass. The current source truth remains G0–G11 BLOCKED; these rows are traceability proposals rather than acceptance evidence.
