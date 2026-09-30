# MH-21 — Hybrid Cloud Architecture — Etalon Candidate

Status: ETALON CANDIDATE / RECONCILED / NOT QUALIFIED
Scope: MediaHub OS / MediaHub iOS
Authority: Local State Authority remains canonical. Cloud is optional capability infrastructure.

## 1. Absolute invariants
- Local State Authority is the sole canonical mutation authority.
- Home Assistant Core remains Smart Home operational authority.
- AI, Cloud, Knowledge Graph, Mobile Remote and Developer Cloud are non-authoritative.
- User Cloud and Developer Cloud are separate trust domains.
- Developer Cloud and Developer Compute Fabric categorically receive no User Data.
- Unknown destination/service and unclassified egress are DENY.
- Critical ambiguity is FAIL CLOSED.
- No Cloud Service may directly control a device or overwrite canonical local state.
- Cloud failure must not become local system failure for critical local functions.
- User Compute Contribution is absent from the accepted architecture.

## 2. Trust domains
T0 Untrusted Internet
T1 Unknown Cloud Service
T2 Identified but Unqualified Service
T3 Qualified External Service
T4 Approved User Cloud
T5 Approved Developer Cloud

Trust level never replaces authorization.

User Cloud and Developer Cloud have separate identity, credentials, policy, audit, classification, network, secrets, storage, artifact, revocation and recovery boundaries.

## 3. Hybrid topology
Local MediaHub Domain
 -> Security / Egress Gateway
 -> Qualified User Cloud services

Developer Cloud is a separate corporate domain and is reachable only by approved corporate engineering flows. It is not an extension of User Cloud.

## 4. User Cloud capability classes
Remote access/relay, push notifications, backup/DR, approved cloud AI, optional storage/synchronization, service health, bootstrap/account support, controlled diagnostics and explicitly approved integrations.

No User Cloud component becomes State Authority.

## 5. Developer Cloud capability classes
Development, CI/CD, corporate AI, OSS research, model registry, artifact generation, qualification support, corporate knowledge and controlled continuous learning.

Permitted inputs: corporate source, source-controlled code, synthetic/sanitized qualification data, approved OSS, corporate research and qualification artifacts.

Forbidden inputs: User Media, Documents, Smart Home state, Knowledge Graph, Digital Twin, credentials, secrets, private prompts, operational history and production User Data.

## 6. Cloud Service Record
Required fields:
service_id, service_type, provider, endpoint, region, jurisdiction, trust_domain, identity,
capabilities, data_classes, allowed_ingress, allowed_egress, retention, residency,
encryption, credential_reference, qualification, version, contract, SLO, quota,
cost_policy, audit_policy, lifecycle, revocation_state.

Registration does not imply trust.

## 7. Qualification lifecycle
Discover -> Identify -> Authenticate -> Contract -> Security Qualification ->
Privacy Qualification -> Data Classification Qualification -> Residency Qualification ->
Egress Qualification -> Performance Qualification -> Operational Qualification ->
Policy Admission -> Production.

Unqualified service = DENY.

## 8. Data classes
Public; Corporate; User; Sensitive User; Security Sensitive; Credential/Secret;
Critical Operational; Restricted Engineering; Developer Corporate; Synthetic/Test.

Every class has destination, residency, encryption, retention, logging, masking, redaction,
transfer and recovery policy.

## 9. Egress
Source -> Identity -> Classification -> Destination Classification -> Policy ->
Minimization -> Redaction/Transformation -> Encryption -> Egress Authorization ->
Transfer -> Verification -> Audit.

Application -> Internet is forbidden for system cloud flows.

## 10. Cloud AI
Application -> AI Gateway -> Identity -> Data Classification -> Context Policy ->
Egress Policy -> Qualified Cloud AI -> Result Validation -> MediaHub.

Context is minimal, purpose-bound, capability-bound, auditable and revocable.
Cloud AI produces proposals/results, never authority.

Critical operations require:
Proposal -> MediaHub Validation -> Policy -> Authorization -> Domain Authority ->
Execution -> Verification.

## 11. Remote access
MediaHub Identity + device trust + API gateway + authorization + policy + risk/context + audit + revocation.
Cloud relay is transport only. Personal VPN remains a MediaHub Gateway capability.

## 12. Notifications
Push is optional. Local notification state remains available. Payload is minimized,
opaque where possible, encrypted where supported, and reconstructable locally.

## 13. Backup / DR
Optional, encrypted, versioned, integrity-verified, residency-aware and independently recoverable.
Restore: Recovery Point -> Integrity -> Trust -> Qualification -> Restore -> State Validation -> Policy Validation -> Admission.

## 14. Storage
User Cloud Storage, Developer Storage and Artifact Storage are separate.
Object storage abstractions must expose provider, residency, encryption, identity, policy,
lifecycle, retention, deletion and integrity.

## 15. Cloud database
Only derived/sync/remote metadata/notification/index/backup metadata/service state.
Canonical critical state remains local.

## 16. Events
Authenticated producer/consumer, schema/version, correlation ID, timestamp, replay protection,
ordering semantics where required, TTL, policy and audit.
Cloud event bus is not canonical event authority.

## 17. Synchronization
Local Authority -> approved cloud representation.
Cloud-to-local mutation requires identity, authorization, policy, contract and State Authority admission.

