# Astra gated development

Apply useful ECC workflow patterns without making ECC a second controller.

## Contract
1. Inspect boundary and acceptance criteria before editing.
2. Form a short implementation plan; do not broaden scope.
3. Implement the smallest change satisfying the contract.
4. Run focused regression tests, then broader tests when cross-cutting.
5. Review the diff for scope violations, secrets, debug artifacts, and policy changes.
6. Report evidence, never manufacture PASS markers.

## Astra invariants
- Target SHA is immutable for a worker run.
- One task branch per claim; never write directly to main.
- Boundary and forbidden-surface checks are fail-closed.
- Verification is a separate process from building, even when both use Claude.
- PASS is allowed only when evidence directly proves every acceptance criterion.
- Production infrastructure, credentials, user data, and unrelated paths are out of scope unless explicitly authorized.

## Efficiency
Prefer deterministic shell/editor operations and focused tests. Avoid broad rewrites and speculative refactors.
