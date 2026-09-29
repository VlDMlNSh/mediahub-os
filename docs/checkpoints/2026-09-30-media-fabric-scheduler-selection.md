# Media Fabric Scheduler Selection

Date: 2026-09-30

## Current evidence

Ray's current scheduling documentation provides:
- resource requirements and node labels for eligibility;
- locality-aware task placement;
- placement groups with PACK, STRICT_PACK, SPREAD and STRICT_SPREAD;
- gang scheduling for workloads requiring resources to be reserved together.

Nomad provides:
- hard constraints for mandatory placement rules;
- soft affinities for preferred placement;
- node pools/datacenters and scheduler placement semantics.

OpenFabric provides a decentralized local compute mesh with peer discovery and local API surfaces, but its current project description is broader than the MediaHub scheduler contract and requires independent qualification before being used as the primary scheduler.

## Decision for PoC

Ray is the primary scheduler candidate for the first Media Fabric PoC because its documented scheduling model maps directly to the already-defined MediaHub requirements:

1. resource fit;
2. node capability selection;
3. data locality;
4. multi-resource placement;
5. failure-aware distributed workloads.

Nomad remains a secondary infrastructure scheduler candidate if MediaHub later needs general service/infrastructure scheduling outside compute/data workloads.

OpenFabric remains a feasibility candidate for decentralized edge/local compute, not the canonical scheduler.

## Required MediaHub abstraction

MediaHub must not expose Ray-specific APIs as its public contract.

The internal architecture should use:

MediaHub Job Contract
  -> Scheduler Adapter
  -> Ray / alternative scheduler

This preserves the ability to replace the scheduler without changing application-level job definitions.

## First PoC

The first non-canonical PoC should test:

- 3+ heterogeneous nodes;
- CPU-only and GPU-capable nodes;
- local and remote dataset placement;
- locality-aware placement;
- hard resource constraints;
- preferred locality;
- multi-node placement;
- node failure and retry;
- scheduler restart;
- duplicate execution prevention;
- result persistence.

Storage should be benchmarked separately first, with SeaweedFS as the primary candidate.

## Safety and scope

No deployment to mh-dev-01 is authorized by this checkpoint.

GOLD #176 remains untouched.

Immutable R4 baseline remains untouched.

Provider credentials remain exclusively in GitHub Secrets and must never be included in scheduler metadata.