## 18. Failure / partition
Local critical state and qualified local capabilities continue.
Cloud-only functions degrade explicitly.
Stale cloud commands expire; unsafe operations are not blindly replayed.
Leases, freshness and replay protection are enforced; recovery triggers reconciliation.

## 19. Cloud commands
Cloud Request -> Identity -> Device Trust -> Capability -> Authorization -> Policy ->
Freshness -> Contract -> State Authority -> Domain Authority -> Execution -> Verification -> Audit.

No direct cloud-to-device-adapter path.

## 20. Credentials / secrets
Short-lived, scoped, revocable credentials with protected storage and hardware-backed protection where available.
CPRG remains registration-only.
Secret values never enter logs, Knowledge Graph, Developer Cloud or ordinary UI/context.

## 21. Egress Gateway
Destination policy/allowlist, identity, classification, protocol validation, TLS/certificate validation,
DNS policy, rate limiting, quota, metering, audit, revocation and anomaly detection.
Gateway is not State Authority.

## 22. Network separation
User LAN, Smart Home, Media, Management, Security, Developer/Compute Fabric, Cloud Egress
and External Integration traffic are separate policy boundaries.
Developer Fabric has no automatic route to User Data Plane.

## 23. Developer Cloud -> Production
Build -> Test -> Security Scan -> SBOM -> Provenance -> Qualification -> Approval ->
Signed Artifact -> Distribution -> MediaHub Verification -> Staged Rollout -> Monitor -> Rollback.
Developer Cloud has no operational write access to production State Authority.

## 24. Model Registry / deployment
Model identity, version, provenance, license, training provenance, security, benchmark,
capabilities, hardware/data requirements, qualification and rollback state.
Deployment: Qualification -> Security -> Policy -> Staging -> Canary -> Observation -> Production.

## 25. Resource and cost governance
CPU/GPU/NPU/storage/bandwidth/API/inference quota, cost budget, leases, priority and anomaly detection.
Local critical workloads take precedence over optional cloud workloads.
Scheduling considers locality, privacy, residency, latency, cost, capability, trust and criticality.

## 26. Observability
Record who, what, when, where, why, policy, data class, capability, result, volume, latency,
credential reference and correlation ID. No secret values.
Local observability remains functional during cloud failure.

## 27. Incident response
Detect -> Block -> Revoke -> Preserve Evidence -> Classify Exposure -> Recover -> Requalify.
Compromise of a cloud service must not automatically cross into MediaHub Core.

## 28. Provider failure / migration / exit
Failover only to qualified providers; otherwise local fallback and safe queueing.
Provider abstraction must not hide security semantics.
Critical services require export, replacement, credential migration, endpoint/DNS migration,
rollback and local fallback where feasible.

## 29. Privacy
Minimization, purpose limitation, local processing, explicit policy, retention/deletion,
export, access control, audit, revocation and residency are mandatory.
Developer training is corporate-only and never silently incorporates User Data.

## 30. Plugin / automation boundary
Plugin -> MediaHub API -> Capability -> Policy -> Egress Gateway -> Cloud.
No arbitrary Internet, credentials, DNS, sockets or storage.
Cloud automation requires identity, capability, policy, lease, freshness, idempotency, timeout,
compensation and audit. Local scheduler remains available for qualified critical workflows.

## 31. Capability matrix
| Capability | Local | User Cloud | Developer Cloud | Authority |
|---|---|---|---|---|
| State Authority | YES | NO | NO | Local State Authority |
| Smart Home | YES | Limited | NO | HA Core |
| Media | YES | Optional | NO | Media Domain |
| Documents | YES | Optional | NO | Document Domain |
| Local AI | YES | Optional | NO | Non-authoritative AI |
| Cloud AI | Optional | YES | Corporate only | Non-authoritative AI |
| Developer AI | NO | NO | YES | Developer Domain |
| Backup | YES | Optional | Corporate artifacts only | Recovery Authority |
| Remote Access | YES | Optional relay | NO | MediaHub |
| Notifications | YES | Optional | NO | Notification Domain |
| Storage | YES | Optional User Storage | Corporate/Artifact Storage | Domain-specific |
| Eventing | YES | Optional | Corporate | Local event authority |
| Model Registry | YES/local mirror | Optional | YES | Non-authoritative registry |
| CI/CD | Local optional | NO | YES | Developer Domain |
| Observability | YES | Optional export | Corporate engineering | Non-authoritative |
| Digital Twin | YES | Optional processing | Corporate only for non-user data | Twin Domain |
| Resource Compute | YES | Optional qualified | Corporate | Resource Manager |

## 32. Access decision
Identity + Device Trust + Service Trust + Capability + Data Class + Destination + Policy +
Context + Freshness + Risk -> ALLOW / ALLOW WITH LIMITS / DEFER / QUARANTINE / DENY.

## 33. Cloud audit
Every cloud operation records timestamp, identity, node, service, destination, capability,
data_class, policy, decision, volume, result, latency, credential_reference and correlation_id.

## 34. Closure semantics
Architecture status is not implementation qualification.
Qualification transition: RECONCILED -> VERIFIED -> QUALIFIED.
Production authorization remains a separate gate.

## 35. MH-22 / MH-23 inputs
MH-22: qualification evidence model, service qualification gates, negative tests, residency/egress evidence,
provider failure/recovery evidence, cost/quota controls, artifact/provenance gates.
MH-23: provider migration, contract/versioning, exit strategy, compatibility, deprecation,
data portability and long-term evolution controls.
