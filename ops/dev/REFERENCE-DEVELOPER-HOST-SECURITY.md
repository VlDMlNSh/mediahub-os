# MediaHub Reference Developer Host Security Baseline

## Purpose

Define a reproducible, least-privilege development host for MediaHub OS 11.x LTS.
This is development infrastructure, not production infrastructure and not an
independent qualification authority.

## Toolchain

Required baseline: Node.js 22 LTS, Python 3.12, Git, OpenSSH, OpenSSL, GPG,
`jq`, `ripgrep`, `fd-find`, `shellcheck`, `shfmt`, `pre-commit`, `age`, pytest,
pytest-cov, Bandit and pip-audit.

Optional scanners such as Trivy, Syft, Grype, Semgrep, Hadolint, Actionlint,
Zizmor and Gitleaks may be added only from trusted, pinned distribution sources
and must not become release-authority dependencies.

## Security rules

1. Never place passwords, API keys, private keys or tokens in repository files,
   shell history, CI logs, evidence artifacts or agent prompts.
2. Privileged installation is interactive and fail-closed. Agents must never
   receive or store the administrator password.
3. Keep developer and qualification identities separate. Development agents
   cannot self-certify independent qualification.
4. Use isolated Git worktrees/branches per agent task.
5. Protect the immutable forensic target from force-push and mutation.
6. Require clean-worktree, exact-SHA, invariant and deterministic-test gates
   before producing a handoff.
7. Keep evidence append-only and content-addressed where practical.
8. Do not install heavy local models on the 8 GiB host without measured need.
9. Prefer user-space virtual environments and pinned dependencies over system
   Python modification.
10. Any new network-facing service requires explicit review before enablement.

## Agent lanes

- ARCHITECTURE: contracts and invariants only.
- RUNTIME: implementation and unit/integration tests.
- SECURITY: static/adversarial verification and hardening.
- VERIFICATION: deterministic reproduction and evidence generation.
- QUALIFICATION: independent review only; never delegated to implementation.
- RELEASE: packaging and release gates; no bypass authority.
- OPERATIONS/DEVEX: host automation, CI and developer ergonomics.

## Fail-closed conditions

Stop the affected lane on unexpected files, dirty protected branches, SHA drift,
failed tests, missing provenance, dependency ambiguity, secret exposure, scope
expansion, or attempted authority bypass. Continue unrelated safe lanes.
