# MH-17 — Device Simulator

**Status:** PROPOSED / CANDIDATE

A simulator is a verification tool, not a trust authority. It MUST model identity, discovery, capabilities, state transitions, commands, events, telemetry, failures, latency, loss, retries, malformed input, disconnects, and ambiguous outcomes.

Simulator behavior MUST be distinguishable from real-device evidence. Passing simulation does not establish hardware/protocol qualification.

The simulator SHOULD support deterministic scenarios and fault injection for security, safety, compatibility, backpressure, offline, and command-lifecycle tests.
