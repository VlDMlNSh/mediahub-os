# MediaHub OS — Contour A WB-08 Caller Trace and Readiness Effort Estimate

- Date: 2026-10-15
- Status: **BOUNDED SOURCE TRACE / PLANNING ESTIMATE / NOT QUALIFIED / NOT ACCEPTED**
- Scope: read-only caller/reference trace for WB-07's ingress and signer paths; provide a planning estimate for a verifiable Contour A autonomous-development architecture ready for a controlled deployment decision.
- No code changes, tests, qualification, runtime execution, provider/model calls, credential use, infrastructure changes or deployment.

## 1. Caller/reference trace result

### 1.1 Confirmed caller for the node-specific command signer

- `.github/workflows/astra-autonomous-supervisor.yml`, blob SHA `a0209a2d01122354d19e95d2f362a6ecfa3d6186`, references `control/commands/**`, constructs `control/commands/mh-dev-01.json`, invokes `python3 ops/control/sign_command.py control/commands/mh-dev-01.json`, and later checks that the resulting signature is a 64-character string.
- `ops/control/sign_command.py`, blob SHA `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`, defines `mediahub.astra.control-command.v1`, canonical JSON body generation, node-specific HMAC key mapping, timestamp freshness validation, and file signing.
- `astra_github_agent.py`, blob SHA `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`, declares the same schema, canonicalizes command fields excluding signature, verifies HMAC and freshness, and reads `control/commands/{NODE_ID}.json`. This is strong source-level evidence that the workflow signer and agent verifier belong to the same operational-command format; it is not proof of successful end-to-end runtime operation.

### 1.2 Second signer helper

- `tools/sign_astra_command.py`, blob SHA `a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8`, emits `schema: 1` and signs with `ASTRA_COMMAND_HMAC_KEY`.
- The recursive `main` tree contains 799 entries with `truncated=false`. Direct source inspection of the tracked workflow/script candidates and GitHub code-search queries did not establish a caller or verifier for this helper.
- **Bounded conclusion:** its active/canonical status is unknown. Search misses are not proof of non-use. Do not delete, consolidate or rename it without a separate source-history and owner-approved disposition pass.

### 1.3 Task Contract ingress

- `runtime/mediahub_runtime/task_ingress.py`, blob SHA `59e1254aa61cc8f55f53bd1e179631e81c441393`, defines `FileTaskIngress`, parses `mediahub.ai.astra-task` version `1.0.0`, converts the file's `approval_state` into `AstraTaskRequest`, and passes requests to `AstraGatewayRuntime.run_bounded`.
- The 799-entry `main` tree has no separately named Task Contract schema file; the relevant source-level definition is embedded in the ingress module. This does not rule out an external or generated producer.
- No inspected workflow/script reference established a caller of `FileTaskIngress`. This is a bounded evidence gap, not proof that no caller exists in all deployment contexts.
- The file Task Contract path remains distinct from the signed operational-command path and from the P0 typed authorization path.

## 2. Effort estimate: Contour A architecture ready for controlled deployment

### 2.1 Define the deliverable precisely

The estimate targets a **complete, internally consistent, source-backed architecture package for Contour A** that is ready for an owner-authorized implementation/deployment plan. It includes defined component boundaries, contracts, trust and authorization flows, hardware/runtime assumptions, reproducible build and recovery design, observability, threat model, qualification plan, acceptance criteria, traceability, and unresolved owner decisions.

It does **not** mean that code is implemented, tests or qualification pass, hardware is provisioned, or the environment is deployed/accepted. Those require separate work and explicit authorization. New hardware facts remain UNKNOWN until provided or accepted by the owner.

### 2.2 Planning estimate

These are expert planning ranges, not measurements of completed work. They assume one focused bounded pass per work package, direct repository evidence, documentation synchronization after each material pass, no large new architecture decision, and no substantial rewrite of existing code.

| Work package | Estimated active assistant/repository hours |
|---|---:|
| A. Repository/branch reconciliation, source provenance, baseline and legacy-vs-target classification | 4–8 |
| B. Contour A scope, component inventory, responsibility and dependency graph | 4–7 |
| C. Jarvis/Astra/autonomous-controller orchestration and lifecycle contracts | 6–10 |
| D. Task ingress, command envelopes, identity, authorization, approval provenance, secret/key boundaries | 6–10 |
| E. Execution adapters, queues, state/persistence, scheduling, retries, idempotency, recovery | 5–9 |
| F. New-hardware topology, local/hybrid provider boundary, resource and network assumptions (after owner supplies facts) | 4–8 |
| G. Threat model, failure modes, observability, audit trail, containment and recovery | 4–7 |
| H. Reproducible build/package/installation and rollback architecture (design only) | 4–7 |
| I. Architecture consistency sweep, contract/requirement traceability, conflict resolution proposals | 5–9 |
| J. Deployment-readiness dossier, qualification matrix, acceptance gates, evidence index and handoff | 4–7 |
| **Gross total before overlap/unknowns** | **46–82 hours** |
| Contingency for unresolved decisions, source gaps and rework (20–30%) | **9–25 hours** |
| **Working planning range** | **55–107 focused hours** |

Recommended planning point: **about 75–85 active hours** for the architecture package, if owner decisions and new-hardware facts arrive promptly and source discovery does not reveal a major design reset. Use **55–110 hours** as the honest current range. This is not a promise or a completion guarantee.

### 2.3 What that means in this chat

The estimate counts active bounded analysis/documentation time, not elapsed time between messages.

- At 2 active hours/day: about 28–55 working days.
- At 4 active hours/day: about 14–28 working days.
- At 6 active hours/day: about 9–19 working days.

These conversions are arithmetic scenarios, not a forecast of ChatGPT availability or response latency. The current chat has already accumulated substantial prior work; the repository does not expose a reliable time ledger for those earlier sessions, so a defensible total-project remaining-hours calculation cannot be obtained by subtracting guessed past hours. The range above is a forward estimate from the current observed architecture gaps, and it may move after broader reconciliation.

### 2.4 Separate work that is outside the estimate

After architecture readiness, actual deployment and independent acceptance are separate stages. Depending on hardware access and owner permissions, allow an additional provisional **20–50+ active hours** for implementation closure, packaging, authorized qualification, controlled deployment, operational observation, remediation and independent acceptance. This is a deliberately broad, separate planning placeholder; it is not included in the 55–107 architecture hours and must be recalculated after target hardware and the deployment model are known.

No tests, qualification or deployment were performed in this pass. The project's guardrails still prohibit these actions without explicit authorization.

## 3. Main schedule risks

1. Hardware, OS, network, storage, compute and model/provider target remain unspecified/UNKNOWN.
2. The exact authority and approval provenance for Task Contract ingress remain undecided.
3. The second signer helper's disposition is unknown.
4. The end-to-end Jarvis→ASTRA A0 issuer/verifier path is not established.
5. Branches remain diverged; do not treat documentation-branch commits as integrated into `main`.
6. The estimate assumes the goal is Contour A architecture readiness, not a finished product in Contour B.

## 4. Recommended next steps

1. Continue source-only tracing of Task Contract producer/call sites, workflows and any documented external ingress.
2. Prepare an explicit owner-decision record for: trusted inbox writer, approval attestation authority, canonical command schema/helper, trust-domain separation, and approved Jarvis→A0 ingress.
3. Inventory the remaining Contour A work packages against the master roadmap and classify each as evidenced/partial/unknown/blocked.
4. Only after the owner supplies or accepts new-hardware facts, finalize deployment topology and reproducibility constraints.
5. Keep design readiness, implementation, verification, qualification, deployment and independent acceptance as separate status gates.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
