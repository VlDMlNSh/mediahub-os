# PR #458 Independent Routing Governance Review — Wave 371 — 2026-10-22

## Disposition

**Review status: PARTIAL / NOT ACCEPTED.** PR #458 has five exact-head checks completed successfully, but the required branch-protection and review gates are not verifiable through the current GitHub integration. No merge or dispatch was attempted.

## Immutable references

- Repository: `VlDMlNSh/mediahub-os`
- `main` HEAD observed: `b33ab31674bfa9595a8f2ba5a570dbc1eb3686b2`
- PR #458 head: `afd6dcd901da44b4cdb5d155f96dce172adb3c55`
- PR #458 base: `main`
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Evidence collected

- Read PR #458 file list and patches.
- Read back `.github/ai/model-router.yml` at blob SHA `73de4ab3c16e5e6daec7739ece40426bed9fe474`.
- Read back `scripts/verify_ai_factory.py` at blob SHA `1d05578e1596eda24f7bcd5381e063a46aa01049`.
- Read back `tests/ai/test_provider_selector.py` at blob SHA `bf7fbedeb75e502fe28512ae6083b4775a95ed35`.
- Current exact-head checks for PR #458: 5/5 completed/success:
  - Verify AI factory policy and secret boundaries
  - validate
  - Verify approved executor routing boundaries
  - Verify Astra agent boundary
  - verify
- GitHub reviews API returned zero reviews and review threads.
- Classic branch protection endpoint returned HTTP 403 `Resource not accessible by integration`. Rulesets endpoint returned an empty list; this does not prove there are no inaccessible organization-level or other rules.
- Gemini controller and all three child workflow runs are terminal completed/success on immutable target `1c22d82c1750aebe0c5571e088d9c0adc012c42f`: controller 39786556843, Agent 1 39786584867, Agent 2 39786587768, Agent 3 39786592525. This is execution evidence, not candidate acceptance.

## Review findings

1. **Routing policy direction is consistent with the governing boundary.** The router is policy-only, prohibits direct provider calls and paid fallback, permits Gemini only through the controller workflow, keeps Claude/Ollama as a separate local lane, and uses fail-closed behavior for unknown routes.
2. **Direct provider smoke workflows are removed.** The PR removes OpenAI, Anthropic, Gemini direct API, and OpenRouter smoke workflows. This addresses the unauthorized alternate provider-routing surface described in the existing Wave 369 audit.
3. **Static guard coverage is stronger for routing policy but does not qualify runtime.** The verifier asserts required policy strings, controller secret-binding names, and absence of direct-provider workflows. The updated test module asserts these policy boundaries. These are source-level/static checks; they do not demonstrate live runtime isolation, provider quota behavior, resumable routing, or full Contour A acceptance.
4. **Review/merge gates remain blocked by missing evidence.** There are no recorded reviews/review threads returned, and the integration cannot read branch protection. Do not infer that approval is unnecessary or that branch protection is disabled.
5. **No changes were made to code, secrets, permissions, or workflow dispatch state in this pass.**

## Gate ledger

| Gate | Status | Evidence |
|---|---|---|
| Exact-head CI for PR #458 | SUCCEEDED | Five checks on `afd6dcd901da44b4cdb5d155f96dce172adb3c55` |
| Source-level routing review | PARTIAL | Router, verifier, tests and PR patches inspected |
| Independent required review | NOT VERIFIED | Review API and review threads empty |
| Branch protection / required status policy | NOT VERIFIED | Endpoint HTTP 403; rulesets empty is inconclusive |
| Runtime qualification | NOT RUN in this pass | No runtime test or new dispatch attempted |
| Merge / deployment / acceptance | NOT PERFORMED | Governance gates incomplete |

## Next bounded action

Use an authorized GitHub UI/administrative route to inspect the repository's branch protection and required reviews/status checks for `main`. Once those requirements are established, satisfy the required independent review and recheck exact-head CI. Do not merge while these gates are unknown. In parallel, continue independent verification of the Contour A schemas, issuer/capability gates, and runtime evidence under Issue #301.

## Related evidence

- [PR #458](https://github.com/VlDMlNSh/mediahub-os/pull/458)
- [Wave 369 merge and routing governance audit](https://github.com/VlDMlNSh/mediahub-os/blob/docs/next-wave-370-gemini-batch-reconciliation-20261022/docs/checkpoints/MEDIAHUB-MERGE-AND-ROUTING-GOVERNANCE-AUDIT-WAVE-369-2026-10-22.md)
- [Wave 370 Gemini batch reconciliation](https://github.com/VlDMlNSh/mediahub-os/blob/docs/next-wave-370-gemini-batch-reconciliation-20261022/docs/checkpoints/MEDIAHUB-NEXT-GEMINI-BATCH-RECONCILIATION-WAVE-370-2026-10-22.md)
- [Canonical Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
