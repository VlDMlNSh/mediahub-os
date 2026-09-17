# MediaHub AI Engineering Policy

## Mission
Treat this repository as the authoritative engineering source for MediaHub OS / MediaHub iOS.

## Operating rules
- Preserve the functional baseline, State Authority boundaries, recovery boundaries, and qualification policy.
- Never silently weaken tests, security checks, release gates, or invariants to make a task pass.
- Prefer the smallest reversible change that satisfies the requirement.
- Before modifying code, inspect adjacent contracts, schemas, tests, architecture documents, and existing workflows.
- Every non-trivial change must include or update tests.
- Never introduce production credentials, tokens, private keys, or secrets into the repository.
- Do not make production deployment changes from an AI coding task unless an explicit human-approved release workflow requires it.
- Treat generated code as untrusted until CI and independent review pass.

## Multi-agent protocol
- Architecture agent defines constraints and acceptance criteria.
- Implementation agents work in isolated branches and produce focused PRs.
- Verification agents inspect implementation independently and must not assume the implementer is correct.
- Security review is mandatory for changes involving permissions, networking, process execution, persistence, secrets, plugins, or deployment.
- When another agent has already modified the same subsystem, rebase/resolve deliberately rather than overwriting its work.

## Tooling
Use current stable versions of GitHub Actions and project tooling where compatible with the repository baseline. Pin critical actions to reviewed major versions and avoid floating third-party binaries.

## Completion standard
A task is not complete when code merely compiles. It is complete when the relevant tests, security checks, contracts, and repository qualification gates pass and the resulting PR is reviewable.
