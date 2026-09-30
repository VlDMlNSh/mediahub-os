# MediaHub OS / MediaHub iOS — MH-4 Security Architecture

Date: 2026-09-30
Status: RECONCILED ARCHITECTURAL BASELINE — NOT YET FROZEN
Scope: MH-4 — Security Architecture

## 1. Purpose and authority boundary

MH-4 defines the MediaHub security foundation and cross-cutting security control model.

Security is a prerequisite to protected execution. It is not a second canonical state authority.

MediaHub State Authority remains the canonical platform authority. Security may authenticate, authorize, deny, revoke, quarantine, enforce, contain and record security facts, but it must not create a competing State Authority.

Security enforcement is centralized as a logical control plane and distributed to the domains that execute protected operations.

## 2. Security decision model

Canonical security evaluation:

Identity
+ Device Trust
+ Capability
+ Authorization
+ Policy
+ Context
+ Continuous Verification
-> Security Decision

No individual factor is sufficient for trust.

In particular:
- network visibility != trust;
- authentication != authorization;
- identity != capability;
- capability != permission;
- permission != current authorization;
- process liveness != trust;
- discovery != qualification;
- qualification != permanent trust.

Default security posture:
- deny;
- least privilege;
- authenticated;
- qualified;
- encrypted according to classification;
- audited;
- locally enforceable where possible;
- no unnecessary exposure.

Critical ambiguous security decisions fail closed.

## 3. Identity architecture

MediaHub uses one logical identity architecture with distinct principal classes:

- User Identity;
- Node Identity;
- Device Identity;
- Service Identity;
- Workload Identity;
- Application Identity;
- Cluster Identity;
- External Integration Identity;
- Developer Identity.

User identity is never equivalent to device identity.

Every privileged service and workload has its own scoped identity. A universal service credential is prohibited.

Identity lifecycle is persistent where required, verifiable, auditable and revocable.

## 4. Node and device trust

Every MediaHub node has a unique cryptographic identity.

Trust is dynamic and qualification-bound.

Canonical device lifecycle:

Unknown
-> Discovered
-> Identified
-> Pending Qualification
-> Qualified
-> Trusted
-> Admitted
-> Active
-> Degraded
-> Quarantined
-> Revoked

Discovery alone never grants production access.

Unknown Device -> DENY / QUARANTINE.

Admission requires, as applicable:
1. identity;
2. hardware/software qualification;
3. capability profile;
4. security assessment;
5. policy admission;
6. runtime admission.

Failed integrity, compromised credentials, unexpected software, policy violation or other security evidence can lower trust and trigger quarantine/revocation/requalification.

Hardware-backed identity and attestation are preferred where supported, including TPM, Secure Enclave, platform keystore and secure boot/measured boot. Unsupported hardware does not receive capabilities that depend on unavailable security primitives; capability is reduced or trust is constrained.

## 5. Authentication

Authentication answers "who are you?" and is separate from authorization.

Supported authentication factors may include:
- cryptographic credentials;
- platform/device-bound credentials;
- passwords where appropriate;
- hardware security keys;
- adaptive MFA;
- biometrics.

Biometrics are an authentication factor, not the canonical identity. Sensitive operations may require step-up authentication and fresh authorization.

## 6. Authorization

Authorization evaluates:

Who
+ Device
+ Workload
+ Capability
+ Resource
+ Action
+ Context
+ Policy
-> Decision

The authorization model combines:
- RBAC for stable roles;
- ABAC for attributes and contextual conditions;
- capabilities for bounded authority;
- policy for the final decision.

Authorization failure never falls back to a broader role.

Least privilege is mandatory. Permanent unrestricted administrator, filesystem, network, secret or device-control access is prohibited unless an explicitly qualified architecture requires a narrowly scoped equivalent.

Privileged access is preferably Just-In-Time:
- temporary;
- capability-scoped;
- auditable;
- revocable;
- policy-controlled.

## 7. Continuous verification

Trust is not permanent.

Verification may occur:
- at login;
- during device admission;
- at API invocation;
- immediately before sensitive operations;
- when context changes;
- when risk changes;
- during credential rotation;
- after recovery;
- after network transitions;
- after software updates.

Critical operations require a fresh authorization/policy decision immediately before execution. This includes security settings, access control, surveillance, locks, credentials, recovery, destructive and irreversible operations.

## 8. Cryptographic trust and key hierarchy

Conceptual hierarchy:

