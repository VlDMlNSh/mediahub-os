# CPRG Trust and Identity Contract

Date: 2026-09-30

## Status

Architecture-only checkpoint. No production keys, VPN configuration, server deployment, provider registration, or infrastructure changes are authorized by this document.

## 1. Purpose

Define the trust and identity contract for the Central Protected Registration Gateway (CPRG) before implementation.

CPRG is a logical registration authority with an independently replaceable physical host. Approved hosting forms remain:
- dedicated small server under user control;
- rented European cloud/VPS server.

The hosting location does not define trust. Cryptographic identity and explicit authorization define trust.

## 2. Security domains

The following identities are separate:

1. MediaHub Node Identity — identifies a MediaHub node.
2. CPRG Identity — identifies the currently authoritative registration gateway.
3. Developer Infrastructure Identity — identifies developer servers and compute contributors.
4. Provider Identity — identifies an external provider endpoint/service.
5. GitHub/Secret-Management Identity — identifies the approved credential boundary.

No identity is implicitly trusted merely because the corresponding system participates in MediaHub.

## 3. Trust hierarchy

The architecture requires an offline or separately protected deployment trust root above the CPRG host.

Logical hierarchy:

Trust Root
  -> CPRG authority identity
      -> registration authorization
          -> short-lived request/lease
              -> provider registration operation

Separately:

Trust Root
  -> MediaHub node identity
      -> authenticated registration request

The CPRG host itself is not the ultimate trust root.

The exact root storage mechanism is intentionally left as an implementation decision, but it must not be a casually writable file on the production CPRG host.

## 4. CPRG identity

CPRG must have a unique cryptographic identity containing or binding:

- logical authority identifier;
- public verification key;
- validity interval;
- authority version/epoch;
- revocation status;
- deployment metadata sufficient for audit;
- certificate/attestation chain as selected during implementation.

A physical host replacement must not silently create a new authority.

## 5. MediaHub node identity

Each MediaHub node must have a unique identity.

Node identity must support:

- proof of possession;
- expiration;
- revocation;
- rotation;
- replay-resistant authentication;
- audit correlation without exposing private key material.

Shared static credentials across nodes are prohibited.

Mesh membership is not sufficient authorization for API-key registration.

## 6. Mutual authentication

The future protocol must establish both sides of trust:

MediaHub node
  -> proves node identity to CPRG

CPRG
  -> proves active CPRG authority identity to node

Only after mutual authentication may the registration request proceed to policy evaluation.

Transport encryption alone is not considered sufficient proof of authority.

## 7. Registration authorization

Authentication and authorization are separate.

A valid node identity does not automatically authorize registration.

The policy decision evaluates:

(node_identity,
 request_id,
 operation,
 provider,
 destination,
 lease,
 credential_scope,
 authority_epoch)

A request is authorized only when all applicable constraints pass.

## 8. Request identity

Every registration operation receives a unique request ID.

Request identity must be:

- unique;
- unpredictable where needed;
- bound to the node identity;
- bound to the CPRG authority epoch;
- single-use;
- short-lived;
- auditable;
- impossible to reactivate after closure.

## 9. Nonce and replay protection

Every authentication/registration handshake must contain freshness material.

Required properties:
- challenge/nonce;
- issuance time;
- expiration;
- one-time or replay-cache semantics;
- server-side verification;
- closed-state enforcement.

A captured successful request must not be reusable.

## 10. Lease contract

Registration authorization is always lease-bound.

Lease properties:
- explicit start;
- explicit expiration;
- bounded maximum lifetime;
- server-enforced expiration;
- automatic closure;
- no client-controlled extension;
- no renewal after request closure.

The registration tunnel may exist only while the corresponding lease is active.

## 11. Authority epoch

CPRG uses an authority epoch/version to prevent stale authority state.

Conceptually:

epoch N -> epoch N+1

A node must reject registration authorization that refers to a revoked or stale epoch.

An epoch transition is an administrative security event and must produce evidence.

## 12. Rotation

Rotation must be distinguishable from migration.

### Key rotation
Same logical CPRG authority, new cryptographic key.

### Host migration
Same logical CPRG authority, new physical host.

### Authority replacement
New logical CPRG authority after compromise or permanent loss.

These operations must not be conflated.

## 13. Revocation

Revocation must support at least:

- node revocation;
- CPRG key revocation;
- authority epoch revocation;
- active registration lease termination;
- emergency global registration disable.

Revocation must fail closed.

## 14. Emergency kill switch

The architecture requires an emergency registration kill state.

When activated:

1. new registration requests are denied;
2. pending authentication cannot advance to policy approval;
3. active registration leases are terminated;
4. active registration tunnels are closed;
5. the affected CPRG authority is marked revoked/disabled;
6. audit evidence is emitted;
7. MediaHub data plane remains operational.

The kill switch must not be implemented as a general MediaHub shutdown.

## 15. Migration

A planned migration must have a single authoritative transition.

