# MH-17 — Error Model

**Status:** PROPOSED / CANDIDATE

Errors are classified by boundary and recovery meaning: discovery, identity, authentication, authorization, protocol, validation, capability, transport, timeout, rate/resource, device, persistence, security, safety, and lifecycle.

Errors MUST carry stable machine-readable class, correlation context, retryability, severity, and whether outcome is known or unknown where applicable.

A timeout or transport error does not prove physical failure. Ambiguous command outcomes MUST enter explicit `UNKNOWN` handling and recovery policy, especially for non-idempotent operations.
