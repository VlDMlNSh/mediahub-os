# MediaHub Autonomous Development — Wave 04C / Component Selection Checkpoint

Date: 2026-09-10

## Governance

R4 SHA: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`
R4 TREE: `2279612908135418b2b5448d598274ea6741deaa`
Release: LOCKED
Production: LOCKED

## Cross-chat rule

Before any significant component is implemented, inspect GitHub prior art, evaluate maturity, maintenance, license, tests, security and architecture, then select only the smallest stable blocks required by the MediaHub-native contract.

External projects are never automatically installed wholesale and never become MediaHub authority.

## Wave 04C evidence

Selected native agent approach: official Codex and Claude CLIs behind a MediaHub-native launch contract.

Codex: USE-AS-IS through controlled adapter.
Claude Code: USE-AS-IS through controlled adapter.
OpenRouter wrappers: not accepted as native implementation.

The launch boundary requires qualified model selection, broker-owned credentials, HTTPS endpoints and dynamic executable resolution. Secrets are not placed in argv or logs.

## Component-selection checkpoint

The complete selection matrix is stored in `docs/COMPONENT-SELECTION-MATRIX-2026-09-10.md`.
The existing GitHub component registry remains the source of prior-art decisions.

Primary sandbox candidates: Daytona, E2B, Anthropic sandbox-runtime, Firecracker.
They are candidates only; none is production-qualified or installed by this checkpoint.

Orchestration reference: LangGraph. MCP reference: official Python and Swift SDKs.
Policy reference: OPA. Supply-chain/security infrastructure: OpenTelemetry, Cosign, Gitleaks, Semgrep, OSS-Fuzz, Renovate.

## Execution evidence

Local targeted tests after executable-resolution fix: 17 passed.
Ruff: PASS.
mypy: PASS.
Semgrep: 0 findings.
Repository security scan before documentation-only selection work: SECURITY_RC=0.
Real provider E2E: NOT EXECUTED because authorized credentials were absent.

## GitHub branch

`continuation/w04c-component-selection-20260910`

This branch was created from checkpoint `5a3784495938dc5976befd99910d18e51fb25912` without force-push or history rewrite.

GitHub commits on this continuation branch include the component matrix and native agent launch/test boundary.

## Next action

Continue Wave 04C: integrate the native launcher with Cloud Development Adapter, then qualify bounded streaming, timeout/cancellation, revocation and failure-injection paths before Wave 05.
