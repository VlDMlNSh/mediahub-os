# MediaHub OS — Location-Independent Cloud-Agent Credential Registration, Wave 12
Date: 2026-10-16
Contour: A — Developer Fabric
Status: DOCUMENTARY DESIGN / PROPOSED / NOT IMPLEMENTED / NOT QUALIFIED

## 1. Owner requirement and decision

Preserve the existing three-server topology:
1. Mac mini 2018 running macOS.
2. Mac mini 2011 running Linux.
3. Remote video server.

Design API credential registration independently from any one server, network ingress, public IP, physical location, or runtime worker. There is no required single internet entry point for cloud-agent registration or task admission. The system may continue to use servers and provider APIs; this wave changes credential identity and selection semantics only, not the topology.

Key distinction: registration identity is separate from execution location. A provider credential is stored once as a logical credential record and referenced by policy. A task or worker requests an authorized credential reference; the secret broker resolves it at execution time under policy. The key is not assigned permanently to a host. Actual API requests still egress from whichever approved runtime performs the request, and a provider may independently enforce account, region, IP allowlist, organization policy, or risk controls. This architecture cannot override provider restrictions or guarantee identical eligibility from every network.

## 2. Proposed logical architecture

```text
Operator / approved registration workflow
                 |
                 v
Credential registration contract
  - provider + account/project identity
  - secret value submitted over approved secure channel
  - data classification and permitted capabilities
  - provider restrictions / allowed egress classes
                 |
                 v
Credential vault / secret manager (logical service)
  - encrypted secret custody
  - stable opaque credential_id
  - version, owner, status, expiry, scope metadata
  - audit and revocation
                 |
                 v
Policy and task admission (ASTRA A0 boundary)
  - task audience + capability + data class
  - provider/model allowlist
  - credential eligibility decision
                 |
                 v
Short-lived credential lease / just-in-time resolution
                 |
        +--------+---------+
        |        |         |
        v        v         v
   macOS host  Linux host  Remote video server
   Mac mini    Mac mini    approved tasks only
   2018        2011
                |         /
         -------+--------/
             outbound API calls
             from selected runtime
```

This is a logical flow, not a claim that a vault or broker is already deployed. The vault may be an existing approved secret manager or a future adapter. The exact implementation depends on the accepted target manifest and A0/R-06 governance.

## 3. Registration contract

A credential record contains metadata only:
- credential_id: opaque stable identifier, never the secret itself;
- provider_id and account_or_project_id;
- secret_version reference held by the vault;
- scope/capabilities and permitted task classes;
- permitted data classifications;
- provider-declared constraints: region, IP/network allowlist, account restrictions, model/API eligibility;
- registration actor, creation time, expiry/rotation deadline, current status;
- policy bundle digest and audit event reference.

The secret value belongs only in the secret manager's protected write path. It must not appear in Git, issue text, pull requests, workflow outputs, logs, task envelopes, model prompts, artifacts, telemetry labels, or the component registry.

## 4. Resolution contract

1. A task requests a credential_id plus provider/model and required capability; it never supplies raw secret material.
2. A0 admission checks actor, task audience, data class, allowed provider/model, expiry, policy version and permitted egress class.
3. The secret broker resolves the current secret version only for an admitted worker with an active short-lived lease.
4. The worker receives the secret through the narrowest supported runtime secret channel; values are masked in logs and excluded from artifacts.
5. Every use emits metadata-only audit evidence: task ID, credential_id, version, provider/model, worker identity, egress class, policy decision, timestamps and outcome. Secret values and authorization headers are excluded.
6. Revocation blocks future resolution, cancels leases where feasible, and invalidates cached credentials. Rotation creates a new secret version while preserving credential_id and audit history.
7. If provider policy requires a fixed egress IP or region, admission routes the task to a compliant egress class or returns a policy denial. It must not silently tunnel through an unapproved proxy or expand the destination allowlist.

## 5. No single ingress requirement

Cloud-agent admission and credential registration must use authenticated, policy-checked interfaces rather than depending on a single public ingress server. Supported transport patterns may include GitHub-originated approved workflows, outbound polling/long-polling from registered workers, or authenticated event delivery through an approved transport. These are design options pending A0 lifecycle and target-manifest resolution.

