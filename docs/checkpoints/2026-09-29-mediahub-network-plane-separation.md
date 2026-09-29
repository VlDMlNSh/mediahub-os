# MediaHub Network Architecture Checkpoint — 2026-09-29

## Decision

Separate the future networking architecture into distinct logical planes.

### 1. Media Mesh / Media Data Plane

Purpose: the MediaHub product/runtime infrastructure itself.

Primary requirements:
- high throughput and low latency;
- direct peer-to-peer paths where possible;
- large data transfer and synchronization;
- distributed storage;
- distributed CPU/GPU workloads;
- scalable node-to-node communication.

This is the high-speed mesh of the MediaHub infrastructure.

### 2. Development Mesh / Development Plane

Purpose: development, orchestration, CI/CD, remote execution, and management of MediaHub.

Primary requirements:
- VPN bridge / secure overlay;
- distributed mesh connectivity;
- node discovery and ACL/security;
- remote workers;
- GitHub/Astra/Codex integration;
- build/test execution;
- artifact exchange;
- resilience and reconnect.

High throughput is useful but is not the defining requirement.

### 3. Control Plane

GitHub remains the canonical control and secret-management plane.

Responsibilities:
- source control;
- GitHub Actions;
- Astra orchestration;
- qualification;
- command/evidence state;
- GitHub Secrets.

AI credentials remain exclusively managed through GitHub Secrets. They must not be persisted on MediaHub nodes.

### 4. AI Gateway Plane

OmniRoute remains an independent candidate AI gateway layer.

Purpose:
- unified AI endpoint;
- provider routing;
- fallback;
- load balancing;
- provider health.

It must not be conflated with either the Media Mesh or Development Mesh.

## Target logical architecture

Control Plane
-> Development Mesh (VPN + distributed development)
-> Media Mesh (high-speed data/compute)

AI Gateway is an independent service plane reachable from Astra/development infrastructure.

## Constraints

- GOLD Run #176 remains untouched.
- Immutable R4 baseline remains untouched.
- Desktop Commander remains prohibited.
- No secrets are written to Git or persistent node configuration.
- VPN/mesh is not intended to bypass provider regional restrictions.
- Existing provider qualification evidence remains authoritative until refreshed.

## Architectural principle

The Development Mesh and Media Mesh may share underlying physical links or selected transport technology, but they are separate logical planes with different optimization criteria. The development VPN should not be treated as the high-speed data bus for the MediaHub product.

## Next work

1. Audit existing OmniRoute credential handling.
2. Compare development-mesh candidates (WireGuard/Headscale/NetBird/Netmaker) for distributed development.
3. Separately evaluate high-speed Media Mesh transport suitable for large data and distributed compute.
4. Keep deployment isolated from the active GOLD run.
