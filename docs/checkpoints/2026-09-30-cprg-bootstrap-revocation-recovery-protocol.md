# CPRG Bootstrap, Revocation and Recovery Protocol

Date: 2026-09-30

## Status

Architecture-only checkpoint. No production keys, VPN deployment, server provisioning, provider registration, or trust-root generation is authorized.

## 1. Objective

Define how MediaHub nodes obtain, use, rotate, and lose registration trust, and how the system recovers after CPRG loss or compromise.

Core invariant: CPRG failure may disable API-key registration, but must not disable the MediaHub data plane, local compute, or the developer compute fabric.

## 2. Actors

- Trust Root — separately protected authority for issuing/revoking identities.
- CPRG Authority — current logical registration authority.
- MediaHub Node — client requesting API-key registration.
- Recovery Authority — emergency authority activated only under defined recovery conditions.
- Audit Verifier — independent component/process that verifies evidence integrity.
- Provider — external API-key registration endpoint.

The Trust Root, CPRG Authority, and Recovery Authority are logically distinct roles even if a future implementation chooses carefully controlled co-location.

## 3. Identity lifecycle

UNPROVISIONED -> BOOTSTRAP_PENDING -> ISSUED -> ACTIVE -> ROTATION_PENDING -> ROTATED -> REVOKED

REVOKED is terminal for that identity.

## 4. Bootstrap principle

Bootstrap is the highest-risk lifecycle event because the node does not yet possess an established registration trust relationship.

Therefore:
- bootstrap credentials must be single-use or tightly bounded;
- bootstrap must bind the resulting identity to one specific node;
- bootstrap must have explicit expiration;
- bootstrap must be auditable;
- bootstrap must not grant API-key registration authority by itself;
- bootstrap must not grant Media Mesh, developer compute, or user-data authority beyond the separate node onboarding contract.

The bootstrap mechanism must not rely solely on knowledge of a static shared secret.

## 5. Bootstrap flow

NODE_GENERATED -> BOOTSTRAP_REQUEST -> BOOTSTRAP_AUTHENTICATED -> NODE_IDENTITY_ISSUED -> CPRG_TRUST_ESTABLISHED -> BOOTSTRAP_CLOSED -> REGISTRATION_ELIGIBLE

REGISTRATION_ELIGIBLE is an eligibility state, not authorization to perform an arbitrary registration.

## 6. Bootstrap trust options

Option A — short-lived out-of-band enrollment secret:
- single-use;
- node-bound;
- expiration;
- no shared permanent secret;
- immediate invalidation after enrollment.

Option B — device-generated key proof:
- node generates key pair locally;
- node proves possession during enrollment;
- private key never leaves the node.

Option C — hardware-backed identity where platform capabilities justify it.

No option is selected for implementation by this checkpoint.

## 7. Node private-key boundary

The node private identity key must remain on the node.

It must not be:
- sent to CPRG;
- stored in GitHub;
- placed in repository files;
- copied into audit;
- included in registration payloads;
- exposed through ordinary MediaHub metadata.

The node proves possession cryptographically.

## 8. CPRG identity bootstrap

Nodes must also verify the CPRG identity.

A new node must receive or securely discover the trust anchor required to validate the active CPRG authority.

The design must avoid an unauthenticated key-download-then-trust flow.

## 9. Revocation classes

At minimum:
1. Node identity revoked.
2. CPRG signing/authority key revoked.
3. CPRG authority epoch revoked.
4. Registration request revoked.
5. Active registration lease terminated.
6. Global registration kill switch active.
7. Recovery/migration mode active.

Each class has different blast radius.

## 10. Revocation semantics

### Node revocation
A revoked node cannot authenticate for registration, create a new registration request, or extend an existing registration lease. Normal MediaHub operation remains independent.

### CPRG authority revocation
New registrations are denied, active registration leases are terminated, protected registration tunnels are closed, and a new authority may be activated only through recovery/migration policy.

### Request revocation
A request becomes permanently closed.

### Lease termination
The lease ends immediately and the tunnel must be closed server-side.

## 11. Revocation distribution

Because ordinary MediaHub nodes do not maintain a permanent CPRG VPN connection, revocation state must be obtainable through the normal control path.

Future implementation may use signed revocation statements, short-lived authority metadata, versioned revocation state, pull-on-demand verification, and bounded local cache.

The design must not require a permanent full-tunnel connection.

## 12. Stale-state defense

A node with stale revocation or authority metadata must not silently continue registration.

The protocol must define:
- maximum acceptable metadata age;
- authority epoch;
- signature validation;
- expiration;
- behavior when revocation state cannot be refreshed.

For security-sensitive registration, uncertainty fails closed.

## 13. Recovery levels

### R0 — transient outage
CPRG unavailable with no evidence of compromise.

Result:
- registration unavailable;
- MediaHub continues;
- retry later.

### R1 — host loss
CPRG host permanently unavailable.

