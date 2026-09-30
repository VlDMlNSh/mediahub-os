# Central Protected Registration Gateway (CPRG)

Date: 2026-09-30

## Purpose

CPRG is the centralized control-plane component for protected API-key registration.

The architectural goal is to keep VPN functionality out of ordinary MediaHub nodes while preserving privacy and a narrow, auditable registration path.

## Canonical hosting decision

CPRG is a **logically centralized, physically independent registration server**.

It is intentionally separated from:
- the MediaHub user/data plane;
- the MediaHub developer cluster;
- Astra workers;
- CI runners;
- developer compute;
- user storage.

CPRG may be hosted on either:

1. a small dedicated server under the user's control; or
2. a small **rented cloud/VPS server in Europe**.

Both are first-class architectural deployment options.

The architecture does **not** require CPRG to be located on the same physical server as the user's central MediaHub server.

For the current design phase, **no hosting provider, country, VPS plan, VPN software, or server configuration is selected or deployed**. Hosting selection is an implementation/qualification decision that follows the architecture.

A European cloud server is therefore an approved architectural option, not an implementation commitment.

## Canonical rules

1. There is one logical CPRG registration authority for the deployment domain.
2. CPRG is hosted on a dedicated small server or isolated cloud/VPS instance.
3. Ordinary external MediaHub nodes are VPN-free and must not require VPN software, VPN credentials, or VPN routing configuration.
4. External MediaHub nodes reach CPRG through their normal direct network path.
5. **VPN is used exclusively for API-key registration.** It must not carry media, storage, compute, synchronization, ordinary Internet, or general management traffic.
6. API-key registration is a separate **request-scoped operation** with authentication, policy, lease, and audit.
7. A registration request receives a unique request/job identity and an explicitly bounded scope.
8. The protected registration path is created only for the lifetime of the authorized registration operation and is automatically closed on completion or lease expiry.
9. CPRG must not expose the VPN-backed registration path as a reusable general-purpose tunnel to client nodes.
10. Media/data-plane traffic must never be routed through CPRG.
11. Media, storage, compute, synchronization, and ordinary Internet traffic remain on their normal direct paths.
12. CPRG is not a general Internet gateway, NAT gateway, proxy, or transit router for MediaHub nodes.
13. Provider credentials remain in the approved secret-management boundary (GitHub Secrets where applicable); credential values must not be copied into MediaHub node metadata or committed to the repository.
14. Registration operations must be least-privilege and limited to the exact provider/key-registration action admitted by policy.
15. Each registration operation must produce an audit record containing at least request identity, source node, operation class, policy decision, lease, timestamps, result state, and failure information where applicable.
16. Failure of CPRG must not interrupt ordinary MediaHub data-plane connectivity.
17. Failure or unavailability of the protected registration path must fail closed for the registration operation.
18. Mesh connectivity and the protected registration path are separate security domains.
19. Any provider-specific network access must comply with the provider's applicable terms and access policies.
20. **Registration capability does not imply MediaHub data access, developer compute access, or developer-personnel access.**
21. **The server-side firewall must enforce registration-only egress independently of client routing configuration.**
22. CPRG must not host Astra, CI runners, developer workloads, user storage, or MediaHub media services.
23. CPRG must have no dependency on the developer compute cluster for registration availability.
24. Loss, compromise, replacement, or migration of the CPRG host must not require changes to the MediaHub data plane.
25. Hosting migration must preserve the logical CPRG contract: identity, authorization, registration-only routing, audit, lease, and fail-closed behavior.

## Hosting model

### Option A — dedicated small server

A physically or virtually dedicated small server can host CPRG under the user's administrative control.

Advantages:
- maximum control over host configuration;
- simple isolation model;
- predictable resource usage;
- independent lifecycle from the developer cluster.

### Option B — European cloud/VPS

A small rented cloud/VPS server in Europe can host CPRG as an independent registration appliance.

Advantages:
- stable external reachability;
- geographic diversity from the user's local infrastructure;
- simple replacement/scaling of the registration host;
- no need to expose a home/central server directly for registration traffic.

This option does **not** make the European server part of the developer compute cluster. Its role remains exclusively CPRG.

