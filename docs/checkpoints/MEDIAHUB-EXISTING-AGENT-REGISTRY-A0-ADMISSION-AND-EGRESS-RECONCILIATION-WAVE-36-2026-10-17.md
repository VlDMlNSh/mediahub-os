# MediaHub OS — Existing Agent Registry, A0 Admission and Provider-Egress Reconciliation, Wave 36

- Date: 2026-10-17
- ID: MH-CLOUD-AGENT-ADMISSION-RECONCILIATION-W36
- Contour: A — Developer Fabric
- Status: **SOURCE-BOUND RECONCILIATION / PROPOSED DECISIONS / IMPLEMENTATION GATES OPEN**
- Documentation ref: docs/mediahub-chat-tree-map-20261012
- Main source HEAD reviewed: 99e7c0598bdc2f69201958aeb983f64c04504990
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Executive result

MediaHub already contains separate source artifacts for (1) the agent/provider catalog, (2) engineering role profiles, (3) provider selection, (4) provider adapter configuration, and (5) the 23-lane A0/ASTRA execution queue. The correct direction is to reconcile those existing components under one admission contract, rather than add another agent registry, queue, provider router or scheduler.

The existing code and catalogs establish useful structure, but they do not prove end-to-end agent authorization or multi-runner queue safety. This pass recommends a compatibility-preserving admission extension, with schema validation and runtime activation held behind the accepted A0, MH-12, R-06 and target-manifest contracts.

### Recommended component ownership

- `profiles/agent-registry.json`: catalog of known agent/provider/tool identities and candidate capability profiles.
- `.github/agent-system/registry.yaml`: A0/A1/A2/A3 role-fabric definitions and task-scoped worker policy.
- `schemas/ai/ai-provider-registry.schema.json`: narrow runtime provider-selection list, not a global agent admission registry.
- `schemas/ai/ai-provider-adapter.schema.json`: provider adapter identity, operations, availability, endpoint and configuration reference.
- `ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json`: current 23-domain lane status and required evidence. A0 owns engineering queue lifecycle, subject to its accepted contract.
- `runtime/mediahub_runtime/agent_fabric.py`: current local-filesystem claim/lease primitive, whose multi-runner guarantees remain unproven.
- `architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` and `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml`: canonical lifecycle, role boundaries, thresholds and G0–G11 promotion gates.

No artifact above is individually sufficient to authorize a provider call. In particular, `enabled: true`, `activation: credentialed_only`, the presence of a credential reference, a successful historical run, or provider model discovery must not be treated as `ADMITTED`, `QUALIFIED` or `LAUNCHED`.

## 2. Live source crosswalk

