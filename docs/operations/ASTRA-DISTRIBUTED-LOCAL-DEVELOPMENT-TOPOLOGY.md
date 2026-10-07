# ASTRA Distributed Local Development Topology

## Authority and pools

- **mh-dev-01** is the controller and authority node. It owns signed command admission, queue promotion, qualification gates, and authoritative result publication.
- **mh-dev-02** is the primary local executor pool.
- **Voktors-Mini.Dlink** is the fast local executor pool.
- **Voktors-Mac-mini.local** is the canonical identity used by the fast-pool admission contract when the Mac runner is registered under its stable hostname.

## Executor architecture

The executor matrix includes both **Codex** and **Claude**. A task has an A2 Builder and an independent A3 Verifier. The builder is constrained to the task boundary; the verifier evaluates the resulting diff and scoped test evidence against the literal acceptance criteria.

Every worker is bound to an exact **target SHA**. A worker rejects a mismatched checkout or dirty workspace before execution. Workers create isolated branches and never write directly to `main`. GitHub Actions is the evidence transport: worker results, verifier evidence, branch heads, and promotion decisions are published as immutable workflow artifacts and checked against the target SHA.

## Promotion rules

Promotion is **fail-closed**. A missing launcher, authentication/policy denial, identity mismatch, stale evidence, target-SHA mismatch, boundary violation, verifier failure, or malformed evidence blocks promotion. No historical evidence is substituted for a fresh run.

A task may be idempotent: when its declared acceptance is already satisfied, the builder may make no source change. In that case the worker records `NO_CHANGES_REQUIRED`, runs the independent verifier and scoped regression suite, and promotes only when those checks pass.

## Security boundary

Workers do not receive authority to merge to `main`, alter production infrastructure, modify credentials, or access user data outside their declared task boundary. Secrets are suppressed from evidence and are never committed.
