# MediaHub OS — Credential Reference and Schema-Gap Crosswalk, Wave 20

- Date: 2026-10-16
- ID: MH-CAF-CREDENTIAL-XWALK-20
- Contour: A — Developer Fabric
- Status: SOURCE-BOUND DOCUMENTARY CROSSWALK / PROPOSED / IMPLEMENTATION AND QUALIFICATION OPEN
- Scope: reconcile location-independent credential registration with the current v0.2 task-envelope and agent-registry candidates, A0/MH-12 issuer boundaries, R-06 governance and target-manifest status.
- Owner topology: preserve Mac mini 2018/macOS, Mac mini 2011/Linux and remote video server. Hosted ephemeral workers remain an additive execution lane.

## 1. Decision boundary

Credential registration identity and execution placement are separate dimensions. A logical credential record must be addressable without permanent assignment to one physical host or one public ingress. The secret itself belongs only in an approved secret manager's protected write and resolution path.

This does not remove outbound provider traffic or override provider-side account, project, IP, region, quota, billing, terms or data-handling controls. The selected worker still originates the provider request. A provider route that conflicts with the worker's eligible egress profile must be denied or routed only to an independently approved compatible profile.

This crosswalk is documentary. It does not select a vault, issuer, wire protocol, endpoint, runtime or physical target.

## 2. Exact source revisions reviewed

| Source | Ref | Blob SHA | Established scope |
|---|---|---|---|
| Location-Independent Cloud-Agent Credential Registration, Wave 12 | docs branch | `5c0eb33ecb68bb55648a9dbf07b61394bd404786` | Proposed logical credential record, vault-held secret reference, just-in-time resolution, leases, rotation/revocation and provider-aware egress |
| Cloud-Native Credential and Egress Architecture, Wave 14 | docs branch | `21ab57f932594bed670583d0eb66d4abb076755f` | GitHub-hosted ephemeral worker default, runtime-only secret injection, direct outbound HTTPS |
| Direct-Egress Decision, Wave 18 | docs branch | `d7730895d97f84fc8ff25d1fdda61558dbd50696` | No owner-operated persistent server in the default provider path; hosted egress remains visible to providers |
| Task Envelope Schema v0.2 | docs branch | `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a` | Proposed task authority, data policy, provider/model destination authorization, budgets and evidence references |
| Agent Registry Schema v0.2 | docs branch | `b49b89b8fbdfc180862e3dc78f8198f35e486035` | Proposed agent identity, capabilities, provider routes, authorization references, expiry and revocation |
| A0 Lifecycle / MH-12 Issuer Source Trace, Wave 07 | docs branch | `49ca0b69737bf8d44fe3a42daa47fd9157c9097d` | Source trace; accepted ingress, issuer, audience, expiry, revocation and replay contract remain open |
| R-06 Governance Disposition Template, Wave 07 | docs branch | `834fd1ab70eee88355844ba2ebba6c2b6c47ecdb` | Unfilled audit/privacy decision template; no governance acceptance |
| Clean Target Manifest Authority Reconciliation, Wave 10 | docs branch | `1f748bf80e08067fd85a7e1b0821cc4d12bda676` | No owner-accepted exact deployment target manifest in the reviewed source set |

## 3. Cross-schema findings

### 3.1 Task envelope v0.2

The task schema requires `routing.authorized_destinations[]` entries with `provider_id`, `model_id`, `authorization_ref`, `eligibility_evidence_ref`, `data_policy_revision` and `quota_bucket`. It also has task-level authority and data-policy references.

The current candidate contains no explicit `credential_id` / `credential_ref` field. The generic `authorization_ref` must retain authorization semantics; overloading it to mean a secret selector would conflate distinct controls.

### 3.2 Agent registry v0.2

The agent registry's `provider_routes[]` entries bind provider/model, data classes, purpose, policy reference, authorization reference and a paid-fallback boolean. Its authorization and lifecycle objects cover agent grant references, scope digest, expiry and revocation.

The current candidate has no dedicated credential record identity, vault secret-version reference or provider account/project binding. Agent lifecycle is not equivalent to credential lifecycle. The registry is an agent admission record, not a complete secret-custody registry.

