# MediaHub self-regulating / self-recovering control loop

Status: ENGINEERING DESIGN / NOT RELEASE AUTHORIZATION

## Objective

Provide a bounded control loop for an appliance/building OS without allowing an AI model or an external
component to become the authority.

## Loop

1. Observe: collect health, metrics, events and resource signals through OTel/Prometheus.
2. Classify: map a signal to a known failure domain and severity.
3. Decide: deterministic policy selects a permitted action.
4. Authorize: State Authority/security policy verifies that the action is allowed.
5. Act: execute restart, retry, failover, restore, quarantine or update through a bounded adapter.
6. Verify: run health/readiness and invariant checks after the action.
7. Record: persist evidence, correlation, causation and outcome.
8. Recover: use Temporal for durable retries/workflows; use restic/RAUC for data/system recovery.
9. Escalate: stop and require operator intervention when confidence, authorization or invariants fail.

## Failure domains

- process/service failure -> supervised restart
- transient integration failure -> bounded retry/backoff
- stale external data -> reject/quarantine; never overwrite canonical state
- persistence failure -> fail closed, restore only through authorized recovery
- corrupted artifact -> reject signature/hash and quarantine
- failed update -> RAUC rollback/recovery path
- capacity pressure -> admission control/degradation, not uncontrolled spawning
- AI uncertainty -> advisory result only; deterministic validator decides

## Hard invariants

- State Authority is the sole canonical mutation authority.
- Recovery cannot bypass authentication/authorization.
- Health is not authorization.
- Discovery is not trust.
- A successful external call is not proof that its data is authoritative.
- Every automated action has a correlation ID and evidence record.
- Repeated failure moves the system toward safe degradation, not infinite retries.

## Component roles

OTel/Prometheus observe. Temporal executes durable workflows. PostgreSQL stores authoritative metadata.
Object storage stores immutable/binary artefacts. restic protects recoverability. RAUC protects appliance
software recovery. Cosign verifies release provenance. Syft/Trivy protect the software supply chain.
IfcOpenShell/PaddleOCR/OpenCV/ONNX/llama.cpp provide bounded processing capabilities only.
