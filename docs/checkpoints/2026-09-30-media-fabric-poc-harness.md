# Media Fabric Non-Canonical PoC Harness

Date: 2026-09-30

## Objective

Validate the MediaHub Job Contract and scheduler semantics before any deployment to the canonical Astra node.

## Harness layers

1. Schema layer
   - validate Node Capability;
   - validate Job Contract;
   - validate Desired/Observed/Execution state transitions.

2. Scheduler simulation
   - heterogeneous CPU/GPU nodes;
   - resource-fit filtering;
   - locality scoring;
   - hard constraints;
   - preferred constraints;
   - deterministic tie-breaking.

3. Failure injection
   - node loss before execution;
   - node loss during execution;
   - storage loss;
   - network partition;
   - scheduler restart;
   - duplicate worker/report submission.

4. Evidence layer
   - placement decision;
   - locality hit/miss;
   - bytes moved;
   - execution duration;
   - retries;
   - final result identity;
   - recovery duration.

## Determinism

The simulator must produce reproducible decisions from:
- fixed node inventory;
- fixed job contract;
- fixed dataset locations;
- explicit scheduler policy;
- explicit random seed when randomized behavior is introduced.

No production credentials or external provider calls are required.

## Minimal scenarios

### S1 Resource fit
GPU job cannot be placed on CPU-only nodes.

### S2 Locality
Two eligible GPU nodes exist; one already has the input dataset. Scheduler should select the locality-compatible node under the defined policy.

### S3 Hard constraint
A node outside the required capability/label set must never receive the job.

### S4 Failure before start
Selected node disappears; scheduler must re-place the job without creating duplicate committed output.

### S5 Failure during execution
Worker disappears; retry must produce one committed result.

### S6 Scheduler restart
Observed state is reconstructed from durable execution evidence; completed work must not be duplicated.

### S7 Network degradation
A locality-remote placement is rejected or penalized when its required network threshold cannot be satisfied.

## Success criteria

The PoC is not a performance qualification. It is a correctness gate.

PASS requires:
- valid schemas;
- deterministic placement for deterministic inputs;
- hard constraints never violated;
- locality policy respected;
- no duplicate committed result;
- recoverable node failures;
- reconstructable execution state;
- machine-readable evidence.

Performance benchmarking follows only after this correctness gate.

## Architectural boundary

The harness is non-canonical and must not alter:
- mh-dev-01;
- Astra GOLD #176;
- immutable R4 baseline;
- GitHub Secrets.

The first real multi-node deployment remains a separate, explicitly authorized step.
