# CPRG v1 Threat Model and Hardening Plan

Date: 2026-09-30

## Scope

This document threat-models the Central Protected Registration Gateway (CPRG), a small dedicated server whose protected VPN path is used exclusively for API-key registration. It does not authorize production deployment.

## Security objective

CPRG must provide a narrowly scoped registration capability without becoming:
- a general VPN gateway;
- an Internet proxy/NAT/transit node;
- a MediaHub data gateway;
- a developer compute node;
- a credential vault outside the approved secret-management boundary.

The strongest invariant is:

**Registration capability does not imply data-plane access, compute access, or developer-personnel access.**

## Assets

1. API registration authorization.
2. Provider registration endpoint/session.
3. Node identity and authorization state.
4. Short-lived registration lease.
5. Registration audit evidence.
6. CPRG host integrity.
7. GitHub secret-management boundary.
8. Provider-specific registration metadata.
9. Network policy and routing state.

## Trust boundaries

### B1 — GitHub / secret-management boundary

Provider credentials originate from the approved secret-management boundary. CPRG must never become a second uncontrolled long-term secret store.

### B2 — MediaHub node to CPRG

The node is authenticated before registration. Mesh membership alone is insufficient.

### B3 — VPN registration tunnel

The tunnel is request-scoped and short-lived. It is not a reusable client VPN.

### B4 — CPRG to provider registration endpoint

Only the exact registration operation allowed by policy may traverse this path.

### B5 — CPRG host

The host is a high-value control-plane component and must be hardened independently from the developer cluster.

## Threats and required mitigations

### T1 — Tunnel becomes a general-purpose VPN

Risk:
A client uses the tunnel to reach arbitrary Internet destinations or internal networks.

Required controls:
- no IP forwarding except an explicitly bounded registration path;
- firewall allowlist for registration destinations;
- no default route pushed to clients;
- no split-tunnel escape that permits arbitrary destinations;
- egress ACL enforced on CPRG, not only by client configuration;
- reject non-registration traffic;
- short lease and automatic teardown.

Acceptance evidence:
A negative test demonstrates that an admitted client cannot reach an unrelated Internet address, MediaHub subnet, developer subnet, or storage endpoint through CPRG.

### T2 — Client identity theft

Risk:
An attacker obtains or impersonates a MediaHub node identity.

Required controls:
- per-node cryptographic identity;
- challenge/nonce;
- proof of possession;
- expiration;
- revocation;
- replay protection;
- no shared static client credential across nodes.

Acceptance evidence:
A copied/invalid identity is denied and an expired identity cannot open a registration session.

### T3 — Credential leakage

Risk:
API-key values appear in logs, artifacts, process arguments, crash dumps, repository files, or node metadata.

Required controls:
- credentials only from approved secret-management boundary;
- never pass secrets in command-line arguments;
- redact structured and unstructured logs;
- prohibit secret persistence on MediaHub nodes;
- no credential values in evidence;
- bounded process environment handling;
- cleanup after registration.

Acceptance evidence:
Automated secret-scanning and synthetic canary tests show no credential material in audit/evidence outputs.

### T4 — Registration request replay

Risk:
A previously authorized request is replayed.

Required controls:
- unique request ID;
- nonce;
- issuance timestamp;
- short expiration;
- one-time registration token;
- server-side replay cache or equivalent;
- request state transition that closes the operation.

Acceptance evidence:
The same request cannot be successfully registered twice when the policy requires one-time use.

### T5 — Lease extension or stale tunnel

Risk:
A client keeps access after registration completes.

Required controls:
- explicit lease expiration;
- server-side timeout;
- teardown independent of client cooperation;
- registration completion immediately closes the path;
- watchdog detects stale sessions.

Acceptance evidence:
Post-completion connectivity to an allowed registration destination is denied.

### T6 — Provider endpoint abuse

Risk:
The protected path reaches a provider endpoint outside the exact registration action.

Required controls:
- destination allowlist;
- port/protocol allowlist;
- operation-level policy;
- payload size and rate limits;
- deny-by-default egress;
- provider-specific policy compliance.

Acceptance evidence:
An unapproved destination and an unapproved operation are both denied.

### T7 — CPRG compromise becomes lateral movement

Risk:
Compromising CPRG provides a bridge into MediaHub or developer networks.

Required controls:
- no trust relationship that permits arbitrary inbound access;
- no route to Media Mesh;
- no route to developer compute network;
- no shared administrative credentials;
- dedicated host;
- host firewall;
- minimal packages/services;
- tightly controlled configuration;
- separate monitoring.

Acceptance evidence:
A compromised-service simulation cannot reach protected internal subnets.

### T8 — Registration endpoint is abused as an oracle

Risk:
Attackers use CPRG to test provider credentials, enumerate provider behavior, or generate excessive requests.

Required controls:
- authentication before provider interaction;
- strict request rate limits;
- per-node quotas;
- bounded retries;
- no arbitrary provider model/API enumeration;
- sanitized provider errors.

