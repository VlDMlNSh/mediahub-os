# MediaHub OS — Gemini Three-Account Queue Validation, Wave 62

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SOURCE REVIEW COMPLETE / DISPATCH AND RUNTIME EVIDENCE PENDING**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Queue acceptance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Gemini agent workflows: merged PR #314, merge commit `4f2788058a98d84a6189651364e154dfb21c2899`

## 1. Corrected quota assumption

Owner clarification: `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, and `GEMINI_API_KEY_3` represent three different Google accounts. The proposed quota model must therefore treat them as three independent account scopes, subject to verification that each key is issued by its claimed account and that the applicable project/model/metric quota is independent.

For each credential alias, record a non-secret account-scope identifier and evidence of account/project association. The coordinator may aggregate available capacity across the three scopes only for tasks whose provider policy, model availability and data-egress class permit that route. Each account retains its own RPM/RPD/TPM or other documented limits and cooldown. Do not merge the three limits into one undifferentiated counter, and do not infer independent capacity from key names alone.

If two or more keys resolve to the same project or shared quota scope, those entries must share the upstream scope ledger. This is a source-of-truth correction to prior generic statements that treated Gemini key count as insufficient evidence of additional quota.

## 2. Existing workflows confirmed from GitHub main

| Workflow | Secret mapping | Blob SHA | Source status |
|---|---|---|---|
| `gemini-autonomous-engineering.yml` | `GEMINI_API_KEY` | `09523d809530ae5b7bf528eab5fa53bc5deaf92d` | Existing bounded Gemini engineering workflow |
| `gemini-agent-2.yml` | `GEMINI_API_KEY_2` | `259c8c82b8d90a39e1c90e65390e469b241b5581` | Research & Architecture |
| `gemini-agent-3.yml` | `GEMINI_API_KEY_3` | `91b5397001e088dfae2f450ee77c9c23118b5601` | Security & Verification Review |

PR #314 is merged. Source inspection confirms manual `workflow_dispatch`, GitHub-hosted `ubuntu-latest`, 30-minute timeout, explicit per-workflow secret mapping, GitHub MCP tools limited to file read, branch creation, file writing and PR creation, and an output/artifact validation step.

These source facts establish workflow configuration only. They do not establish current secret presence, account ownership, a successful API call, durable queue behavior, or autonomous completion.

## 3. Queue reality and acceptance boundary

Issue #301 states that CAF-Q-001…CAF-Q-015 is a documentary queue, rather than an active scheduler or dispatch system. The current Gemini workflows each accept one manually supplied task and open a PR. Their concurrency groups include `github.run_id`, so they do not serialize work across runs and do not themselves provide a shared autonomous queue.

Therefore, “three agents are configured” and “the autonomous queue is operating” are separate acceptance states. The next implementation slice must add or reuse a bounded queue coordinator, task lifecycle and recovery behavior before queue operation can be claimed.

## 4. Recommended initial operating sequence

1. Use the existing three Gemini workflows without changing credential values or scope.
2. Dispatch one bounded read-only task through each account-specific workflow after owner-authorized dispatch is available.
3. Capture workflow run ID, job ID, workflow conclusion, artifact name/digest, MCP tool-call counts, task ID and resulting PR number/head SHA.
4. Verify each run shows the intended workflow and secret reference in source configuration; runtime evidence must never reveal secret values.
5. Dispatch a second task only after the first task's terminal state and evidence are reconciled.
6. Check duplicate task IDs, duplicate branches/PRs, interrupted runs and stale tasks.
7. Exercise quota exhaustion/fallback only after explicit provider-call and qualification authorization. Never intentionally exhaust a production quota to prove routing.
8. Treat the pool as operational only after independent verification of successful runs, queue recovery, idempotency, secret redaction, correct quota-scope accounting and the A0/MH-12/R-06/target-manifest gates.

## 5. Known implementation gaps

- No shared task dispatcher or durable queue operation has been evidenced. Issue #301 explicitly records a documentary queue.
- Each agent workflow is manually dispatched; its per-run concurrency key does not coordinate other runs.
- Workflow action references `@v0` and `actions/checkout@v4` remain mutable major tags; full-SHA supply-chain pinning is an identified hardening requirement.
- The workflows grant job-level `contents: write` and `pull-requests: write`; effective permissions and organization settings require run evidence and least-privilege review.
- The three account/project quota scopes and free-tier availability require owner-side/provider-side evidence; GitHub source access cannot establish account ownership or quota.
- Issue #301 keeps A0 issuer/ingress/lease/cancel/recovery, R-06 privacy authority, target manifest, schema meta-validation and independent review as acceptance dependencies.

## 6. Execution boundary

This pass read source files and PR/issue metadata. No workflow dispatch or provider call was performed. No secret values were read. No tests, qualification, installation, host/runtime inspection, infrastructure change, deployment, migration or merge occurred.

The current GitHub connector tools available in this session expose workflow job/run inspection and rerun operations, but no workflow-dispatch action. Therefore a dispatch cannot be initiated from this session through the connected GitHub action surface. The owner can launch the existing manual workflows using the runbook below; after run IDs exist, evidence can be inspected through GitHub.

Runbook: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/operations/GEMINI-AGENT-POOL-AND-ROUTER-RUNBOOK-WAVE-42.md

## 7. Next bounded action

Use issue #301 as the controlling work item. Prepare the smallest implementation PR for task intake/claim/lease/idempotency/recovery and evidence reconciliation, reusing accepted A0 and v0.2 schema contracts. Keep automatic dispatch, provider calls, schedules and qualification behind separate gates. In parallel, the owner may launch the three manual Gemini workflows one at a time; attach exact run and artifact evidence before claiming operational success.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
