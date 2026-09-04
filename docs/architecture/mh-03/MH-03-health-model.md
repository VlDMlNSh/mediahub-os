# MH-03 Health Model

Health is bounded observation, not authority.

States:
- STARTING: initialization in progress;
- READY: required foundation available;
- DEGRADED: safe reduced operation;
- RECOVERING: bounded recovery active;
- STOPPING/STOPPED: lifecycle termination.

Health signals should distinguish liveness, readiness and dependency health. Health must not expose mutable internal objects or sensitive data.

Readiness must fail closed for missing critical foundation. Optional dependency failure can be represented as degraded without falsely reporting full readiness.
