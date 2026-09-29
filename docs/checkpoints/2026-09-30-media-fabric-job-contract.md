# Media Fabric Job Contract and Node Capability Model

Date: 2026-09-30

## Purpose

Define the protocol-level model for future MediaHub distributed execution without deploying it to the canonical Astra node.

## Node Capability

A node advertises only non-secret infrastructure capabilities:

- stable node identity;
- operating system/architecture;
- CPU capacity;
- RAM capacity;
- GPU vendor/model/memory;
- local storage capacity and capabilities;
- network capabilities;
- supported compute/storage roles;
- health/availability state.

Provider API keys, GitHub tokens, credentials and user data are never part of capability metadata.

## State model

Media Fabric separates:

1. Desired state — what should run.
2. Observed state — what actually exists and is healthy.
3. Execution state — what each job/task is doing.

An unavailable control-plane registry must not automatically invalidate already-running data-plane work.

## Job Contract

A distributed job should declare:

- input dataset/object;
- resource requirements;
- locality preferences;
- network requirements;
- retry/recovery policy;
- output dataset/object;
- execution constraints;
- optional checkpoint policy.

Example conceptual contract:

job:
  input: media/dataset
  resources:
    cpu: 8
    ram: 16GB
    gpu: 1
  locality:
    preferred: true
  recovery:
    retry: 3
  output: media/result

## Scheduler inputs

Placement should consider at minimum:

- resource fit;
- data locality;
- network cost;
- node health;
- failure domain;
- storage availability;
- execution policy.

The scheduler should prefer avoiding large data movement when an eligible compute node is already close to the required data.

## Failure model

The future PoC must test:

- worker disappearance;
- storage-node disappearance;
- network partition;
- scheduler restart;
- task retry;
- checkpoint/resume;
- duplicate execution prevention;
- result consistency.

## Architectural boundary

Development Mesh provides management connectivity and identity.

Media Transport provides data-plane connectivity.

Storage Fabric provides durable distributed data.

Compute Fabric schedules and executes tasks.

GitHub/Astra remains the control plane for development and qualification.

AI Gateway remains a separate service plane.

## Constraints

- No deployment to canonical mh-dev-01 from this checkpoint.
- GOLD #176 remains untouched.
- Immutable R4 baseline remains untouched.
- Provider credentials remain exclusively in GitHub Secrets.
- No network layer is to be used to bypass provider regional restrictions.

## Next step

Implement schemas and a non-canonical simulator/benchmark harness first. Only after schema and failure tests are stable should a real multi-node PoC be deployed to explicitly authorized test machines.