The European location is an infrastructure choice. It must not be treated as a mechanism for bypassing provider restrictions. Provider-specific access remains subject to applicable provider policies and terms.

## Hosting invariants

Regardless of physical hosting:

- one logical CPRG authority;
- dedicated security boundary;
- no user data;
- no developer workloads;
- no general VPN;
- no full-tunnel routing;
- no Media Mesh transit;
- no developer Mesh transit;
- no storage gateway;
- no general proxy/NAT;
- registration-only egress;
- short-lived registration leases;
- server-side enforcement;
- auditable operations;
- fail-closed registration;
- normal MediaHub operation remains independent.

## Network separation

### DIRECT

- Media Mesh / P2P
- media and storage traffic
- compute-job traffic
- synchronization where explicitly permitted
- ordinary Internet traffic

### CPRG

- authenticated API-key registration requests
- the protected registration transport required for that operation
- registration-specific audit/control messages

**No other traffic is permitted through the VPN registration path.**

The default route for MediaHub nodes remains direct. CPRG must not become a default route or full-tunnel endpoint for external MediaHub nodes.

## Registration lifecycle

REQUEST
  -> AUTHENTICATE
  -> POLICY CHECK
  -> ISSUE SHORT LEASE
  -> OPEN PROTECTED REGISTRATION PATH
  -> REGISTER API KEY
  -> VERIFY RESULT
  -> RECORD RESULT / AUDIT
  -> CLOSE PATH
  -> EXPIRE LEASE

The protected path exists only for the registration request. It is not persistent connectivity.

Any failure after lease activation must converge to a closed state. A closed request ID cannot be reused to reopen a registration session.

## Security model

The CPRG host is the sole trusted registration boundary. Client nodes receive no persistent VPN capability merely because they are members of the MediaHub Mesh.

The registration protocol must enforce:

- authenticated node identity;
- proof of possession;
- least privilege;
- explicit operation scope;
- destination allowlisting;
- bounded request payloads;
- short-lived authorization/lease;
- replay protection;
- rate and concurrency limits;
- auditability without secret/personal-data leakage;
- automatic closure;
- isolation from the Media Data Plane;
- fail-closed behavior for registration failures.

## Primary threat classes

The CPRG threat model explicitly covers:

- general-purpose VPN escape;
- stolen/forged node identity;
- credential leakage;
- replay;
- stale/extended leases;
- provider endpoint abuse;
- CPRG-to-MediaHub/developer lateral movement;
- registration abuse and enumeration;
- audit-log privacy leakage;
- DNS/routing manipulation;
- resource exhaustion;
- unnecessary host services;
- administrative credential compromise;
- backup leakage;
- CPRG outage and dependency failure;
- cloud-host compromise or provider-side isolation failure;
- hosting migration/configuration drift;
- geographic hosting becoming an unintended policy bypass mechanism.

Detailed mitigations, acceptance evidence, and the qualification sequence are maintained in:
docs/checkpoints/2026-09-30-cprg-threat-model-and-hardening.md

## Qualification gates before production

1. Static configuration review.
2. Hosting/isolation review.
3. Identity/authentication negative tests.
4. Routing isolation tests.
5. Destination allowlist tests.
6. Replay tests.
7. Lease expiry and forced teardown tests.
8. Credential leakage tests.
9. Audit privacy tests.
10. Resource exhaustion tests.
11. Host service/package baseline.
12. CPRG outage test proving MediaHub data-plane continuity.
13. Provider registration canary.
14. Recovery/restart test.
15. Hosting migration/replacement test.
16. Independent evidence verification.

No production deployment is authorized until these gates pass.

## Architectural consequence

This creates four distinct planes:

1. **Media Data Plane** — direct local/mesh traffic.
2. **Federation/Control Plane** — admission, job coordination, cloud escalation, and ordinary management.
3. **Protected Registration Plane** — centralized CPRG path used exclusively for API-key registration.
4. **Compute Contribution Plane** — bounded compute contribution from MediaHub nodes to the developer compute fabric; it never grants access to user data or CPRG.

CPRG is a separate security domain from all four operational planes.

GOLD #176 remains untouched.
Immutable R4 baseline remains untouched.
