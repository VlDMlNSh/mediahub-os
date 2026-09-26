# MediaHub Autonomous Development — Wave 04C Checkpoint

Date: 2026-09-10
Trigger: `Продолжать`
Status: CONTINUATION-READY / RELEASE-LOCKED / PRODUCTION-NOT-AUTHORIZED

## Immutable lineage
- R4 SHA: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`
- R4 TREE: `2279612908135418b2b5448d598274ea6741deaa`
- R4 verified unchanged.

## Git state
- Branch: `engineering/mh21-sandbox-lifecycle-20260910`
- Previous HEAD: `d93e47cf11ac38018793195c2f91f53b4735fdc5`
- Wave 04C milestone commit: `f2ea917be09c1186155803a7b00ca148bbc76cea`
- Wave 04C TREE: `fde5a0421a5685a46d8f2a9d60f1458e73661a3d`
- Working tree was clean immediately after milestone commit.

## Implemented
- GitHub prior-art review completed for official Codex and Claude Code CLI surfaces.
- Native agent launch contract added; OpenRouter wrappers are not used by the new contract.
- Qualified model and Credential Broker checks are required before launch resolution.
- HTTPS endpoint requirement is enforced.
- Codex command uses native `codex exec` JSON/ephemeral/workspace-write surface.
- Claude command uses native print/JSON/model surface.
- No secret is placed in command arguments.
- Prior-art registry updated with Wave 04C decision and sandbox-runtime future reference.

## Evidence
- Full pytest: `298 passed`.
- Repository security scan: `SECURITY_RC=0` / `SCAN_OK`.
- Functional baseline: `FUNCTIONAL_BASELINE=PASS`.
- Baseline SHA256: `9cab7f0518208ecaeae8f605785a9e25eb9ed1ae9db420b19898fe83059dc18a`.
- Governance SHA256: `0160f24d3364d44b33aadc330be1519b99b61af4a3941400563caaf4d9576b4b`.
- Targeted Ruff: PASS.
- Targeted mypy for new implementation: PASS with explicit package bases.
- Targeted Semgrep: 0 findings.
- Targeted Bandit on new implementation: PASS; Bandit on tests reports normal B101 assert findings only.
- `git diff --check`: PASS.
- Native executables: Codex `0.151.0`, Claude Code `2.1.263`.
- Required MediaHub provider credential locations checked by metadata only: ABSENT.
- Real provider E2E: NOT EXECUTED / BLOCKED by absent credential material.

## Important qualification boundary
Wave 04C is NOT fully qualified yet. The launch contract is implemented and unit/security
verified, but native authenticated provider E2E and streaming integration remain unfinished.
No cloud lane is enabled and no provider policy is bypassed.

## Next safe action
1. Integrate the native launch contract into `CloudDevelopmentAdapter` without exposing secrets.
2. Bind model/protocol/capability routing and bounded streaming to the same boundary.
3. Add failure-injection/recovery tests for malformed stream, oversized event, timeout and revocation.
4. Re-run full qualification.
5. Only after 04C is fully qualified consider Wave 05.