| Source | Ref | Blob SHA | Source-bound observation |
|---|---|---|---|
| Agent catalog | `main:profiles/agent-registry.json` | `993cbbe1b2b2a88da7d8884a897b404f055981a8` | Declares `mediahub.ai.agent-registry` v1.2.0. Entries include identity, capabilities, `enabled`, tier and activation modes. Some entries set credential environment-variable names; values are not part of the catalog. Qualification and admission semantics are heterogeneous. |
| Role-fabric registry | `main:.github/agent-system/registry.yaml` | `0317d1e794aa80cd0fa22bd953b95921b26aafd3` | Defines one ASTRA coordinator, architect/builder/verifier roles, task-scoped worker runtime, no nested delegation, default concurrency 3, overlap blocking and independent verification. |
| Provider selection schema | `main:schemas/ai/ai-provider-registry.schema.json` | `9537a64bc948b1bea3e2a640670f48e107760a50` | v1.0.0 allows provider_id/enabled/priority and global selection policy, including FAILOVER. It lacks task-bound data class, destination authorization, account eligibility, spend ceiling and route-specific fallback authorization. |
| Provider adapter schema | `main:schemas/ai/ai-provider-adapter.schema.json` | `e0dab7002222451579e649a7d1d29985393d9a42` | v1.0.0 defines provider adapter, provider type, adapter type, operations, capabilities, availability/state, endpoint and configuration reference. It is a technical adapter descriptor, not an admission decision. |
| 23-lane queue manifest | `main:ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json` | `b948f0beb510f24399d82aaefcb7f95584e99cab` | Includes 23 lanes with disposition, owner, base/head SHA, lease, worker, PR and notes. Most current authority fields are UNKNOWN; global dependency order is UNKNOWN. |
| Claim/lease primitive | `main:runtime/mediahub_runtime/agent_fabric.py` | `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | Uses local file records and `fcntl` flock, path-overlap checks, heartbeat, expiry and release. It cannot alone establish atomic distributed claims across independent ephemeral runner filesystems. |
| ASTRA role/authority contract | `main:architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml` | `adc852009c3a79d0e64265a3af8a4910a1388057` | A0 single coordination authority; A1 architecture/contracts; A2 bounded implementation; A3 independent verification; executor/transport/provider/model layers have no authority. Cloud fabric authority is none. |
| ASTRA qualification and launch gates | `main:architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` | `aef6229477ed8ec45e45170f98ea87f7ba75ca29` | Lifecycle includes DISCOVER/PREFLIGHT/ADMIT/QUALIFY/EXECUTE/VERIFY/INTEGRATE/RECONCILE/PRE_SOAK/SOAK_24H/LAUNCH_READY/LAUNCHED/BLOCKED/ROLLBACK. G0–G11 require fresh source-bound evidence; G11 is human-authorized. |
| ASTRA governance contract | `main:architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` | `1d3ac25e7817f365807ad85d0d7c9007bd48bebf` | Credential creation authority HUMAN; per-provider isolation and auditing required; credential max age 90 days; default parallel claims 3; heartbeat TTL 120s; lease TTL 600s; executor timeout 900s; evidence freshness 24h. |
| MH-12 Secrets | `main:docs/architecture/MH-12-secrets.md` | `4e4faf00e3d24c1de5a394e78670c68786ac9a1e` | Generate → Store → Use → Rotate → Revoke → Destroy; secret material stays out of source, logs, telemetry, prompts and evidence; exact store remains non-canonical pending evidence and ADR. |
| MH-21 data egress | `main:docs/architecture/MH-21-data-egress.md` | `242b3090d41f52866889b8c8cf587ff4c95eadb3` | Classification → Purpose → Destination → Privacy Policy → Security Policy → Authorization → Redaction/Minimization → Bounded Transfer; arbitrary egress denied by default. |
| MH-21 provider trust | `main:docs/architecture/MH-21-provider-trust.md` | `ad7226a2e7eeeaf412f94e08440db72ac4fe13cf` | Provider lifecycle is discovered/evaluated/qualification-pending/approved/active/degraded/blocked/quarantined/revoked; approval is revocable and time-bounded. |
| P0-07 trusted-context proposal | docs branch | `c0ae0d3fe340c3e50382b7d4aa8da7b6b5f56d9f` | Proposed / governance review required. Issuer, lifecycle, format and API are intentionally left open; preserve P0-04 mutation authority, P0-05 consumer boundary and P0-07 decision boundary. |
| P0-07 R-06 route reconciliation | docs branch | `452d3531c9897679d52cedc7b5311234f98b8fa8` | Accountable reviewer/authority and formal R-06 acceptance path remain unestablished in the reviewed records. |
| R-06 governance template | docs branch | `834fd1ab70eee88355844ba2ebba6c2b6c47ecdb` | Template remains unfilled and carries no acceptance. Audit schema, privacy, retention, outage and reconciliation semantics stay open. |
| Current ASTRA qualification truth | `main:docs/qualification/CURRENT-TRUTH.generated.md` | `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731` | G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED. |
| Canonical component manifest 2.0 | `main:docs/checkpoints/mediahub-github-component-final-manifest-2.0.md` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Existing component-selection authority. Temporal, NATS, etcd and similar durable-coordination candidates are future-gated until an evidenced gap and admission. |

## 3. Contract boundaries to preserve

1. **Agent catalog vs role registry:** provider/executor identities remain in the existing agent catalog; A1/A2/A3 roles remain in the role-fabric registry. A single identifier can be linked across them, but each document retains its current purpose.
2. **Catalog vs authorization:** catalog membership, `enabled`, provider readiness, a secret reference, or successful API auth are facts about registration/configuration only. They must not promote the agent to task admission.
3. **Provider adapter vs destination policy:** adapter `endpoint` and `configuration_ref` are technical values. Every request must also pass MH-21's task-bound destination gate. An arbitrary endpoint supplied by the agent or model is denied.
4. **Provider selection vs failover authorization:** a provider-registry `FAILOVER` policy cannot independently authorize alternate data destinations. The task envelope must name each allowed provider/model/underlying routed provider, data class, destination, region policy and budget before the initial invocation.
5. **Agent claims vs distributed claim authority:** the local ClaimStore remains useful for a single shared filesystem/process domain. Independent ephemeral runners need an accepted shared atomic claim authority, fencing generation and recovery proof before parallel writes.
6. **A0 engineering state vs product state:** A0 owns the engineering coordination lifecycle inside its accepted boundary. MediaHub Product State Authority remains the sole canonical product-state mutation authority. Provider, model, executor, transport and workflow outputs have no product-state authority.
7. **A0 issuer vs P0-07 authorization-context issuer:** do not assume ASTRA's coordination role creates trusted P0-07 authorization contexts. The issuer/lifecycle proposal is a separate open governance item.
8. **Audit policy vs ordinary logs:** R-06 must govern audited operations, privacy, sink durability, retention, access and reconciliation. Keep R-06 acceptance separate from the task queue's operational event log.
9. **Manifest vs target-specific deployment:** the canonical component manifest records component selection; a target manifest still needs exact host/service/OS, network flows, secret references, health/recovery and acceptance evidence for the selected deployment profile. Do not treat the component list as a deployment target manifest.

## 4. Proposed compatible admission contract

Add admission semantics as a versioned additive contract mapped to the existing catalog and queue. Keep current IDs and v1.2.0 catalog format until an explicit schema migration is accepted.

Required fields for any task-eligible agent:

- `agent_id`, `catalog_revision`, `integration_kind`, `provider_account_ref`, `provider_project_ref`, `repo_id`, `source_ref`, exact `source_sha`.
- `admission_state`: DISCOVERED, REVIEW_PENDING, WAITING_AUTH, AUTH_VERIFIED, READ_ONLY_ADMITTED, PATCH_ADMITTED, QUALIFIED, ACTIVE, DEGRADED, BLOCKED, QUARANTINED, REVOKED, EXPIRED.
- `credential_ref` as an opaque reference only; `credential_version_ref`, expiration/revocation state and auth evidence reference. Never include the credential value.
- Allowed provider/model IDs, underlying router destinations, data classes, endpoint IDs, approved region/egress class, purpose, allowed file paths, capabilities, write scopes, max requests/tokens/budget, timeout, concurrency limit, retry budget and pre-authorized fallback order.
- `policy_revision`, terms/privacy evidence references and expiry, security/privacy review references, verifier profile, artifact schema and latest accepted evidence digest.
- A task-specific authorization record: task ID, approver identity, allowed context files, exact routes, cost ceiling, deadline, cancellation semantics and output/provenance requirements.

All new fields are proposed. The validation contract must map to existing stable IDs and statuses, reject unknown status values, and use a migration strategy that preserves old consumers. A versioned schema and offline validator should be produced only after A0 issuer/ingress, R-06 and the target-manifest source crosswalk is reconciled.

## 5. Server-independent credential and network model

The architecture must remove a fixed dependency on one owner-operated server, while retaining the real network and provider-policy boundary:

- Use the provider's own GitHub App/OAuth integration where one is already supported, or a narrowly scoped provider/account/project credential reference injected into only the authorized job.
- Prefer GitHub OIDC short-lived credentials only for a provider or secret manager that explicitly supports that trust model. OIDC is not a universal drop-in replacement for every model API key.
- For API-key-only providers, use a repository/environment/job-scoped secret store selected by an accepted MH-12 decision; values stay in the service's secret store and are never copied to the agent catalog/task payload.
- The workflow can execute on a hosted runner without an owner-operated always-on server. It still sends traffic from a real service egress point; IP ranges and execution regions remain provider-visible. Do not claim that the provider becomes location-blind.
- Select an actual provider-permitted execution region and record route/egress metadata. Provider eligibility and data policy remain hard gates, not account- or location-switching triggers.
- Keep the existing three-server topology as a separate local lane; cloud workers complement it and receive no automatic access to server credentials.

Official technical sources reviewed:
- GitHub OIDC short-lived tokens: https://docs.github.com/en/actions/concepts/security/openid-connect
- GitHub-hosted runner network/IP behavior: https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- GitHub cloud-agent scope and secret isolation: https://github.com/github/docs/blob/main/content/copilot/responsible-use/agents.md
- Jules task VM, repository and branch selection as a cloud coding-agent reference: https://jules.google/docs/

GitHub's OIDC guidance describes short-lived credentials when a trust relationship is configured. Its runner guidance describes many hosted-runner IP ranges and recommends against treating the dynamic ranges as a fixed internal allowlist. Product-specific account terms, provider routes and current eligibility remain separate evidence items.

## 6. Source gaps, chosen path and blocked decisions

| Item | Source-bound status | Selected next action |
|---|---|---|
| Agent/provider catalog schema | Existing `profiles/agent-registry.json` v1.2.0, no linked schema file evidenced in this pass | Create an additive versioned admission-schema proposal; preserve existing catalog IDs and consumers |
| Provider registry schema | v1.0.0 exists but is intentionally narrow | Keep as provider-selection input; supplement with task admission policy at a higher boundary rather than overloading provider selection |
| A0 accepted issuer/ingress | D2 trusted-context proposal is NOT ACCEPTED / NOT FROZEN | Reconcile exact accepted A0 ingress and issuer lifecycle source before implementation of write-capable agent admission |
| R-06 audit/privacy | Acceptance route unestablished; template unfilled | Keep R-06 OPEN; do not invent authority, event semantics, retention or fail-open behavior |
| Secret store | MH-12 says exact store is non-canonical pending evidence and ADR | Choose per-service scoped secret references provisionally; do not standardize an unapproved vault |
| Endpoint allowlisting | MH-21 egress controls are PROPOSED; provider Wave 30/31 found request-time destination gaps | Require a central policy gate before transport; endpoints come from the approved route catalog, never agent output |
| Distributed claim store | Existing ClaimStore is filesystem-local | Compare only components already admitted or selected in the component manifest; if none provides multi-runner atomic claims, keep cross-runner writes serial and raise one documented gap |
| Target manifest | Component manifest exists; one accepted target deployment manifest has not been demonstrated by the inspected source set | Locate exact authoritative target manifest by current map and repository tree; do not substitute component manifest |
| Qualification | G0–G11 are BLOCKED | Keep production admission closed until fresh revision-bound evidence and independent A3 review pass all required gates |

## 7. Implementation order

W36-A: Complete this crosswalk and route open decisions without minting new stable IDs prematurely.

W36-B: Produce a proposed JSON Schema for catalog admission and an offline structural validator, with compatibility fixtures for `profiles/agent-registry.json`, `.github/agent-system/registry.yaml`, provider schemas and the 23-lane manifest. Do not enable a provider or change runtime routing in the schema-only work.

W36-C: Create a source-bound change proposal for the distributed claim authority and task envelope, including crash/stale-lease/cancellation/replay cases. Reuse the existing component manifest; do not add a second scheduler or database by default.

W36-D: After governance reconciliation, implement the minimum compatibility-preserving validator and dedicated tests on a feature branch rooted at the current main SHA. Ensure workflow path filters and the self-hosted 24-hour queue workflow are understood before choosing touched paths.

W36-E: Run authorized offline tests against the immutable candidate commit; then a synthetic, read-only hosted-runner workflow with no provider credentials. Only after independent evidence may a provider-specific probe be authorized for one named agent, account, model, data class, route and cost ceiling.

W36-F: Enroll patch-writing agents one at a time via an isolated task branch and PR-only outputs. Every result receives independent validation. G0–G11 and human launch/release authority remain unchanged.

## 8. Verification boundary

This pass read current GitHub file content and source SHAs. It did not modify runtime code or workflows, access credentials, invoke a model/provider, dispatch Actions, run tests, inspect an execution host, change infrastructure or deploy. The current qualification truth remains BLOCKED. This report is source-bound design/reconciliation evidence, not runtime qualification or admission.
