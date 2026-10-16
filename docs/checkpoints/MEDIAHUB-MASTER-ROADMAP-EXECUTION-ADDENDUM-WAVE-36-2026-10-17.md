# MediaHub Master Roadmap — Existing Agent Registry and Admission Reconciliation, Wave 36

- Date: 2026-10-17
- Parent plan: docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Wave 35 architecture: docs/checkpoints/MEDIAHUB-CLOUD-AGENT-AUTONOMOUS-QUEUE-REFERENCE-ARCHITECTURE-WAVE-35-2026-10-17.md
- Wave 36 source reconciliation: docs/checkpoints/MEDIAHUB-EXISTING-AGENT-REGISTRY-A0-ADMISSION-AND-EGRESS-RECONCILIATION-WAVE-36-2026-10-17.md
- Status: **EXECUTION-ORDER ADDENDUM / PROPOSED / ADMISSION AND MULTI-RUNNER IMPLEMENTATION GATED**

## Source-bound correction to the component plan

Current main already contains:
- `profiles/agent-registry.json` v1.2.0;
- `.github/agent-system/registry.yaml` role registry;
- provider-registry and provider-adapter JSON Schemas;
- an A0-owned 23-lane queue manifest;
- local Agent Fabric claim/lease primitives;
- canonical ASTRA governance and G0–G11 qualification schemas.

Therefore this plan must extend and validate existing catalogs/contracts rather than introduce a parallel registry or task lifecycle.

## Revised work sequence

| Step | Work item | Deliverable | Go/no-go |
|---|---|---|---|
| W36-A | Reconcile existing registries and control boundaries | Source-bound packet W36 with exact refs/SHA | Completed as documentary reconciliation |
| W36-B | Define admission schema compatible with current agent catalog | Proposed JSON Schema and sanitized fixtures on isolated feature branch | Only schema-level behavior; no provider enabled by implication |
| W36-C | Define catalog validator and drift report | Offline validator for existing agent catalog, role registry, provider schema and queue manifest | No secrets, network calls, provider selection or workflow dispatch |
| W36-D | Validate on a bounded feature branch | Schema/contract tests at an immutable candidate SHA | Requires safe workflow path review and isolated test environment; no merge |
| W37-A | Reconcile A0 trusted issuer/ingress and task authorization envelope | Accepted primary-source crosswalk and open-decision list | Write-capable admission stays blocked until authority is explicit |
| W37-B | Close R-06 privacy/audit policy route and MH-12 secret-store ADR | Governance decision and evidence | Current R-06 route remains OPEN; no invented approval authority |
| W37-C | Compare existing persistence/queue options for atomic cross-runner leases | Component gap matrix and exact protocol proposal | No second scheduler/database without an accepted demonstrated gap |
| W38 | Implement task-to-agent binding, destination gate and lease/fencing only after accepted source contracts | Minimal code diff and independent review | Single-writer or read-only mode until shared claim authority is proven |
| W39 | Synthetic read-only hosted-runner qualification | Run ID, exact SHA, sanitized evidence artifact, cancellation/recovery evidence | No provider credentials exposed to worker |
| W40 | One provider/agent admission | Route-specific auth and non-mutating probe evidence after explicit task authorization | One account/project/model/data class/destination per admission record |
| W41 | Patch-worker enablement and lane-by-lane concurrency | Independent verification, path/diff guard, retry/cancel/revoke evidence | PR-only output; no automatic merge, release or deployment |
| W42 | Fresh integrated qualification and soak | G0–G11 evidence at one frozen SHA | Human launch authorization remains mandatory |

## Current blockers that control the order

1. A0 D2 trusted authorization-context issuer/ingress remains a proposal rather than an accepted implementation contract.
2. R-06 audit/privacy governance has no established accountable approval path in the reviewed records and its disposition template remains unfilled.
3. MH-12 mandates credential lifecycle and secret exclusion; exact secret store remains non-canonical pending evidence and an ADR.
4. Existing local ClaimStore uses filesystem-local locking; cross-runner atomic leases and cancellation/recovery remain unproven.
5. The component-selection manifest exists, but the inspected source set has not established one accepted deployment target manifest with the selected host/service/OS/network/secret/health/recovery details.
6. Current generated qualification truth remains G0–G11 BLOCKED / overall NOT_PROVEN / BLOCKED.

## Server-independent provider access

The architecture may run an authorized hosted workflow without a user-operated always-on server. Where supported, use GitHub OIDC/workload identity with a narrowly bound trust relationship; where the provider requires an API key, use a scoped service-managed secret reference. A secret reference is host-independent, but the provider still sees the actual request's network origin and may evaluate IP/region or account eligibility. The work sequence shall select permitted execution geography rather than assume location-blind requests.

## Scope of this update

This is a roadmap addendum and status correction only. The main roadmap and canonical component manifest remain unchanged. No provider/model call, credential access, host/runtime inspection, infrastructure change, test, qualification, deployment or branch integration occurred during this source reconciliation.
