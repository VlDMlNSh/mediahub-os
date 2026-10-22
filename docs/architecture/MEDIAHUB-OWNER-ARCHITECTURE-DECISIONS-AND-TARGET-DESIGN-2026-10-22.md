# MediaHub OS — Owner Architecture Decisions and Consolidated Target Design

- Date: 2026-10-22
- Wave: 378
- Status: **OWNER-DIRECTED ARCHITECTURE RECORD / PROPOSED TARGET / IMPLEMENTATION, QUALIFICATION AND ACCEPTANCE NOT VERIFIED**
- Canonical documentation branch at authoring start: `docs/mediahub-chat-tree-map-20261012`, HEAD `937b6fa164d0e89e5e5781bf8c236e4fb862ad56`
- Main at authoring start: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- This record consolidates owner-discussed decisions. It does not override Functional Baseline 2.0, binding contracts, issuer/capability policy or the Product State Authority.

## 1. Target architecture and authority

MediaHub OS has two distinct contours:

- **Contour A — engineering fabric:** GitHub-centered ephemeral workers, bounded tasks, approved cloud model routes, secret isolation, independent verification and evidence.
- **Contour B — user/media compute:** user-owned nodes and local media services, admitted by explicit identity, consent, capability, resource quota, data-egress policy and revocation. Contour B must not enter production rollout until Contour A has been deployed and independently accepted.

Execution capacity is not authority. Keep task origin, task decomposition, execution/control-plane operations and canonical product-state mutation separate.

1. **ChatGPT / Jarvis** may receive or originate requests. Jarvis may route simple media tasks to an eligible media route and delegate complex engineering tasks to ASTRA GOLD A0.
2. **ASTRA GOLD A0** decomposes complex tasks into a dependency graph, selects eligible execution pools, assigns bounded subtasks, tracks lifecycle and assembles verified results.
3. **GitHub Supervisor / approved controller** provides only its qualified engineering control-plane capabilities: task records, dispatch, monitoring, lease/cancellation/recovery where implemented, and evidence collection. It does not replace A0 as decomposition authority.
4. **Model agents and workers** are untrusted executors/advisors. They cannot broaden scope, access unrelated data, issue credentials, merge to main or mutate canonical product state.
5. **MediaHub Product State Authority** remains the sole canonical product-state mutation authority. A successful worker run is not permission to commit product state.
6. **User-owned MediaHub nodes** provide only explicitly admitted capacity. Enrollment grants no unrestricted filesystem, credential, user-data or product-state access.

Never bypass issuer/capability, consent, lease, governance, budget, privacy or branch-protection controls. Technical possibility is not authorization.

## 2. Owner-confirmed decisions in this chat

### 2.1 Privacy — strict local-first

- User media and detailed local operational logs remain on the user's own nodes by default.
- Only explicitly authorized data and necessary, filtered engineering evidence may leave the local trust boundary.
- No implicit cloud fallback for media, logs or private prompts.
- Unknown data classification, missing policy, unknown recipient or missing authorization means deny external transfer.
- A task-specific exception binds purpose, source, recipient/provider/model, exact data classes or objects, operation, expiry, retention/deletion terms where available, budget and evidence.
- Revocation blocks new actions under that authorization; it cannot recall data already transferred.
- Hashes and metadata are not automatically non-sensitive.

### 2.2 Backups — encrypted copies on user-owned nodes

- Store encrypted backups only on explicitly approved user-owned nodes/media.
- Keep decryption keys separate from backup data; do not put a usable key in the same backup set.
- Verify archive integrity and periodically test restoration.
- Record source, time, format/version, integrity result and restore-test evidence without leaking private content.
- Creating a backup does not prove recoverability.
- Do not blindly replay restored queues. Re-check task authorization, lease/fencing, idempotency, previous outputs and current policy.

### 2.3 Updates — staged promotion with gates and rollback

- Stage updates and automatically check provenance and compatibility before activation.
- Required gates must pass before promotion.
- Activation is controlled and observable. Failed health/compatibility checks block promotion and trigger bounded rollback or quarantine.
- A signature/hash proves only particular provenance/integrity properties, not safety, compatibility or authorization.
- Irreversible schema/data migrations require a compatible backup/restore plan and explicit gate.
- Do not promote unverified artifacts or deploy to production merely because CI passed.

## 3. Data classification and egress

These proposed classes must be reconciled with existing binding contracts before implementation.

| Class | Examples | Default |
|---|---|---|
| D0 — public technical | Public source, documentation, specifications | Transfer subject to license and repository policy |
| D1 — internal technical | Internal configuration, non-sensitive diagnostics, engineering metadata | Restricted; approved route and purpose only |
| D2 — user/private content | Photos, video, audio, documents, private prompts, sensitive metadata and derivatives | Local-first; external processing requires task-level authorization |
| D3 — secrets/authority material | API keys, tokens, private keys, credential files, signing material | Never embed in model prompts, worker artifacts or general logs; use dedicated secret injection and least privilege |

