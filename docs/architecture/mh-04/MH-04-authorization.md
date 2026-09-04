# MH-04 Authorization

Authorization evaluates WHO may perform WHAT on WHICH RESOURCE under WHICH CONTEXT and POLICY.

Decision: ALLOW, DENY or QUARANTINE. Allow is permission to continue through the canonical command path, not permission to mutate directly.

Missing authorization, unknown capability, invalid context or policy ambiguity -> DENY.

Authorization must be deterministic, auditable and bounded. It must not create a second authority path.