Root Trust
  -> Platform / Device Trust
  -> Node Identity
  -> Service / Workload Identity
  -> Session / Ephemeral Credentials

One universal MediaHub master key is prohibited.

Keys are protected separately from the data they protect. Hardware-backed storage is used where available.

Encryption requirements:
- sensitive data, secrets, credentials, backups and critical state are encrypted at rest according to classification;
- API, control-plane, cluster, remote-access, external-integration and cloud traffic is encrypted in transit;
- end-to-end encryption is used where architecturally required and feasible.

Existing repository decision that SOPS + age are selected secret-protection primitives remains compatible with this model and is retained unless a later architectural contradiction is demonstrated.

## 9. Secret and credential lifecycle

Secrets must not be stored in source code, Git, ordinary configuration, logs or user-visible storage. Plaintext environment exposure is permitted only when explicitly required and bounded by the runtime architecture.

Credential lifecycle:

Issued
-> Active
-> Rotating
-> Rotated
-> Suspended
-> Revoked
-> Destroyed

Lifecycle controls include expiration, rotation, revocation, compromise response and audit.

Secret unavailability removes the affected capability; it never triggers an insecure fallback.

## 10. CPRG boundary

CPRG (Central Protected Registration Gateway) has one specialized role: protected registration of API credentials.

Canonical flow:

Request
-> Authentication
-> Policy
-> Lease
-> Protected Registration
-> Verification
-> Close

CPRG is not:
- a general proxy;
- NAT;
- Internet gateway;
- storage;
- compute;
- Developer node;
- permanent VPN tunnel;
- user-data gateway.

Registration capability != data-plane access.

## 11. Segmentation and trust domains

Minimum logical security zones:

- User;
- System;
- Security;
- Smart Home;
- Network;
- Storage;
- AI;
- Developer;
- Cloud;
- External;
- Quarantine;
- Recovery.

Physical co-location does not collapse trust boundaries.

Critical invariant:

User Network != Developer / Compute Fabric.

Developer Fabric has its own identity, network plane, policy, workload namespace and trust domain.

High-speed links such as Thunderbolt/USB4 are subject to node identity, link qualification, topology validation, workload authorization, traffic isolation, admission and monitoring. A physical link is never automatic trust.

## 12. User Data / Developer Data isolation

User Data Domain and Developer Data Domain are distinct architectural trust domains.

Developer personnel do not receive direct User MediaHub Data access.

Developer Cloud categorically cannot receive User Data.

This is an architectural invariant, not merely an ACL.

Developer workflows use synthetic data, test fixtures, controlled corporate data or explicitly permitted interfaces.

Compute Contribution does not imply User Data access and does not grant Developer Personnel Access.

## 13. Egress security

Every trust-boundary egress follows:

Source
-> Data Classification
-> Destination Classification
-> Authorization
-> Policy
-> Egress Decision
-> Audit
-> Transfer

Applies especially to:
- Internet;
- Cloud;
- Developer Cloud;
- external APIs;
- external storage;
- AI services.

User Data -> Developer Cloud is DENY BY ARCHITECTURE.

Cloud Development has separate identity, trust, secrets, policy, network, egress and audit boundaries and has no operational authority over local canonical MediaHub state.

## 14. AI security

AI is not authority.

AI does not automatically receive:
- secrets;
- unrestricted filesystem access;
- unrestricted network access;
- User Data;
- critical-state mutation rights.

Canonical path:

AI
-> Identity
-> Authorization
-> Policy
-> Consumer Contract
-> State Authority
-> Execution

AI recommendations are not authorization decisions.

For Smart Home:

User / AI
-> MediaHub Policy
-> Home Assistant Core
-> Device

AI never bypasses Home Assistant Core.

## 15. Smart Home and critical operations

Home Assistant Core remains the Smart Home operational authority established by the current master architecture reconciliation.

MH-4 supplies the security boundary around that authority:
- identity;
- capability;
- authorization;
- current policy;
- current state verification;
- audit;
- quarantine/revocation.

For locks, alarms, security devices, critical climate, energy and safety equipment, authorization and policy are checked immediately before execution.

MH-4 does not redefine Home Assistant ownership, failover topology or Smart Home product decisions.

## 16. API and callback security

Every API requires:
- authenticated identity;
- authorization;
- capability scope;
- input/schema validation;
- resource/rate limits;
- replay protection where required;
- audit;
- versioned contract.

