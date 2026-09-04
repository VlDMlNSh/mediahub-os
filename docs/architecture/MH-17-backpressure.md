# MH-17 — Backpressure

**Status:** PROPOSED / CANDIDATE

Backpressure is mandatory at discovery, event, telemetry, command, and adapter boundaries. Queues require bounded capacity and explicit overflow semantics.

Preferred behavior is protocol-aware sampling/coalescing for telemetry, rejection/defer for commands, and preservation of security/safety events. Dropping data MUST NOT be interpreted as a state transition.

Sustained overload may trigger degraded operation or quarantine. Backpressure MUST NOT permit direct adapter-to-State-Authority bypass.