Result:
- activate replacement authority according to migration policy;
- terminate old leases;
- verify new authority;
- resume registration.

### R2 — suspected compromise
Evidence suggests unauthorized access.

Result:
- emergency registration kill;
- revoke CPRG authority;
- terminate active leases;
- activate recovery authority;
- issue new epoch;
- require fresh registration requests.

### R3 — trust-root compromise
The root authority itself may be compromised.

Result:
- all dependent CPRG authority trust is considered suspect;
- registration remains disabled;
- new trust root/recovery procedure is required;
- no automatic trust migration is permitted.

R3 is a manual, high-assurance recovery event.

## 14. Recovery authority

Recovery Authority is not a second ordinary CPRG.

It exists to perform controlled recovery when the active authority is unavailable or revoked.

Recovery Authority must have:
- separate credentials;
- separate authorization;
- independent audit;
- explicit activation condition;
- bounded lifetime;
- revocation capability.

It must not become a permanent parallel registration authority.

## 15. Recovery state machine

NORMAL -> REGISTRATION_KILLED -> OLD_AUTHORITY_REVOKED -> RECOVERY_AUTHORITY_ACTIVE -> NEW_AUTHORITY_VERIFIED -> NEW_EPOCH_ACTIVE -> REGISTRATION_RESUMED -> RECOVERY_AUTHORITY_CLOSED

No state permits two active authorities.

## 16. Active lease handling during recovery

- transient outage: leases may remain valid only if the authority remains trusted and server-side state is intact;
- host loss: leases are terminated unless a future implementation proves safe state continuity;
- suspected compromise: all active leases are terminated;
- trust-root compromise: all registration state is treated as untrusted.

New registration always requires a new request ID.

## 17. Bootstrap after recovery

A recovered CPRG does not automatically trust every node that previously registered.

The node must validate:
- new authority identity;
- new authority epoch;
- revocation state;
- registration policy.

Existing node identity may remain valid if recovery policy explicitly preserves it.

A compromised node identity is revoked independently.

## 18. Recovery and MediaHub independence

Recovery operations must never:
- change Media Mesh routing;
- stop local media services;
- stop local compute;
- stop compute contribution;
- modify user storage;
- provide CPRG access to developer compute.

Only the Protected Registration Plane changes state.

## 19. Audit integrity

Every bootstrap, revocation, migration, and recovery event must create an auditable security event.

Audit record includes:
- event ID;
- authority epoch;
- actor class;
- operation class;
- timestamp;
- state transition;
- result;
- reason category.

Audit excludes:
- private keys;
- API-key values;
- raw provider payloads;
- personal user data.

Audit integrity should be externally verifiable.

## 20. Emergency kill authority

The architecture requires narrowly held emergency authorization capable of disabling registration.

It must not be equivalent to:
- MediaHub administrator access;
- developer cluster administrator access;
- user data access.

Emergency kill is a registration-plane control.

## 21. Recovery anti-patterns

Prohibited shortcuts:
1. Reusing a static shared bootstrap secret indefinitely.
2. Trusting a CPRG key merely because it was downloaded over an unauthenticated channel.
3. Automatically accepting a replacement CPRG because the old host is unreachable.
4. Running two active CPRG authorities without an explicit single-authority protocol.
5. Silently transferring active leases across a suspected compromise.
6. Storing node private keys on CPRG.
7. Using CPRG as a general VPN.
8. Coupling CPRG recovery to MediaHub shutdown.
9. Treating European hosting location as proof of trust.
10. Storing all provider credentials permanently on CPRG.

## 22. Qualification gates

### Bootstrap
- single-use enrollment;
- node-bound identity;
- private-key non-exportability;
- CPRG authenticity verification;
- bootstrap expiration.

### Revocation
- node revocation;
- CPRG revocation;
- epoch revocation;
- request revocation;
- lease termination;
- global registration kill.

### Recovery
- transient outage;
- host replacement;
- suspected compromise;
- trust-root compromise procedure;
- no split-brain;
- no stale lease reuse;
- independent evidence verification.

### Independence
- MediaHub data plane continues;
- local compute continues;
- developer compute continues;
- no CPRG route to protected networks.

## 23. Remaining architecture decisions

Before implementation, resolve:
1. exact bootstrap channel;
2. exact node key algorithm/storage;
3. exact CPRG trust-anchor format;
4. revocation-state distribution;
5. metadata freshness limits;
6. recovery authority custody;
7. emergency kill custody;
8. audit integrity mechanism;
9. recovery approval quorum/process;
10. host migration transaction;
11. trust-root compromise recovery;
12. backup and restore semantics for authority state.

## Decision

Bootstrap, revocation, and recovery are separate security lifecycles.

The system must prefer explicit denial under uncertainty over silent trust continuity.

The architecture is ready for a subsequent formal protocol/state-machine review, but not yet for implementation.
