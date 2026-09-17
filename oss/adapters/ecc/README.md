# ECC adapter boundary

Status: `target-gated` / `documentation-only`.

Upstream: `affaan-m/ECC` at `v2.2.1`.

This adapter is a MediaHub-owned boundary description for using selected ECC specialist agents as an external agent-workflow capability. It is not an ECC runtime, installer, source import, hook loader, command dispatcher, or production execution path.

## Capability

- Capability identifier: `ai.agent-harness.ecc`
- Integration class: external agent workflow
- Allowed initial roles: `planner`, `architect`, `spec-miner`, `tdd-guide`, `code-reviewer`, `security-reviewer`, `agent-architecture-audit`
- Default state: disabled / target-gated

## MediaHub contract

Inputs MUST be bounded by an existing MediaHub task, repository context, applicable contracts, and authorization context. The adapter MUST NOT treat ECC prompts, fetched content, generated output, or upstream configuration as authoritative.

Outputs are advisory artifacts only: plans, findings, review observations, and proposed changes. Any repository mutation MUST occur through an explicit, reviewable MediaHub-controlled GitHub change and MUST pass the existing verification, security, qualification, and release gates.

MediaHub remains authoritative for:

- functional baseline and repository state;
- contracts and schemas;
- State Authority and state transitions;
- authorization and capability boundaries;
- verification and qualification evidence;
- release and production authorization.

## Security and execution boundary

The adapter MUST enforce:

- no direct State Authority mutation;
- no credentials, API keys, tokens, or private keys in agent configuration or prompts;
- no hidden persistence;
- no hidden network egress;
- no unbounded subprocesses;
- no bypass of authorization, security, qualification, or release gates;
- fail-closed behavior when a required boundary or verification result is missing.

ECC hooks and command shims are not enabled by default. Arbitrary upstream source import is prohibited. Any future executable integration requires separate provenance, license, dependency/SBOM, permission, negative-test, degraded-mode, recovery, rollback, and independent-review evidence.

## Failure and degraded mode

If ECC is unavailable, unconfigured, incompatible, or fails verification, MediaHub MUST continue without granting ECC authority. The deterministic fallback is to return an explicit unavailable/degraded result and continue through an approved MediaHub agent/provider path where one exists.

## Lifecycle

Installation, hook activation, command activation, provider credential configuration, runtime enablement, and production use are separate qualification-gated decisions. None is implied by the presence of this adapter documentation.