Enforce classification at the data-selection/transmission boundary, not only in a prompt. Redact before external transfer. Ambiguous classification fails closed.

## 4. Task envelope and lifecycle

A bounded task should bind immutable task ID and target/source SHA or artifact digest; issuer and required capabilities; operation and allowed paths/resources; explicit prohibitions; data classes, egress policy and named recipient; dependencies; resource/cost/quota limits; expiry/lease; retry/idempotency and cancellation semantics; expected result and verification requirements; evidence manifest.

Reject expired, unsigned, out-of-scope or over-budget tasks. Duplicate delivery must not silently duplicate side effects.

Keep lifecycle/evidence states distinct: `PLANNED`, `AUTHORIZED`, `DISPATCHED`, `RUNNING`, `EXECUTED`, `VERIFIED`, `QUALIFIED`, `ACCEPTED`, `NOT RUN`, `BLOCKED`, `FAILED`, `NOT VERIFIED`. Execution is not verification; verification is not qualification; qualification is not acceptance. Missing evidence remains NOT VERIFIED, not PASS.

## 5. Queues, execution pools and network

- GitHub is the primary coordination/evidence path for engineering tasks, subject to real workflow, quota and governance limits.
- Media processing uses a separate local queue. Queue families may share task IDs, policy, lease/cancel/recovery semantics and evidence references without blindly mirroring private queue state.
- GitHub Actions is not an unlimited persistent dispatcher or guaranteed GPU platform. Runner GPU availability, provider availability, egress, quotas and costs must be verified.
- Approved outbound HTTPS is the default. Private networking may support explicitly permitted inter-node transfers, especially large media artifacts; private connectivity is not authorization.
- No public inbound listener by default. Route failure does not authorize proxy/VPN/region spoofing, an unapproved provider or paid fallback.
- During GitHub outage, local execution may continue only for tasks already fully authorized, within active lease and existing policy/resource limits; otherwise pause safely.

## 6. Model catalog, placement and loading

- Version-control model manifests, versions, checksums, licenses, compatibility and qualification metadata. Do not store large model weights in ordinary Git history by default.
- Git LFS/Packages or another store require checks for size, license, quota, cost, retention and access controls. Local replicas may exist on admitted nodes.
- Track distinct states: catalogued, downloaded, integrity-verified, compatible, loaded, active, qualified and retired.
- Replicate popular models to suitable nodes; keep heavy/rare models where capacity supports them. Consider license, RAM/VRAM, disk, latency, contention and data locality.
- Quantization differs from selective/streamed loading and offload. Combine only when supported; benchmark quality, memory and throughput on actual hardware.
- Do not assume hosted runners provide GPU inference or that a particular hosted model catalog is currently a usable inference service.

## 7. Resource management

Initial priority proposal:
1. **P0:** interactive Jarvis and latency-sensitive user-facing control.
2. **P1:** normal user tasks.
3. **P2:** background engineering and tests.
4. **P3:** batch work and maintenance.

Priority never overrides authorization, privacy, capability, cost/quota or safety. Candidate resource modes: `NORMAL`, `CONSTRAINED`, `PROTECTIVE`, with hysteresis. Observe queue age, latency, throughput, CPU/GPU, RAM/VRAM, model load/unload, cache pressure, errors, retries, disk headroom and provider quotas. Set numerical targets only after measuring actual hardware/workloads.

## 8. Recovery, idempotency and cancellation

Before retry or executor replacement, check current issuer/capability and expiry; lease/fencing and cancellation; existence and validation of prior results; idempotency/deduplication; compatibility and authorization of replacement executor; current egress, budget and resource policies.

Retry transient failures only within bounded policy. If side effects or result state are ambiguous, quarantine and reconcile rather than automatically replay. No paid fallback without explicit authorization.

Each recovery attempt should record task/attempt IDs, reason, source/target executor, lease state, previous result state, idempotency evidence, policy decision and disposition.

## 9. Observability and audit

- Detailed telemetry (CPU/GPU, RAM/VRAM, model loading, local queues, private media processing and sensitive diagnostic context) stays local by default.
- GitHub/approved artifact storage may hold the minimum engineering evidence: target SHA, workflow/run/job IDs, test/tool versions, artifact digests, sanitized outcomes and independent-review references.
- Shared identifiers link local and engineering events without copying private payloads to GitHub.
- Logs/metrics do not grant authority; absence of an event does not prove no action occurred.
- Use bounded local audit buffers with sequence/checksum protection, explicit retention/rotation and full-disk behavior. Reconcile conflicting task states before accepting output.
- Never emit secrets, raw private media or unredacted private prompts in summaries, logs, artifacts or worker reports.

## 10. Backup/restore and update gates

