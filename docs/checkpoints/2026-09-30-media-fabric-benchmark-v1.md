# MediaHub Media Fabric Benchmark v1

Date: 2026-09-30

## Purpose

Define a reproducible, non-canonical benchmark for the future MediaHub distributed Media Fabric. This document is a test specification, not a deployment authorization.

## Safety / isolation

- Do not modify canonical Astra or mh-dev-01.
- Do not touch GOLD #176.
- Do not modify immutable R4 baseline.
- Use only synthetic/non-sensitive test data.
- Provider/API credentials remain exclusively in GitHub Secrets.
- No credential may be persisted into benchmark nodes, images, logs, artifacts or repositories.

## Test topology

Minimum: 3 disposable/test nodes.

Node A: source + storage client.
Node B: storage + compute worker.
Node C: storage + compute worker.

The Development Mesh provides management connectivity only. Media Transport is measured separately and must not be assumed to be the Development Mesh data plane.

## Phase 1 — Network transport

Measure:
- direct P2P establishment;
- relay fallback;
- one, four and eight concurrent transfers;
- sustained throughput;
- median/p95 latency;
- packet-loss recovery;
- CPU and RAM overhead;
- reconnect time after node/network interruption;
- NAT traversal behavior.

Primary output: direct-versus-relay throughput and resource-cost table.

## Phase 2 — Storage

Candidates:
- SeaweedFS;
- JuiceFS.

Workloads:
- 1 GiB, 10 GiB and larger synthetic sequential files where test capacity permits;
- many small files;
- parallel reads/writes;
- replication;
- node removal/recovery;
- adding a new storage node;
- disk heterogeneity.

Metrics:
- MB/s or GiB/s;
- operations/s;
- p50/p95 latency;
- CPU/RAM overhead;
- replication bandwidth;
- recovery time;
- usable capacity overhead.

## Phase 3 — Compute

Candidates:
- Ray;
- Nomad;
- OpenFabric;
- Dask.

Workloads:
- CPU task fan-out;
- GPU task placement where available;
- heterogeneous resource constraints;
- worker failure;
- retry/recovery;
- data-local versus remote execution;
- concurrent jobs.

Metrics:
- task startup latency;
- tasks/s;
- successful completion rate;
- recovery time;
- CPU/GPU utilization;
- network bytes per task;
- scheduler overhead.

## Phase 4 — End-to-end Media Fabric

Test path:

Node A -> Media Transport -> Storage Fabric -> Compute Node B/C -> Storage Fabric -> Node A

Use synthetic media-like files and deterministic compute transforms.

Measure:
- end-to-end elapsed time;
- network throughput;
- storage throughput;
- compute utilization;
- data movement volume;
- failure recovery;
- repeatability across at least three runs.

## Acceptance gates

A candidate advances only if the benchmark provides reproducible evidence for:
1. stable node connectivity;
2. measurable direct path when available;
3. predictable relay fallback;
4. storage recovery after node loss;
5. compute recovery after worker loss;
6. bounded CPU/RAM overhead;
7. no persistent credentials on worker nodes;
8. successful end-to-end workload execution.

No overall winner is declared by this document. Selection must follow measured workload-specific evidence.

## Target architecture after qualification

Control Plane -> Development Mesh -> Compute Fabric / Storage Fabric -> Media Transport

AI Gateway remains an independent plane.
