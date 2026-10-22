# MediaHub OS — Consolidated Owner Architecture Decisions
**Wave:** 378 · **Date:** 2026-10-22  
**Status:** PROPOSED — owner-directed architecture consolidation; NOT IMPLEMENTED, NOT QUALIFIED, NOT ACCEPTED as runtime behavior.  
**Normative baseline:** Functional Baseline 2.0 remains the canonical immutable functional reference. This record supplements but does not supersede Baseline, security contracts, or governance.

## 1. Evidence boundary and repository reconciliation

Live read-only checks before drafting:
- `main` HEAD observed: `11d04d2f2687e9ba9215e4b67af2e450516960bb` — approved executor routing enforced and direct provider calls removed (#458).
- Canonical docs branch HEAD observed: `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`.
- Bootstrap blob `75f30750183efe8c6877368e9f0ada48f8e81ea7`; continuation checkpoint blob `89a8721f3509212b4e38e4d5bdd55560ba629fa9`; Master Roadmap blob `4b45b4bfeb5fcbf2dd409fb98241832283982c95`; canonical map blob `ba5731256321251b6a92b35d51f5bd0f2c1d4e86` (retrieved by SHA after the file wrapper returned empty content); Functional Baseline 2.0 blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the controlling Contour A workstream. It records CAF-Q-001…015 as documentary rather than a live scheduler; standards-compliant Draft 2020-12 schema validation, negative fixtures, independent review, semantic resolution, A0 issuer/ingress/lease/cancel/recovery, and R-06 audit/privacy gates remain open.
- PR #437 is merged. PR #474 was observed open/unmerged; PR #485 observed open/draft/unmerged and overlaps this owner-directed architecture.
- Controller workflow `.github/workflows/gemini-batch-dispatch-controller.yml` was read. Its existence is not proof of dispatch. Combined-status lookup for observed PR #474/#485 head SHAs returned no entries, so exact-head CI is NOT VERIFIED by that query. Branch-protection lookup returned 403, so protection is NOT VERIFIED.
- This pass did not dispatch Gemini, run Claude locally, invoke models, change runtime code, deploy, merge, or qualify/accept any runtime.

Sources: [Bootstrap](MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), [canonical map](MEDIAHUB-CHAT-TREE-MAP.md), [continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md), [Master Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md), [Baseline 2.0](../checkpoints/mediahub-functional-baseline-2.0.md), [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301), [PR #485](https://github.com/VlDMlNSh/mediahub-os/pull/485).

## 2. Contours and trust/authority boundaries

**Contour A — engineering fabric:** governed intake, decomposition, bounded dispatch, isolated execution, independent verification, provenance and explicit acceptance. Prefer GitHub-hosted ephemeral workers and approved outbound HTTPS when provider terms, quotas, data policy and egress permit. It should not require an owner-operated always-on server or public inbound listener. Documentation, schemas, historical successful runs, or a successful probe do not qualify a live fabric.

**Contour B — user-facing media runtime:** handles private media and product-facing work. Do not begin until Contour A is deployed and independently accepted.

Authority roles:
- **Owner/user:** supplies intent, approvals and explicit task-specific data-egress permissions.
- **Jarvis:** receives requests, routes simple permitted media tasks and escalates complex engineering to ASTRA GOLD A0; does not self-grant product-state authority.
- **ASTRA GOLD A0:** decomposes engineering requests, coordinates bounded subtasks and evaluates results; cannot bypass issuer/capability or governance gates.
- **GitHub Supervisor/controller:** manages engineering dispatch, queue/lease, cancellation, recovery, correlation and evidence; is not A0 and not product-state authority.
- **MediaHub Product State Authority:** sole canonical product-state mutation authority under existing contracts.
- **Model agents/workers:** untrusted executors/advisors; cannot self-issue capabilities, approve their own output, expose secrets, merge protected branches, deploy, or accept product state.

Technical capability is not permission. No authority mixing, issuer/capability bypass, automatic merge to main, direct deployment, broad write tokens, or secret exposure to model agents.

## 3. Queues, task envelope and lifecycle

Use separate authoritative queue domains: GitHub-backed engineering queue and local media queue. Share protocol and identifiers, not blindly mirrored mutable queue state. Task envelope should bind at least task ID, issuer, capability/policy reference, immutable input/source references, data class, requested outcome, executor constraints, quota/resource limits, lease/deadline, cancellation semantics, idempotency declaration, output manifest and evidence references.

Target lifecycle: `PLANNED → AUTHORIZED → DISPATCHED → RUNNING → EXECUTED → VERIFIED → QUALIFIED → ACCEPTED`. These states are distinct. Also represent `BLOCKED`, `NOT RUN`, `FAILED`, `CANCELLED`, and `NOT VERIFIED`. Missing status or evidence is never PASS. GitHub Actions is a bounded transport/ephemeral execution mechanism, not an unlimited persistent dispatcher.

## 4. Model catalog, artifacts and routing

Keep versioned catalog/manifests in GitHub and local replicas on eligible nodes. Track exact model revision, hash, license, source/provenance, runtime compatibility, resource envelope, capabilities, storage location and qualification status. Do not store large weights in ordinary Git history; consider LFS/packages only after evaluating size, license, quotas, cost, retention and access control.

Distinguish catalogued, downloaded/on-disk, loadable, loaded, active route, tested route and qualified route. Replicate popular models where useful; place heavy/rare models on capable nodes. Placement considers RAM/VRAM, disk, concurrency, latency, privacy and recovery. Presence in a registry does not prove a model is active or qualified.

Prefer approved provider APIs for permitted engineering tasks. Hosted runners have limits; do not assume GPU availability, fixed egress, free quota, regional access or unlimited capacity. No paid fallback without explicit owner authorization. No proxy/VPN/region spoofing to evade provider restrictions.

## 5. Adaptive resource control

Scheduling priorities are hints, never authorization overrides: P0 interactive Jarvis/user-facing; P1 normal user tasks; P2 background engineering; P3 batch/maintenance. Protect interactive responsiveness through admission control, bounded concurrency and reservations. Suggested modes: `NORMAL`, `CONSTRAINED`, `PROTECTIVE`, with hysteresis. Set no numeric thresholds until hardware and workload are measured.

Monitor CPU, RAM, GPU/VRAM, disk headroom, load/unload time, queue age, latency, throughput, retries/errors, cache, quota and cost. Resource priority cannot override safety, capabilities, data policy, consent or quota.

## 6. Recovery, retries and idempotency

Before retry/failover check lease/fencing, whether the prior attempt may still run, whether a validated result exists, idempotency/deduplication, replacement-executor compatibility/authorization/data eligibility, and quota/cost policy. Retry transient failures only under bounded policy. Ambiguous execution/result state goes to quarantine and reconciliation, not blind retry. No unauthorized paid fallback.

Record task/attempt IDs, reason, source/target executor, lease state, prior result state, idempotency evidence, policy decision, retry budget, final status and evidence links/digests. Restoring a queue never automatically authorizes old tasks to resume.

## 7. Hybrid observability

Detailed operational telemetry remains local on owner nodes: CPU/GPU, memory, local queue, model loading, media metrics, detailed logs and private content references. GitHub/approved artifact storage receives engineering evidence: immutable target SHA, workflow/run/job IDs, tool/runtime versions, test results, independent review, artifact digests and sanitized summaries. Correlate via stable IDs without uploading private media or detailed local logs.

Metrics are not proof of correctness; logs do not grant authority; missing telemetry does not prove no action. If GitHub is unavailable, local execution may continue only for tasks already fully authorized and still inside valid leases, quotas and active policies. Buffer audit events locally with monotonic sequence numbers and integrity checks; define retention, rotation, disk-full handling and reconciliation. Conflicts require reconciliation before accepting output.

## 8. Strict local-first privacy

User media and detailed local logs stay on owner-controlled nodes by default. External transfer is denied unless task-specific explicit auditable permission allows it. Unknown classification defaults to deny.

- **D0 public technical data:** transfer according to repository/license policy.
- **D1 internal technical data:** restricted to approved destinations and minimum necessary fields.
- **D2 user media/private content:** local-first; no external transfer without task-specific explicit owner permission.
- **D3 secrets, credentials, authority material:** never in model prompts, agent workspaces, ordinary logs or artifacts; use dedicated secret injection and least privilege.

Each egress boundary specifies purpose, source/recipient, exact data, issuer/capability/policy, required owner permission, expiry, size/rate limits, retention/deletion and audit evidence. Minimize/redact permitted transfers. Revocation blocks future actions but cannot recall already-transferred data.

## 9. Backups and disaster recovery

Back up to owner-controlled nodes with encryption, keys separate from backup storage, integrity checks and periodic restore drills. Separate backup sets for configuration, models/artifacts, user media, metadata/system state and audit records according to retention/privacy needs.

Restore to quarantine first. Verify checksums, key availability, source/timestamp, procedure version, configuration and model/runtime compatibility, metadata, queues/leases and audit integrity. Revalidate authorization, lease, idempotency and existing outputs before tasks resume. Ambiguous tasks remain quarantined. Record procedure version, source copy, tested data classes, integrity/key checks, observed recovery/data-loss window, defects and remediation. A successful backup job alone does not prove recoverability.

## 10. Staged updates, provenance and rollback

Separate discovery/download, provenance/signature/hash/license verification, compatibility/policy validation, isolated staging, automated contract/security/integration/regression gates, controlled activation, observation/rollback and evidence recording. Never promote an unverified version automatically. Hash/signature establishes identity/provenance only to the extent of its trust chain, not safety or compatibility. Rollback must account for data/schema migration, state compatibility, leases, model cache and credential revocation; never reintroduce revoked credentials.

## 11. Owned hardware assumptions (not verified inventory)

- Mac mini 2018: intended Jarvis/home coordination; RAM/storage/current capability still require measurement.
- Mac mini 2011: reported 16 GB RAM and clean Linux; candidate for background tasks, builds/tests and lightweight work.
- Future media server budget around 100,000 RUB; not finalized. Ryzen 5 5600 / RTX 3060 12 GB / 32 GB RAM / 1 TB NVMe was only a preliminary candidate.
Qualify hardware against measured workload before choosing model sizes/targets. Servers serve local compute; GitHub serves governed cloud engineering/routing. Never assume a host is reachable or authorized without verified host identity, capabilities, allowlist and policy.

## 12. Ordered acceptance gates

1. Close A0 issuer/ingress/lease/cancel/recovery and Product State Authority boundaries; close R-06 audit/privacy gates.
2. Approve D0–D3 classification, egress contract, secret isolation, retention/deletion and revocation.
3. Accept authoritative task/registry/evidence schemas; run standards-compliant JSON Schema Draft 2020-12 validation, format assertions, positive/negative fixtures, semantic resolution and compatibility checks.
4. Harden execution: immutable checkout SHA, strict ref/path/model allowlists, pinned actions, bounded permissions, runtime-only secret injection, dispatch correlation, cancellation and ambiguous-dispatch reconciliation.
5. Independently separate implementation, contract/test review, and security/authority/provenance audit. Never claim an agent was assigned without verified dispatch.
6. Test lease fencing, idempotency, bounded retries, restore drills, audit-buffer behavior and staged update/rollback.
7. Accept Contour A only with exact-SHA CI, independent review, artifact digests, run/job IDs, reproducible evidence and explicit governance/owner acceptance.
8. Begin Contour B only after Contour A deployment and independent acceptance.

Do not launch a blocked Gemini controller. Check exact secret/variable names against the workflow and contract; never rename or alias as a workaround. Gemini must use `.github/workflows/gemini-batch-dispatch-controller.yml`; record immutable target SHA, controller run ID, each child run/job ID, terminal statuses, reports, artifact digests, tests and independent verification. Missing evidence is NOT RUN/NOT VERIFIED. Claude Code is a separate task, allowed only on a confirmed third host with verified identity/capabilities/allowlist and a qualified permitted route with no paid fallback. That host is not Gemini transport. Browser work requires current agent-browser instructions and an availability check.

## 13. Current state and unresolved evidence

| Area | Evidence at this pass | Status / gate |
|---|---|---|
| Main code | HEAD observed at `11d04d2f...` | Refresh before execution |
| Canonical docs | HEAD observed at `937b6fa...` | This proposal is a working branch, not canonical |
| Baseline 2.0 | Accepted immutable reference | Preserve |
| CAF-Q-001…015 | Documentary queue | Live scheduler not established |
| Schemas | Prior 18/18 bounded read-back checks recorded in Issue #301 | Full Draft 2020-12 validation/negative fixtures/semantic review open |
| A0 and R-06 | Open in Issue #301 | BLOCKED pending required gates |
| Gemini batch | Not dispatched in this pass | NOT RUN |
| PR #474/#485 checks | Status lookup returned no entries | NOT VERIFIED |
| Branch protection | API returned 403 | NOT VERIFIED |
| Contour A | No acceptance established here | NOT QUALIFIED / NOT ACCEPTED |
| Contour B | Not started by this pass | BLOCKED until Contour A acceptance |

## 14. Owner-directed decisions consolidated

- Strict local-first privacy; private media stays local by default.
- Encrypted backups on owned nodes, separate keys, integrity checks, periodic restore drills.
- Staged updates with automated compatibility/provenance gates, controlled activation and rollback.
- Hybrid observability: local operational telemetry, sanitized engineering evidence in GitHub/approved artifact storage.
- Separate engineering/local-media queues with shared task protocol but no blind state mirroring.
- Adaptive model replication and resource control based on measured demand/hardware.
- Explicit separation of Jarvis, ASTRA GOLD A0, GitHub Supervisor, untrusted model workers and MediaHub Product State Authority.
- Contour B gated on Contour A deployment and independent acceptance.

These are architecture decisions/proposals, not runtime proof or blanket authorization for data transfer, paid inference, dispatch, host access, merge, deployment or product-state mutation.

## 15. Next bounded step

Review overlap with PR #485 and reconcile this proposal against normative contracts before merging. Then choose one bounded Issue #301 unit on one immutable SHA. First candidate: reproducible schema validation with positive/negative fixtures and digest-recorded tool/version evidence, only within the existing authority/privacy gates.