Required conceptual sequence:

PREPARE_NEW
  -> VERIFY_NEW
  -> ACTIVATE_NEW_EPOCH
  -> DISABLE_OLD
  -> TERMINATE_OLD_LEASES
  -> VERIFY_SINGLE_AUTHORITY
  -> CLOSE_MIGRATION

The exact ordering of lease termination versus authority activation must be resolved during implementation so that no request can be accepted by both authorities.

The acceptance condition is stronger than simple host availability:

**At every point after cutover, at most one CPRG authority can authorize a new registration.**

## 16. Emergency replacement

For suspected CPRG compromise:

DETECT
  -> REVOKE_OLD
  -> KILL_REGISTRATION
  -> ACTIVATE_RECOVERY_AUTHORITY
  -> VERIFY_NEW
  -> ISSUE_NEW_AUTHORITY_EPOCH
  -> RESUME_REGISTRATION

Existing leases from the compromised authority are not silently transferred.

They are terminated and must be recreated as new requests after recovery.

## 17. Provider boundary

CPRG does not become the permanent owner of provider credentials merely because it performs registration.

Provider interaction must be:
- operation-scoped;
- destination-scoped;
- lease-scoped;
- auditable;
- denied outside the admitted registration operation.

No arbitrary provider API/model enumeration is part of CPRG authority.

## 18. Hosting-provider boundary

If CPRG is hosted on a European VPS/cloud:

- the cloud provider is an infrastructure trust boundary;
- provider control-plane credentials must be separate from developer infrastructure credentials;
- CPRG must have no route to Media Mesh or developer Mesh;
- CPRG must have no general inbound administration from arbitrary networks;
- host compromise must not become lateral movement;
- backup material must be minimized;
- replacement must be possible without redesigning MediaHub.

The European location is not itself a trust signal.

## 19. Audit contract

Audit records must establish:

- request identity;
- node identity or pseudonymous node reference;
- CPRG authority epoch;
- operation class;
- provider identity;
- destination policy result;
- lease interval;
- state transitions;
- final result;
- revocation/kill events;
- migration events.

Audit must never contain:
- API-key values;
- private keys;
- raw provider payloads unless a future explicit policy permits a sanitized derivative;
- personal media data;
- arbitrary user content.

## 20. Evidence contract

Every production registration implementation must be able to produce evidence for:

1. mutual authentication;
2. policy decision;
3. lease issuance;
4. destination restriction;
5. registration result;
6. closure;
7. revocation where applicable;
8. absence of secret leakage;
9. single-authority state;
10. recovery/migration state.

Evidence must be independently verifiable without exposing secrets.

## 21. Failure semantics

The following failures must converge to safe states:

- authentication failure -> DENIED;
- authorization failure -> DENIED/CLOSED;
- nonce/replay failure -> DENIED;
- lease expiration -> CLOSED;
- tunnel error -> CLOSED;
- provider error -> CLOSED or RETRY only inside a bounded active lease;
- audit failure -> registration policy decision must be explicitly defined; silent success is prohibited;
- CPRG outage -> registration unavailable, MediaHub data plane continues;
- authority compromise -> REVOKED/KILL;
- migration ambiguity -> registration denied until single authority is established.

## 22. Explicit separation from developer compute

CPRG identity cannot grant:
- developer cluster membership;
- compute contribution rights;
- access to developer source code;
- access to user data;
- access to MediaHub storage;
- Astra worker control.

Conversely, developer infrastructure identity cannot authorize API-key registration through CPRG unless a separate explicit policy grants that operation.

## 23. Open architectural decisions

Before implementation, the following must be resolved:

1. exact cryptographic identity format;
2. root-of-trust storage;
3. CPRG certificate/attestation mechanism;
4. node identity provisioning and bootstrap;
5. rotation procedure;
6. revocation distribution;
7. replay-cache persistence model;
8. authority epoch storage;
9. emergency kill authorization;
10. migration transaction protocol;
11. audit storage and integrity model;
12. recovery authority bootstrap;
13. exact hosting isolation profile for European VPS;
14. monitoring trust boundary.

## 24. Qualification gates

No implementation is considered production-ready until independent tests demonstrate:

- mutual authentication;
- invalid identity rejection;
- stale identity rejection;
- replay rejection;
- revoked node rejection;
- revoked CPRG rejection;
- epoch mismatch rejection;
- lease expiration;
- forced tunnel teardown;
- single-authority invariant;
- migration without split-brain;
- emergency kill;
- emergency recovery;
- no credential leakage;
- no data-plane routing through CPRG;
- no developer-plane routing through CPRG;
- independent evidence verification.

## Decision

The architecture now defines CPRG as a cryptographically identified, logically centralized, physically replaceable registration authority.

European cloud/VPS hosting is an approved deployment option but is not being implemented or selected now.

The next implementation gate is the completion and review of the open trust, bootstrap, rotation, revocation, migration, and recovery decisions.
