# Central Protected Registration Gateway (CPRG)

Date: 2026-09-30

## Purpose

CPRG is the centralized control-plane component for protected API-key registration and related credential-management operations.

The architectural goal is to keep VPN functionality out of ordinary MediaHub nodes while preserving privacy and a narrow, auditable registration path.

## Canonical rules

1. Only the designated central CPRG server may provide the protected VPN-backed registration path.
2. Ordinary external MediaHub nodes are VPN-free and must not require VPN software or credentials.
3. External MediaHub nodes reach CPRG through the server Mesh using their normal direct network path.
4. The protected path is scoped exclusively to authorized registration/credential-management operations.
5. Media/data-plane traffic must never be routed through CPRG.
6. Media, storage, compute, synchronization, and ordinary Internet traffic remain on their normal direct paths.
7. CPRG is not a general Internet gateway, NAT gateway, or transit router for MediaHub nodes.
8. Registration requests are request-scoped, authenticated, policy-checked, bounded, and auditable.
9. Provider credentials remain in the approved secret-management boundary (GitHub Secrets where applicable); credential values must not be copied into MediaHub node metadata or committed to the repository.
10. CPRG must not expose the protected registration channel as a reusable general-purpose tunnel to client nodes.
11. Each registration operation must have a unique job/request identity and an audit record containing at least source node, operation class, policy decision, timestamps, result state, and failure information where applicable.
12. Registration access terminates automatically when the authorized operation completes or its lease expires.
13. Failure of CPRG must not interrupt ordinary MediaHub data-plane connectivity.
14. Failure or unavailability of the protected path must fail closed for protected registration operations.
15. Mesh connectivity and the protected registration path are separate security domains.
16. Any provider-specific network access must comply with the provider's applicable terms and access policies; this architecture does not authorize circumvention of provider restrictions.

## Network separation

DIRECT:
- Media Mesh / P2P
- media and storage traffic
- compute-job traffic
- ordinary Internet traffic

CPRG:
- authenticated registration requests
- credential-management control traffic
- protected management operations explicitly admitted by policy

The default route for MediaHub nodes remains direct. CPRG must not become a default route or full-tunnel endpoint for external MediaHub nodes.

## Security model

The central server is the sole trusted registration boundary. Client nodes receive no persistent VPN capability merely because they are members of the MediaHub Mesh.

The registration protocol must enforce:
- mutual/authenticated node identity;
- least privilege;
- explicit operation scope;
- bounded request payloads;
- short-lived authorization/lease;
- replay protection where applicable;
- auditability;
- automatic closure;
- isolation from the Media Data Plane.

## Architectural consequence

This creates three distinct planes:

1. Media Data Plane — direct local/mesh traffic.
2. Federation/Control Plane — admission, job coordination, cloud escalation, and management.
3. Protected Registration Plane — centralized CPRG path for authorized registration operations.

No production deployment is authorized by this checkpoint.

GOLD #176 remains untouched.
Immutable R4 baseline remains untouched.
