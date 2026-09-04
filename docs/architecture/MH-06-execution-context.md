# MH-06 — Execution Context

Status: PROPOSED

Each runtime operation carries explicit identity, service identity, capability, authorization result, correlation identifier, deadline, cancellation state, resource limits and security context.

ExecutionContext is descriptive/control metadata, not canonical application state. It cannot contain a hidden mutation primitive, arbitrary executable callback or caller-supplied transaction authority.

Context must be bounded, non-forgeable where identity/capability semantics require it, and re-established after crash/restart.
