# Central Protected Registration Gateway (CPRG)

Date: 2026-09-30

## Purpose

CPRG is the centralized control-plane component for protected API-key registration.

The architectural goal is to keep VPN functionality out of ordinary MediaHub nodes while preserving privacy and a narrow, auditable registration path.

## Canonical rules

1. Only the designated central CPRG server may provide the protected VPN-backed registration path.
2. Ordinary external MediaHub nodes are VPN-free and must not require VPN software, VPN credentials, or VPN routing configuration.
3. External MediaHub nodes reach CPRG through the server Mesh using their normal direct network path.
4. **VPN is used exclusively for API-key registration.** It must not carry media, storage, compute, synchronization, ordinary Internet, or general management traffic.
5. API-key registration is a separate **request-scoped operation** with authentication, policy, lease, and audit.
6. A registration request receives a unique request/job identity and an explicitly bounded scope.
7. The protected registration path is created only for the lifetime of the authorized registration operation and is automatically closed on completion or lease expiry.
8. CPRG must not expose the VPN-backed registration path as a reusable general-purpose tunnel to client nodes.
9. Media/data-plane traffic must never be routed through CPRG.
10. Media, storage, compute, synchronization, and ordinary Internet traffic remain on their normal direct paths.
11. CPRG is not a general Internet gateway, NAT gateway, proxy, or transit router for MediaHub nodes.
12. Provider credentials remain in the approved secret-management boundary (GitHub Secrets where applicable); credential values must not be copied into MediaHub node metadata or committed to the repository.
13. Registration operations must be least-privilege and limited to the exact provider/key-registration action admitted by policy.
14. Each registration operation must produce an audit record containing at least request identity, source node, operation class, policy decision, lease, timestamps, result state, and failure information where applicable.
15. Failure of CPRG must not interrupt ordinary MediaHub data-plane connectivity.
16. Failure or unavailability of the protected registration path must fail closed for the registration operation.
17. Mesh connectivity and the protected registration path are separate security domains.
18. Any provider-specific network access must comply with the provider's applicable terms and access policies.
19. **Registration capability does not imply MediaHub data access, developer compute access, or developer-personnel access.**
20. **The server-side firewall must enforce registration-only egress independently of client routing configuration.**
21. CPRG must not host Astra, CI runners, developer workloads, user storage, or MediaHub media services.

## Future hosting option

The CPRG design is intentionally location-independent.

The initial implementation may operate on the currently available central server. A dedicated European-hosted server may be considered later as an infrastructure option if operational, privacy, latency, availability, or provider-access requirements justify it.

A future European server is **not an architectural prerequisite**. The system must first be designed and qualified so that a dedicated external server is unnecessary unless later evidence demonstrates a concrete need.

Changing CPRG hosting must not require adding VPN functionality to ordinary MediaHub nodes.

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

The central server is the sole trusted registration boundary. Client nodes receive no persistent VPN capability merely because they are members of the MediaHub Mesh.

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
- CPRG outage and dependency failure.

Detailed mitigations, acceptance evidence, and the qualification sequence are maintained in:
docs/checkpoints/2026-09-30-cprg-threat-model-and-hardening.md

## Qualification gates before production

1. Static configuration review.
2. Identity/authentication negative tests.
3. Routing isolation tests.
4. Destination allowlist tests.
5. Replay tests.
6. Lease expiry and forced teardown tests.
7. Credential leakage tests.
8. Audit privacy tests.
9. Resource exhaustion tests.
10. Host service/package baseline.
11. CPRG outage test proving MediaHub data-plane continuity.
12. Provider registration canary.
13. Recovery/restart test.
14. Independent evidence verification.

No production deployment is authorized until these gates pass.

## Architectural consequence

This creates four distinct planes:

1. **Media Data Plane** — direct local/mesh traffic.
2. **Federation/Control Plane** — admission, job coordination, cloud escalation, and ordinary management.
3. **Protected Registration Plane** — centralized CPRG path used exclusively for API-key registration.
4. **Compute Contribution Plane** — bounded compute contribution from MediaHub nodes to the developer compute fabric; it never grants access to user data or CPRG.

GOLD #176 remains untouched.
Immutable R4 baseline remains untouched.