The design does not require all API traffic to originate from one server. Each of the three existing hosts may run only its assigned and approved workloads. Network egress remains explicit, logged and constrained by provider policy. An API key's registration record remains independent of which host eventually consumes it.

## 6. Three-server placement invariants

- Mac mini 2018 / macOS: an eligible worker and/or coordination role only as permitted by the accepted target manifest.
- Mac mini 2011 / Linux: an eligible worker and/or service role only as permitted by the accepted target manifest.
- Remote video server: its existing video-server role remains intact; cloud-agent tasks are allowed only where explicitly admitted and isolated from video workloads.
- No host becomes the universal public ingress solely to register API keys.
- No host identity is used as the credential's permanent identity.
- No assumption is made that all hosts have equivalent egress IP, geography, firewall policy, provider eligibility, or trust level.
- Host placement and provider access are separate decisions: policy chooses a compatible execution location per task.

## 7. Failure, availability and security

- Vault unavailable: fail closed for tasks needing a secret; continue credential-free source analysis and deterministic work.
- Provider rejects source IP/region: record a policy/provider denial and select only another already-approved compatible runtime or provider.
- Expired/revoked key: deny resolution, alert through approved telemetry and require rotation/re-registration.
- Provider outage/quota: bounded retry and circuit breaker; provider fallback only when explicitly allowed for the task and data class.
- Compromised worker: revoke worker lease and its task-scoped access; rotate affected credentials according to incident policy.
- Registration replay: use authenticated actor identity, nonce/idempotency key, expiry and append-only audit.
- Cross-task leakage: isolated execution, task-scoped secret injection, no shared mutable secret files, and cache/output scrubbing.
- Audit logs contain credential references and decisions, never secret material.

## 8. Provider-independent guarantees and limits

Guaranteed by the proposed MediaHub design:
- Credential records are logically independent of physical host placement.
- A task selects an approved credential reference by policy.
- Secret resolution is just-in-time and revocable.
- The architecture has no mandatory single public ingress for credential registration.
- Three-server topology remains intact.

Outside MediaHub's control:
- Provider-side IP or region restrictions.
- Account/project-level policies, model access and API enablement.
- Provider risk decisions, rate limits, quotas and terms.
- Network routes and public egress identity of each host or hosted runner.

Therefore, “location-independent registration” means decoupled credential registration and host binding; it does not mean bypassing provider controls or guaranteeing provider acceptance from every location.

## 9. Governance and acceptance gates

Open dependencies:
- A0 issuer, task audience, lease, revoke and credential-resolution lifecycle.
- R-06 data-classification and provider-routing authority.
- Accepted target manifest identifying the roles and egress characteristics of all three servers.
- Approved vault/broker choice and key rotation/incident procedure.
- Provider-specific terms and restrictions recorded as policy metadata.
- Independent security review and authorized qualification.

Acceptance criteria:
1. Register a credential without selecting a permanent host.
2. Store only opaque credential references and metadata in task envelopes and repository artifacts.
3. Resolve a secret only for an admitted task, approved provider/model and valid lease.
4. Demonstrate revocation, expiry, rotation, replay rejection and audit completeness using separately authorized qualification.
5. Demonstrate that the three host roles remain unchanged and placement follows task policy.
6. Demonstrate explicit denial when provider IP/region restrictions conflict with the selected runtime.
7. Verify logs, traces, artifacts and model context contain no secret values.
8. Distinguish documentation, implementation, test, qualification, deployment and acceptance evidence.

## 10. Current status and next step

Status is design-only. No credential was accessed, created, tested or transmitted. No provider call, workflow dispatch, host/runtime inspection, installation, test, infrastructure change, qualification, deployment or branch integration occurred.

Next: reconcile this contract with exact A0 issuer/lifecycle and R-06 sources, then bind the credential registration/resolution fields into the existing canonical task schema and traceability matrix. Preserve the three-server topology and retain the target as UNKNOWN until an accepted manifest and independent evidence exist.