Public API access never bypasses the security architecture.

External callbacks require authentication, integrity protection, scope, replay protection and audit. Known source IP alone is insufficient authentication.

## 17. Session security

Sessions carry:
- identity;
- device binding where appropriate;
- expiration;
- revocation state;
- risk context;
- authorization scope.

Sensitive operations may require re-authentication or step-up authentication.

Session existence is not a permanent authorization grant.

## 18. Mobile security

MediaHub iOS OS on iPad is a local MediaHub node and receives node/device/user identity treatment appropriate to its qualified hardware profile.

MediaHub Remote Access on iPhone/Android is a separate remote-access application family and does not become local Core authority.

Remote access requires:
- device identity;
- user identity;
- secure API channel;
- revocation;
- session management;
- policy enforcement.

Lost-device lifecycle:

Detect
-> Revoke
-> Quarantine
-> Recover
-> Re-enroll

## 19. Cluster security

Cluster admission:

Node Identity
-> Link Verification
-> Hardware Qualification
-> Software Qualification
-> Security Qualification
-> Capability Profile
-> Policy
-> Cluster Admission

Cluster trust remains subject to continuous verification.

Security does not create a second cluster authority. The existing one-logical-distributed-State-Authority model remains authoritative.

## 20. Secure bootstrap and runtime admission

New node bootstrap:

Hardware Detection
-> Identity Bootstrap
-> Integrity Verification
-> Security Qualification
-> Capability Qualification
-> Policy Admission
-> Runtime Admission

Runtime admission:

Identity
-> Integrity
-> Qualification
-> Trust
-> Authorization
-> Policy
-> Admission
-> Execution

Runtime cannot bypass the security control plane.

## 21. Software integrity and supply chain

Security qualification considers:
- source provenance;
- signed artifacts;
- SBOM;
- dependency graph;
- reproducibility where required;
- vulnerability status;
- license;
- build provenance;
- artifact integrity.

Critical software boundary changes trigger requalification.

OSS production admission requires:
Capability Gap
-> Research
-> Provenance
-> License
-> Security
-> Maturity
-> Compatibility
-> Benchmark
-> Qualification

Unknown software is not production-admissible.

Existing evidence tooling (including artifact signing, SBOM and vulnerability scanning) is evidence consumed by policy; tooling itself is not release authority.

## 22. Plugin security

Plugins do not inherit MediaHub Core authority.

Each plugin requires:
- identity;
- capability declaration;
- resource scope;
- network scope;
- data scope;
- version;
- provenance;
- qualification status.

Plugin architecture details remain owned by MH-8; MH-4 defines the security boundary.

## 23. Recovery security

Recovery credentials are separate from ordinary credentials and are:
- protected;
- auditable;
- policy-controlled;
- revocable;
- minimally scoped.

Recovery is a security capability, not unrestricted administrator access.

Critical recovery may require quorum, hardware key, multi-factor approval or isolated recovery environment. Detailed implementation belongs to MH-16.

## 24. Quarantine and incident model

Quarantine is an explicit security state.

A quarantined node/device:
- does not receive ordinary trust;
- is network/data restricted;
- does not execute privileged workloads;
- may perform bounded diagnostics;
- may undergo requalification.

Security incident lifecycle:

Detect
-> Classify
-> Contain
-> Revoke
-> Quarantine
-> Preserve Evidence
-> Recover
-> Requalify
-> Restore
-> Audit
-> Learn

Automatic destructive remediation is prohibited unless explicitly authorized by policy.

Security event classes:
- informational;
- warning;
- suspicious;
- security incident;
- critical security incident;
- compromise suspected;
- compromise confirmed.

## 25. Audit and observability boundary

Security evidence is linked to:
- identity;
- node;
- device;
- service;
- workload;
- network;
- API;
- action;
- policy;
- result;
- timestamp;
- provenance.

Audit records capture, as applicable:
- who;
- what;
- when;
- source/context;
- target;
- identity;
- policy;
- capability;
- result;
- provenance;
- resulting canonical revision for mutations.

Audit is evidence, not authority.

Observability may expose security state, events, incidents and health but cannot grant trust, authorize actions or mutate canonical state.

Credentials, private keys and unrestricted authentication material must not be emitted into telemetry.

## 26. Privacy boundary

Security and Privacy remain separate concerns.

Security determines whether protected resources and operations are technically guarded.

Privacy determines whether data may be used or transferred in a particular context.

