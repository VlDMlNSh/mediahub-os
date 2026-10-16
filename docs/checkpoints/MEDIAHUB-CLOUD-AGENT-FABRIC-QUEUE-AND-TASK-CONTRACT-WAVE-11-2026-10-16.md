# MediaHub OS — Cloud-Agent Fabric Queue and Task Contract, Wave 11

- Date: 2026-10-16
- ID: MH-CAF-QC-11
- Status: **PROPOSED CONTRACT / DOCUMENTARY QUEUE / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Contour: A — Developer Fabric only
- Parent: [Reference Architecture, Wave 08](MEDIAHUB-AUTONOMOUS-CLOUD-AGENT-FABRIC-REFERENCE-ARCHITECTURE-WAVE-08-2026-10-16.md)
- Operational evidence: [Gemini Workflow Evidence, Wave 10](MEDIAHUB-CLOUD-AGENT-FABRIC-GEMINI-OPERATIONAL-EVIDENCE-WAVE-10-2026-10-16.md)
- Task schema: [Cloud-Agent Task Envelope Schema v0.1](MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.1-WAVE-11-2026-10-16.json)
- Documentary queue: [Cloud-Agent Activation Queue Wave 11](MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json)
- Navigation authority: [Project Map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## 1. Decision

Use one provider-neutral task envelope and one admission/queue authority for Contour A. GitHub remains the source/review/evidence plane. ASTRA A0 remains the owner of engineering-work admission, claim/lease, cancellation, recovery and evidence/gate lifecycle under its accepted internal contract. Jarvis remains the higher-level mission coordinator. MediaHub Product State Authority remains the sole authority for canonical product state.

The new JSON Schema and JSON queue are **reviewable proposal artifacts**, not a live queue or runtime API. They intentionally carry explicit references to the authority and policy evidence required for admission. Until the accepted A0 ingress/issuer/lifecycle contract and R-06 disposition are established, the schema cannot be treated as an implementation contract and queue entries cannot be dispatched autonomously.

## 2. Components added in this wave

| Component | Repository path | State |
|---|---|---|
| Task envelope JSON Schema | `docs/checkpoints/MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.1-WAVE-11-2026-10-16.json` | Created; proposal; runtime validation pending |
| Documentary activation queue | `docs/checkpoints/MEDIAHUB-CLOUD-AGENT-ACTIVATION-QUEUE-WAVE-11-2026-10-16.json` | Created; ten work items; no scheduler/dispatch semantics |
| Queue and contract decision record | This document | Created; proposed |
| Cross-domain traceability | Unified System Traceability Matrix | Updated in this wave |
| Plan of record | Master Development Roadmap | Updated in this wave |
| Canonical source/evidence index | Canonical Source Registry and Security Evidence Ledger | Updated in this wave |
| Navigation/checkpoint | Project Map and continuation checkpoint | Updated in this wave |

## 3. Task admission contract

A task may be considered dispatchable only when all conditions below have direct, revision-bound evidence:

1. **Identity and authority:** requester, issuer, target audience, capability scope, expiration and revocation semantics are bound to an accepted A0 contract.
2. **Immutable source:** repository, ref and resolved 40-character commit SHA are recorded before agent execution. Every selected input path is normalized and hashed.
3. **Scope:** explicit allowed paths, forbidden paths, output type and maximum changed-file count are present. Path globs cannot grant access to secrets, workflow authority or canonical product-state mutation.
4. **Data policy:** data class, purpose, egress policy, retention policy and destination-specific authorization are present. Unknown classification or destination blocks external transfer.
5. **Provider route:** each provider/model/fallback is individually authorized for this task, purpose and data class. Quota exhaustion can select only a preauthorized destination. Paid fallback remains disabled unless explicitly authorized by policy.
6. **Budget and retry:** attempt count, duration, input/output bounds, cost ceiling, retryable classes, backoff and idempotency key are bounded.
7. **Output quarantine:** model output, generated patches and artifacts remain untrusted. Initial worker classes are read-only audit, source review and documentation/design proposals. Any patch-capable worker requires a separate isolated-branch or draft-PR policy.
8. **Independent review:** required checks and review authority are explicit. The executor cannot qualify its own output. Automatic merge, direct main writes and product deployment are excluded from this contract.
9. **Evidence manifest:** run/job, source SHA, selected file digests, workflow/action revisions, agent/provider/model identity, policy revision, output/artifact digest, reviewer and final disposition are correlated.
10. **Terminal status:** accepted, rejected, running, cancelled, failed, indeterminate, completed, verified and qualified are distinct states. An ACK, artifact, provider HTTP 200 or successful run alone does not imply verification or acceptance.

## 4. Admission state machine proposal

```text
DRAFT
  -> STATICALLY_VALIDATED
  -> AUTHORITY_VALIDATED
  -> POLICY_AND_DESTINATION_VALIDATED
  -> QUEUED_BY_A0
  -> CLAIMED_WITH_LEASE
  -> EXECUTING_IN_ISOLATED_WORKER
  -> OUTPUT_QUARANTINED
  -> EVIDENCE_ASSEMBLED
  -> INDEPENDENT_REVIEW
  -> ACCEPTED_FOR_NEXT_GATE | REJECTED | FAILED | CANCELLED | RECONCILIATION_REQUIRED
```

This is a proposed logical state machine. It is subordinate to the accepted A0 lifecycle and must be reconciled against that source before implementation. A workflow must fail closed on missing authority, ambiguous admission, changed source SHA, policy mismatch, unknown provider, invalid manifest, lost lease or inconsistent terminal state.

## 5. Queue disposition

The machine-readable queue records CAF-Q-001…CAF-Q-010:

- **P0:** A0 issuer/ingress/lifecycle reconciliation; R-06 governance; Gemini workflow hardening proposal; task-envelope schema review.
- **P1:** evidence-manifest schema; agent registry/admission/revocation; target runner/workspace/network manifest; PR promotion and independent verification; provider adapter/quota/failover policy.
- **P2:** capacity, retry, cancellation and recovery policy.

The next independent source work is CAF-Q-003 and CAF-Q-007. CAF-Q-003 can produce a source-bound patch proposal for the existing Gemini read-only workflows; CAF-Q-007 can identify the canonical runner/workspace/network target. Both remain proposal/read-only work pending exact source and policy evidence. CAF-Q-001 and CAF-Q-002 remain blocking gates for a live queue.

## 6. Provider and agent admission policy

An existing agent or provider is registered from direct operational evidence and policy records, rather than name-only configuration. The successful Gemini run recorded in Wave 10 proves that one read-only audit execution completed; it does not automatically authorize all task classes, all input data, all models, write access or a general scheduler. Each agent registration must bind:

- stable agent/provider/model identity and exact capabilities;
- current source/workflow revision and action dependency identities;
- allowed task classes and data classes;
- allowed destinations and egress purpose;
- quota bucket, bounded concurrency and retry policy;
- output schema and artifact retention;
- authorization, expiry, revocation and evidence references;
- independent review requirements and promotion boundary.

When a new agent becomes authorized, the intended lifecycle is: collect its non-secret identity/capability evidence; review provider and data policy; create a narrow registry entry; issue a task-specific authorization; run only the admitted task class; verify the output; then widen scope through a separate reviewed change. This document creates that process contract as a proposal; it does not connect an agent automatically or create credentials.

## 7. Security and implementation notes

- GitHub's current Actions secure-use guidance recommends least-privilege permissions, auditing action source and pinning third-party actions to full commit SHAs; GitHub-hosted ephemeral runners reduce persistent cross-job contamination risk. See [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use).
- GitHub Copilot cloud-agent documentation describes asynchronous issue/prompt-driven work, branch/PR outputs and ephemeral execution. Availability depends on plan and repository configuration; it is a candidate integration path rather than a presumed free or already-enabled component. See [Kick off a task with Copilot agents](https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/kick-off-a-task) and [responsible use of agents](https://docs.github.com/en/copilot/responsible-use/agents).
- Preserve read-only advisory execution as a distinct worker class. Provider success and model output are evidence inputs, not security approval.
- Do not store tokens, credentials, raw secrets or private provider responses in task envelopes or public artifacts.
- Preserve the branch divergence and do not merge/rebase/cherry-pick as part of this wave.

## 8. Acceptance criteria

This proposal becomes implementation-ready only after:
- A0 issuer, ingress, queue, lease, cancellation and recovery contracts are accepted and revision-pinned;
- R-06 audit/privacy authority, schema, sink, outage and retention decisions are accepted;
- canonical component manifest and target runner/workspace/network manifest are reconciled;
- schema and queue IDs are collision-checked against canonical registries;
- workflow hardening changes are reviewed against exact source SHAs;
- independent security and qualification plans define required positive and negative-path evidence;
- separate authorization exists for implementation, workflow dispatch/provider calls, tests, qualification and deployment as applicable.

## 9. Evidence and status

Wave 10 records a successful historical Gemini read-only workflow run: run `38952885501`, source SHA `b45324009ac3aa65322a702c28069b12190bc4b8`, successful Gemini API step in job `117148417231`, artifact `12069128185`. That is valid operational evidence for that run. The broad fabric remains unqualified.

This wave added documentary schema/queue artifacts and updated project tracking. The schema has not been validated by a JSON Schema validator, the queue has no live scheduler, no agent was newly connected, and no workflow was dispatched or modified in this wave. No provider calls, credentials, tests/scanners, host/runtime inspection, infrastructure changes, qualification, deployment or branch integration occurred.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
