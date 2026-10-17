# MediaHub OS — GitHub-Hosted Cloud Router Coordinator Proposal, Wave 61

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **PROPOSAL / PLAN-ONLY FIRST SLICE / LIVE PROVIDER INVOCATION GATED**
- Prior design: [Wave 60 — GitHub-Hosted Key Rotation and Egress](MEDIAHUB-GITHUB-HOSTED-KEY-ROTATION-AND-EGRESS-DESIGN-WAVE-60-2026-10-17.md)
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Decision

All cloud-agent orchestration, API-key routing, quota accounting, provider calls and cloud model execution remain on GitHub-hosted Actions runners. Local servers participate only in local inference and local computation. User location, carrier, local network and local public IP are excluded from routing inputs. Provider policy for GitHub runner egress remains an admission gate.

The first implementation slice should be a manually dispatched **plan-only** coordinator. It validates one approved GitHub Issue, resolves a candidate route from the existing registry, calculates the quota-scope alias, and records a redacted plan. It performs zero provider calls. No schedule or provider executor belongs in this first slice.

## Reuse-first source findings

- `ops/qualification/provider_model_registry.json` is the existing canonical provider catalog. Its cost/persistence fields are candidate labels, not proof of current account eligibility.
- `ops/qualification/qualify_execution_backends.py` is a qualification utility, not a router. It selects the first present credential alias, uses short fixed retries, has no durable quota/cooldown ledger, and performs concurrent provider probes.
- Gemini Agent 2/3 workflows map one key each and their concurrency group includes `github.run_id`; this does not create a global mutex or shared quota ledger.
- The existing qualification workflow targets a self-hosted runner and is excluded from the cloud path.
- GitHub Issues are the durable task inventory. Actions runs are transient executors; concurrency is a guardrail, not a FIFO queue.

## First-slice contract

- Workflow: `.github/workflows/mediahub-cloud-router-coordinator.yml`.
- Trigger: `workflow_dispatch` only.
- Runner: `ubuntu-latest`; reject self-hosted labels for the cloud lane.
- Inputs: one numeric `task_issue_number` and fixed `mode=plan`. No input may specify a secret name, URL, shell command, arbitrary branch or arbitrary model.
- Task: require an open issue with an approved queue label and a versioned JSON task envelope. Reject unknown fields and unsupported enum values. Issue title/body/comments are untrusted data.
- Planner permissions: minimum issue/registry read access. Add state-branch write access only when implementing the state update. Omit provider secrets, pull-request write access and deployment permissions from the planner.
- Concurrency: stable repository-scoped group with `cancel-in-progress: false`. Issues remain the authoritative queue because pending Actions runs can be coalesced.
- Output: task ID, candidate provider/model, quota-scope alias, decision reason, known reset/cooldown, gate status and sanitized evidence digest.
- Exit semantics: invalid task/state => `BLOCKED`; unresolved admission gates => `GATES_OPEN`; no eligible free route => `QUOTA_EXHAUSTED` or `PROVIDER_QUARANTINED`.

## Static secret boundaries

The planner receives zero provider secrets. Dynamic secret-name lookup from task content is prohibited. Each later provider-specific job must declare its own secret mapping statically and receive only that credential.

The first live-capable version should attempt at most one provider route per run. On quota exhaustion it persists the scoped cooldown and defers; the next run selects the next eligible route. This avoids exposing all provider keys to one process.

- Gemini aliases `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, and `GEMINI_API_KEY_3` share quota state until distinct Google projects and independent quota are evidenced.
- SiliconFlow alias mismatch `SILICON_KEY_2` vs `SILICONFLOW_API_KEY_2` remains a blocker.
- Missing/invalid/unverified credentials quarantine that route.
- Paid fallback remains disabled.

## Quota state and recovery

Use a dedicated state branch with versioned JSON records keyed by provider, account/project/organization, model, metric and reset window. Store only aliases, counters, timestamps, task IDs, attempt counts and sanitized status. Store zero secret values, auth headers, raw prompts, raw response bodies or credential-bearing URLs.

State updates use current ref/blob SHA and optimistic ref advancement. Bounded conflict retries reread and recompute. Read/write failure, invalid schema, stale or ambiguous quota state, or repeated conflict means defer/quarantine. Fail-open behavior is prohibited.

Error policy:
- 429/quota: honor documented `Retry-After` and reset headers.
- 401/403: quarantine credential/provider route pending review; region/account policy rejection quarantines the route for this runner egress.
- 402/billing: stop the route; never activate billing automatically.
- 404/model mismatch: quarantine the model mapping.
- transient network/5xx: bounded retry with backoff and hard attempt budget.
- cross-provider fallback: require task-level data-egress permission and accepted retention/security terms.

## Governance gates

Live provider invocation remains gated on accepted A0 task lifecycle/authorization, MH-12 tool/role enforcement, R-06 audit/privacy/data-egress disposition, the GitHub-hosted target manifest, provider/account/model/quota/retention/egress evidence, secret-alias reconciliation, independent schema/state review, and separate explicit authorization for tests, qualification, workflow dispatch and provider calls.

## Verification boundary and next slice

This document is a proposal based on source inspection. No workflow, runtime code, secret, provider account, queue or state branch was changed. Tests, qualification, provider calls and dispatch remain outside this pass.

Next slice: implement the plan-only workflow and strict task/state schemas on a dedicated branch. Keep the provider executor and schedule absent until the admission gates close.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