### 3.3 Disposition

These are source-level schema gaps relative to the Wave 12 design, not evidence of a live security defect: both schemas are proposed candidates and neither creates runtime authority. Preserve the current v0.2 candidates unchanged pending accepted A0/MH-12/R-06 contracts and independent review.

## 4. Recommended contract composition

Keep three records and their authorities distinct:

1. **Credential record** — stable opaque `credential_id`; provider and account/project identity; vault-only secret-version reference; allowed capabilities/task classes and data classifications; provider restrictions including region/IP/organization requirements; owner, status, timestamps, expiry/rotation deadline and revocation reference; policy revision and metadata-only audit references.
2. **Agent record** — agent identity, immutable workflow revision, allowed task/data/path capabilities, provider routes, issuer/grant/reviewer references, expiry/revocation and provenance.
3. **Task envelope** — task identity, source SHA, requester/admission references, data policy, authorized provider/model route, explicit credential reference, quota/budget, deadline, output bounds, review and evidence requirements.

Proposed future field semantics:
- `credential_id` is an opaque stable identifier, not a secret and not a host identifier.
- `credential_ref` in an authorized destination resolves to that identifier through the accepted credential registry.
- A vault secret-version reference is resolvable only by the secret broker; it must never be copied into a task envelope or worker artifact.
- Provider/account/project and credential eligibility must match the selected destination, task capability, data class, policy revision and eligible egress class.
- A0 admission authorizes the task and lease; the secret broker resolves the secret only after admission, for the narrowest supported runtime channel and short lease.
- Revocation/expiry blocks new resolutions and invalidates leases/caches where supported. Rotation advances the secret version while preserving credential identity and audit lineage.
- Audit events record identifiers, revisions, actor/worker, task, route, egress class, policy decision and outcome; secret values and authorization headers remain excluded.

These field semantics are a design recommendation, not an accepted schema revision. A later versioned credential-record schema and a compatible task/agent schema change require separate source review and approval.

## 5. Admission and privacy gates

- **A0 / MH-12:** accepted issuer, caller/audience, capability binding, lease, expiry, revocation, replay/idempotency, cancellation and recovery contract remain open in the reviewed source trace.
- **R-06:** accountable authority, event schema, data classification, sink durability, outage behavior, retention/deletion, access control, integrity, clock/correlation and independent verification remain unfilled.
- **Target manifest:** exact approved runner/workspace/network profile remains UNKNOWN. The historical three-server topology is owner direction; this does not itself qualify those hosts or establish that they are the default provider execution path.
- **Schema validation:** full JSON Schema Draft 2020-12 meta-validation, format assertions, positive/negative fixtures and semantic reference resolution remain open under CAF-Q-014.
- **Vault/broker:** no implementation has been selected or qualified by this crosswalk.
- **Provider constraints:** no proxy, VPN, source-location spoofing or unapproved fallback is proposed. Provider restrictions remain authoritative.

## 6. Acceptance criteria for a later schema revision

1. Credential identity remains independent of physical host and public ingress.
2. Task and agent records carry only opaque credential references; no raw secret or vault secret version leaks into ordinary task metadata.
3. Provider/account/project, model, capability, data class, policy revision and egress eligibility are cross-validated.
4. Resolution is limited to an admitted task, authorized worker, valid lease and approved destination.
5. Expiry, revocation, rotation, replay rejection and audit completeness have revision-bound negative-path evidence.
6. The three-server topology remains unchanged; any hosted runner is an additive, explicitly described execution target.
7. Missing authority, unresolved reference, provider restriction conflict or unknown target results in BLOCKED/DENY.
8. Standards validation and independent security/privacy review precede any runtime activation.

## 7. Work boundary and next step

This pass used GitHub source reads and branch metadata only. No schema candidate was edited, no secret or credential was accessed, no provider/model was called, no workflow was dispatched, and no test, installation, host/runtime inspection, infrastructure change, qualification, deployment or branch integration was performed.

Next: preserve this crosswalk in the roadmap, traceability matrix, source registry, project map and continuation checkpoint. Keep CAF-Q-014, CAF-Q-001, CAF-Q-002 and CAF-Q-012 open; schema design work does not close those gates.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