### Backup/restore
1. Select permitted data and destination.
2. Encrypt before persistence; keep keys separately.
3. Verify integrity and manifest consistency.
4. Periodically restore in isolated/quarantine environment.
5. Validate schema/version, ownership, authorization, task states and artifact hashes.
6. Reconcile active leases and idempotency before resuming queues.
7. Record outcome and losses. Do not claim qualification without a successful restore test.

### Update
1. Pin immutable source/artifact.
2. Verify publisher/provenance and digest.
3. Validate license, platform/runtime compatibility and policy.
4. Run static, contract, integration and relevant negative tests.
5. Stage candidate and run bounded health/compatibility checks.
6. Confirm backup/rollback path, including migration behavior.
7. Activate only after authorization and required gates.
8. Monitor, then accept under policy or rollback/quarantine.
9. Record old/new versions, target SHA, tests, approval, digest and rollback outcome.

Rollback is not a substitute for safe migration design.

## 11. User-owned nodes and hardware planning

Each node requires unique identity and explicit, revocable admission. Admission binds protocol/runtime compatibility, owner consent, CPU/RAM/VRAM/disk/bandwidth capabilities, allowed models/licenses, task resource budgets, egress policy and credential isolation.

Reported hardware from the discussion (not freshly hardware-verified here):
- Mac mini 2018: six CPU cores; RAM and current runtime inventory need verification.
- Mac mini 2011: four CPU cores, 16 GB RAM, clean Linux as reported.
- Future media server budget estimate: about 100,000 RUB. Ryzen 5 5600 / RTX 3060 12 GB / 32 GB RAM / 1 TB NVMe is a speculative proposal, not a final bill of materials or measured capacity.

Installer-managed disk quota must visibly bound model assets, caches and temporary data; it does not imply unbounded storage or automatic repartitioning.

## 12. Rollout and acceptance boundaries

1. Reconcile with Baseline 2.0, binding A0 issuer/task contracts and existing architecture records.
2. Close Contour A issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates.
3. Qualify approved controller: secret isolation, trigger paths, immutable target, cancellation/recovery and child-run evidence.
4. Validate schemas with standards-compliant JSON Schema Draft 2020-12, format assertions, positive/negative fixtures and semantic-reference checks.
5. Verify independent review and exact-head CI; absent/empty evidence is NOT VERIFIED.
6. Qualify local worker routes independently; never use the local server as Gemini transport.
7. Only after Contour A deployment and independent acceptance, begin Contour B admission/privacy/backup/update/runtime qualification.

No automatic merge to main, product deployment or canonical product-state mutation is authorized by this document.

## 13. Status ledger

### Explicitly selected by owner in this chat
- Strict local-first privacy with explicit external-transfer exceptions.
- Encrypted backups on user-owned nodes, separate keys, integrity checks and periodic restore tests.
- Staged updates with provenance/compatibility checks, mandatory gates, controlled activation and rollback.

### Consolidated design direction requiring contract reconciliation
- Authority split among Jarvis, ASTRA GOLD A0, GitHub Supervisor and Product State Authority.
- Separate engineering/local-media queues with shared bounded task semantics.
- Hybrid local/GitHub observability, adaptive resource policy and recovery/idempotency.
- Model registry/placement, user-node admission and two-contour rollout.

### Not implemented/proven
No runtime code, workflow, installer, model deployment, task dispatch, secret read, host command, benchmark, restore test, update activation, qualification or production rollout was performed by this documentation pass.

## 14. Related sources and overlapping work

- [Functional Baseline 2.0 — accepted canonical functional reference](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md)
- [Bootstrap instruction](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Canonical chat tree map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Canonical continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap 1.0](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301 — Contour A cloud-agent fabric](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #485 — user MediaHub compute and compact context state; open draft, not accepted](https://github.com/VlDMlNSh/mediahub-os/pull/485)
- [PR #474 — Wave 377 continuation context; open, not canonical](https://github.com/VlDMlNSh/mediahub-os/pull/474)
- [PR #441 — dispatch gate evidence; open and mergeability/CI must be rechecked](https://github.com/VlDMlNSh/mediahub-os/pull/441)

## 15. Architecture acceptance checklist

- [ ] Cross-check responsibility boundaries against binding A0 and Product State Authority contracts.
- [ ] Map D0–D3 to schema fields and enforce fail-closed egress in executable tests.
- [ ] Add positive/negative task-envelope fixtures for issuer, capability, lease, expiry, scope and budget.
- [ ] Prove backup key separation and successful restore in isolated test.
- [ ] Test staged update rejection, failed health gate, rollback and irreversible migration protection.
- [ ] Prove idempotent retry and ambiguous-result quarantine.
- [ ] Verify local telemetry redaction, bounded audit and full-disk handling.
- [ ] Reconcile model registry/resource quotas with actual node capabilities.
- [ ] Run exact-head CI and independent review; record run IDs, artifact digests and tool versions.
- [ ] Keep Contour B blocked until Contour A is deployed and independently accepted.