MH-4 supplies enforcement mechanisms required by privacy policy but does not absorb MH-13.

## 27. Failure and availability model

For critical security decisions:

FAIL CLOSED.

Examples:
- unknown identity;
- unknown device;
- unknown state;
- expired/revoked credential;
- failed integrity;
- missing policy;
- ambiguous authorization;
- unavailable required security dependency.

Security must not unnecessarily destroy availability. Qualified emergency/local fallback may exist only when explicitly pre-qualified, capability-scoped, policy-controlled and audited.

## 28. Security invariants

S-01 Unknown Device -> DENY / QUARANTINE.
S-02 Discovery != Trust.
S-03 Authentication != Authorization.
S-04 Identity != Capability.
S-05 Capability != Permission.
S-06 Trust is continuously verifiable.
S-07 Least privilege by default.
S-08 Critical operations require fresh authorization/policy.
S-09 AI is not authority.
S-10 Cloud is not authority.
S-11 Developer Domain has no User Data access.
S-12 Developer Cloud categorically cannot receive User Data.
S-13 No hidden backdoors.
S-14 No permanent unrestricted developer credentials.
S-15 CPRG is registration-only.
S-16 Registration capability != data-plane access.
S-17 User Network != Developer Fabric.
S-18 Runtime admission requires security qualification.
S-19 Failed security verification can cause quarantine/revocation.
S-20 Security does not create a competing State Authority.
S-21 Security decisions are auditable.
S-22 Sensitive data is encrypted according to classification.
S-23 Ambiguous critical security decisions fail closed.

## 29. Forbidden paths

The following paths are architecturally forbidden:

- AI -> direct State Authority mutation;
- AI -> direct Smart Home device;
- Developer -> User Data;
- Developer Cloud -> User Data;
- Cloud Development -> local canonical authority;
- Unknown Device -> Production;
- UI -> privileged internal service without the security/contract path;
- Plugin -> unrestricted system access;
- CPRG -> general data plane;
- Observability -> authority;
- Debug -> permanent root;
- network reachability -> implicit trust;
- authentication success -> implicit authorization;
- physical high-speed link -> implicit admission.

## 30. Security qualification gates

A production admission candidate must demonstrate, at minimum:

1. identity establishment;
2. credential protection;
3. device/node qualification;
4. software integrity;
5. capability profile;
6. authorization correctness;
7. least privilege;
8. secret lifecycle;
9. credential rotation/revocation;
10. quarantine behavior;
11. segmentation and egress enforcement;
12. AI/plugin/cloud authority isolation;
13. API/callback protection;
14. audit completeness;
15. fail-closed behavior;
16. recovery security;
17. supply-chain evidence;
18. independent verification;
19. reproducible evidence/provenance.

Discovery or architecture description alone is not qualification evidence.

## 31. Cross-architecture handoff

MH-4 provides security contracts to:
- MH-5 Integrations;
- MH-6 Core Runtime Services;
- MH-7 Policy;
- MH-8 Plugins;
- MH-10 AI;
- MH-11 Observability;
- MH-12 Security Analysis / Threat Model;
- MH-13 Privacy;
- MH-14 Persistence;
- MH-15 OS / Appliance;
- MH-16 Update / Recovery;
- MH-17 Devices / Protocols;
- MH-21 Hybrid Cloud;
- MH-22 Qualification / Production;
- MH-23 Migration.

MH-4 does not absorb the implementation or detailed architecture owned by those lanes.

## 32. Reconciliation result

The current MH-4 product-security decisions supplied in the master prompt are internally consistent with the existing Security / Trust / Authorization contract and with the active master architecture checkpoint.

No competing State Authority is introduced.
No direct AI, Cloud, Developer or Plugin authority is introduced.
User/Developer data separation remains architectural.
CPRG remains registration-only.
Security remains a cross-cutting control plane with distributed enforcement.
The existing SOPS + age secret-protection decision remains compatible.
The current Smart Home authority decision remains unchanged.

No new product-owner decision is required to establish the MH-4 security foundation described here.

## 33. Status discipline

This document is a reconciled architectural baseline. It is not, by itself, evidence of production qualification or implementation completion.

MH-4 status: RECONCILED / OPEN FOR ARCHITECTURE FREEZE REVIEW

Closure requires the project's normal acceptance/freeze gate and recorded evidence. Implementation qualification belongs to the dedicated development/qualification lanes.