Acceptance evidence:
Unauthenticated and over-quota requests never reach the provider.

### T9 — Audit log becomes a privacy leak

Risk:
Audit records expose API keys, user identifiers, personal paths, provider payloads, or sensitive metadata.

Required controls:
- structured audit schema;
- allowlisted fields only;
- no raw request/response bodies;
- no secret values;
- pseudonymous node IDs where practical;
- retention policy;
- integrity protection.

Acceptance evidence:
Synthetic sensitive values inserted into requests are absent from audit output.

### T10 — DNS or routing manipulation

Risk:
A compromised DNS path redirects registration traffic.

Required controls:
- explicit destination policy;
- authenticated TLS verification;
- controlled DNS policy;
- fail closed on certificate/hostname mismatch;
- avoid manual IP pinning for dynamic provider endpoints.

Acceptance evidence:
Synthetic DNS redirection fails registration.

### T11 — Resource exhaustion

Risk:
CPRG becomes unavailable due to connection, CPU, memory, log, or retry exhaustion.

Required controls:
- bounded concurrent sessions;
- request size limits;
- connection timeouts;
- rate limits;
- log rotation;
- circuit breaker;
- bounded retries;
- health monitoring.

Acceptance evidence:
A load test reaches configured limits while registration remains fail-closed and the host remains recoverable.

### T12 — Host compromise through unnecessary services

Risk:
An unnecessary package or service becomes an attack path.

Required controls:
- minimal OS installation;
- only VPN, registration service, firewall, time synchronization, and required monitoring;
- no developer tools;
- no compiler/build environment;
- no arbitrary containers unless separately justified;
- no SSH from arbitrary networks;
- configuration baseline and drift detection.

Acceptance evidence:
A service/package inventory matches the approved baseline.

### T13 — Administrative credential compromise

Risk:
CPRG administrator credentials provide broad host access.

Required controls:
- separate administrative identity;
- strong authentication;
- no shared accounts;
- least-privilege service account;
- privileged actions audited;
- emergency access procedure.

Acceptance evidence:
Registration-service credentials cannot administer the host.

### T14 — Backup becomes a secret/data leak

Risk:
Backups contain credentials, VPN private keys, or sensitive registration material.

Required controls:
- CPRG backup allowlist;
- no raw transient registration payloads;
- encrypted backup;
- access-controlled backup repository;
- tested restore;
- explicit retention.

Acceptance evidence:
Backup manifest contains only approved state.

### T15 — Failure of CPRG affects MediaHub operation

Risk:
A central control-plane failure blocks normal MediaHub data and compute operation.

Required controls:
- no CPRG dependency in normal data-plane routing;
- registration-only dependency;
- local operation continues when CPRG is unavailable;
- registration requests fail closed.

Acceptance evidence:
CPRG shutdown test shows Media Mesh and local compute continue while registration is unavailable.

## Required state machine

Registration state must be explicit:

REQUESTED
-> AUTHENTICATED
-> POLICY_APPROVED
-> LEASE_ACTIVE
-> TUNNEL_ACTIVE
-> REGISTRATION_IN_PROGRESS
-> REGISTRATION_VERIFIED
-> CLOSED

Any failure after lease creation must converge to CLOSED.

No state may transition from CLOSED back to an active registration state using the same request identity.

## Required authorization tuple

Every registration attempt should be evaluated as:

(node_identity, request_id, operation, provider, destination, lease, credential_scope)

A valid node alone is insufficient.

## Routing invariants

The CPRG VPN must never become:
- default route;
- full tunnel;
- Media Mesh transport;
- developer Mesh transport;
- storage path;
- compute path;
- general proxy;
- NAT gateway.

The server-side firewall must enforce these invariants independently of client configuration.

## Operational separation

CPRG should not host:
- Astra worker;
- CI runner;
- developer workloads;
- artifact builds;
- model serving;
- user storage;
- MediaHub media services.

This prevents unrelated compromise domains from accumulating on the registration host.

## Qualification sequence

1. Static configuration review.
2. Identity/authentication negative tests.
3. Routing isolation tests.
4. Destination allowlist tests.
5. Replay tests.
6. Lease expiry tests.
7. Credential leakage tests.
8. Audit privacy tests.
9. Resource exhaustion tests.
10. Host service/package baseline.
11. CPRG outage test proving MediaHub data-plane continuity.
12. Provider registration canary.
13. Recovery/restart test.
14. Evidence bundle and independent verification.

## Explicit non-goals

This checkpoint does not authorize:
- production VPN deployment;
- provider-specific regional-access workarounds;
- storage of permanent provider credentials on CPRG;
- general remote access;
- developer cluster access through CPRG.

## Decision

The dedicated small-server model is accepted as the preferred CPRG architecture, subject to the qualification gates above. The VPN remains a narrowly scoped registration transport, not a general connectivity mechanism.
