# MediaHub OS — Contour A WB-09: Owner Direction, Hardware Baseline and Architecture Integrity Review

- Date: 2026-10-15
- Ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **OWNER-DIRECTION RECORDED / HARDWARE PROFILE PARTIAL / DOCUMENTARY INTEGRITY REVIEW PARTIAL / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED**
- Scope: record the owner's newly supplied machine inventory and authority intent; reconcile these directions with existing contracts; define an evidence-led, source-only architecture integrity review. No runtime, test, security scan, installation, provider/model call, credential use, deployment, merge or infrastructure action was performed.
- This is a new working checkpoint, not a normative replacement for Baseline 2.0 or for any accepted primary contract.

## 1. Owner-provided hardware facts

The following facts are supplied directly by the owner in the conversation on 2026-10-15. They are **owner-reported**, not independently inspected or hardware-qualified.

| Profile ID | Owner-reported machine | Reported CPU | Reported memory | Current architectural treatment |
|---|---|---|---|---|
| HW-MINI-2018 | Mac mini, 2018 | Intel Core i5, reported 6 cores | 32 GB RAM | Primary target candidate for the clean-slate Contour A design, subject to exact model/CPU, OS, storage, network and capability confirmation. |
| HW-MINI-SERVER-2011 | Existing Mac mini Server, 2011 | Intel Core i7; exact SKU/core count unknown | 16 GB RAM | Secondary/legacy physical candidate. It may be considered only as an optional non-critical node until exact OS support, security lifecycle, storage/network condition, and workload compatibility are established. Do not place it on the critical path based on RAM/CPU labels alone. |

These two assets are not evidence that previous installations succeeded. Historical failed installation state, host identity, installed packages, runtime configuration and deployment state remain excluded from the target baseline unless separately re-discovered and accepted through an authorized process.

### 1.1 Hardware and deployment facts still open

- Exact model identifiers, CPU SKUs, firmware/boot constraints and supported OS versions: **UNKNOWN**.
- Chosen OS and version/build, support/security-update window, architecture compatibility and Python/runtime versions: **UNKNOWN**.
- Internal/external storage devices, usable capacity, filesystem, encryption, backup target, restore objectives and media/data retention: **UNKNOWN**.
- Ethernet/Wi-Fi interfaces, link speeds, switch/router/VLAN/subnet, DNS, DHCP/static addressing, firewall, VPN/mesh, inbound exposure and segmentation: **UNKNOWN**.
- Compute workload envelope: concurrent agents, task rates, CPU/RAM budgets, local inference model/quantization, accelerator requirements, video workloads and thermal/power envelope: **UNKNOWN**.
- Which services are permitted on the 2011 node and whether that machine is a target asset rather than history-only equipment: **OWNER DIRECTION PARTIAL**. It is recorded as an optional candidate, not accepted for production/critical duties.
- The remote video server and any other previously discussed hardware are not automatically part of the target topology. Include only after owner-confirmed inventory and profile evidence.

**No deployment topology or service placement can yet be marked hardware-qualified.** The 2018 machine can anchor the design profile, but cannot be assigned a definitive workload until the remaining profile facts are supplied or explicitly accepted.

## 2. Owner direction: mission/task authority

The owner states:
1. The owner is the developer and may create tasks for Jarvis.
2. Jarvis may submit work to ASTRA A0 / request autonomous queueing.

For architectural consistency, this direction is recorded with the following narrow interpretation, preserving existing trust boundaries:

- **Human/developer → Jarvis:** the owner may create missions/tasks. The mission must carry stable identity, objective, acceptance criteria, scope and requested autonomy/risk class.
- **Jarvis → ASTRA A0:** Jarvis may submit a bounded, authenticated task/queue request through an accepted ingress contract. A request is not itself an authorization grant and must not be accepted merely because it came from Jarvis or is reachable over the network.
- **ASTRA A0:** A0 owns ASTRA-internal queue, admission, claim/lease, scheduling, retry/cancel, execution/evidence and recovery lifecycle within its accepted scope. Jarvis can request admission and observe/report results; it must not create a competing authoritative A0 queue or self-grant A0 capabilities.
- **Sensitive operations:** owner intent to create missions does not mean blanket approval for every sensitive action. Sensitive-operation approval must be represented by a verifiable attestation from an explicitly authorized approval authority, scoped to action/resource, task, audience, expiry and replay policy. A task file's self-declared `approval_state` is not, by itself, evidence of who approved it.
- **Delegation:** Jarvis-to-A0 delegation can only preserve or narrow authority; it cannot create new privileges. A0 must fail closed when identity, approval, capability, freshness, scope or provenance cannot be verified.
- **Product state:** neither Jarvis nor A0 becomes the canonical MediaHub Product State Authority. The existing product-state mutation boundary and Smart Home/Home Assistant Core authority remain unchanged.

This interpretation aligns with existing owner/security packet invariants. It does **not** resolve the existing DEC-DEV-02 primary-source wording conflict by itself, nor establish an implemented ingress.

## 3. Source-backed architecture consistency findings

### 3.1 Evidence currently available

1. WB-06 found a local typed `AuthorizationContext`/allow-list policy seam, but did not establish complete issuer provenance or connect that path to the separate HMAC command envelope.
2. WB-07 found distinct seams for JSON Task Contract ingress/gateway, typed authorization, and signed operational commands. The Task Contract path accepts file-supplied `approval_state` after shape/enum checks; the trusted inbox writer and approval attestation authority were not established.
3. WB-08 found source-level alignment between `.github/workflows/astra-autonomous-supervisor.yml`, `ops/control/sign_command.py`, and `astra_github_agent.py` around `mediahub.astra.control-command.v1`. This is static source evidence, not proof of successful runtime operation.
4. `tools/sign_astra_command.py` emits a different schema/key convention. Its active/canonical status remains unknown; do not delete or consolidate it based on search misses.
5. No tracked caller of `FileTaskIngress` was established in the bounded trace. This is a traceability gap, not proof of non-use in external/generated/deployment contexts.
6. The owner-decision packet and unified architecture contract preserve the distinction between ASTRA-internal lifecycle state and canonical MediaHub Product State Authority, but existing primary-source wording includes a documented conflict requiring governed reconciliation.

### 3.2 Integrity matrix

| Area | Current documentary status | Evidence needed to close | Current consequence |
|---|---|---|---|
| Hardware/OS/profile | PARTIAL / UNKNOWN | Exact model/SKU, OS/build/support lifecycle, storage/network facts and workload envelope | No hardware-specific service placement or deployment plan may be qualified. |
| Mission creation authority | OWNER DIRECTION RECORDED | Mission schema, identity/audit path, task-scope and risk-class rules | Human may create Jarvis missions; this does not imply unrestricted execution. |
| Jarvis → A0 ingress | NOT ESTABLISHED END-TO-END | Accepted schema/version, authenticated caller identity, issuer/consumer trust, audience, replay/idempotency, freshness, revocation, bounded payload and failure semantics | Dispatch must remain fail-closed; no assumption that an ingress is implemented. |
| Queue lifecycle | SPLIT BOUNDARY RECOMMENDED; DEC-DEV-02 CONFLICT STILL REQUIRES RECONCILIATION | One accepted lifecycle owner per domain, explicit adapter/delegation contract, ownership of queue vs mission state, retries/cancel/leases/fencing | Jarvis requests work; A0 owns its internal queue lifecycle. Avoid duplicate authority. |
| Sensitive-operation approval | OPEN | Approval authority, signed/verifiable attestation, subject/action/resource/task binding, expiry, revocation and audit | Do not trust a file's `approval_state` as approval proof. |
| Command signing | PARTIAL SOURCE ALIGNMENT | Canonical envelope/helper decision, key custody/rotation, node identity, verifier binding, replay/revocation and operational caller evidence | Keep both helpers; do not claim end-to-end security or runtime success. |
| Capability/AuthorizationContext | PARTIAL | Complete producer/serialization/transport/consumer trace; issuer provenance; audience; attenuation; expiry/revocation; policy enforcement | Routing labels are not security grants. |
| Queue/execution reliability | DESIGN REVIEW OPEN | Durable state semantics, atomic claim/lease/fencing, idempotency, bounded retries, dead-letter/manual review, cancellation and restart recovery | No claim of crash-safe autonomy until contract and qualification evidence exist. |
| Result/evidence integrity | DESIGN REVIEW OPEN | Result schema, target/source SHA binding, provenance, independent verification, immutable audit/evidence links and promotion gates | Agent assertions cannot self-promote work to verified/qualified/accepted. |
| Storage/backup/restore | UNKNOWN | Storage profile, encryption/access, retention, backup/restore, RPO/RTO, corruption handling | No persistence or recovery readiness claim. |
| Network/egress/isolation | UNKNOWN | Network zones, allowed ingress/egress, provider/data-class policy, secrets boundary, local-only fail-closed behavior | No silent cloud/provider fallback; no network-reachability trust. |
| Build/update/rollback | DESIGN ONLY / NOT VERIFIED | Reproducible package manifest, hashes/SBOM, provenance, migration policy, rollback/restore and recovery acceptance criteria | No installation or rollout authorization implied. |
| Observability/incident response | DESIGN REVIEW OPEN | Correlation IDs, audit events, clock source, redaction, log retention, alerting, incident containment and key revocation procedure | No operational readiness claim. |
| Branch/source provenance | DIVERGED | Governed reconciliation plan; source pin refresh; no implicit integration | Documentation-branch work is not in main unless integrated through an authorized process. |
| Contour A → Contour B | BINDING GATE | Deployment evidence, independent qualification, explicit owner acceptance with exact-SHA evidence | Product development in Contour B remains blocked until the gate is met. |

## 4. Architecture review procedure to finish independently

Proceed through the following source-only review packages without waiting for routine owner input. Any owner/governance decision that cannot be inferred safely remains an explicit blocker.

1. **Contract graph:** extract producer → schema → transport → consumer → state mutation for missions, Task Contract, command envelopes, AuthorizationContext, results and evidence. Pin source refs/blob SHAs and identify undocumented edges.
2. **Authority and trust graph:** reconcile principal identities, mission creator, task issuer, approval attester, capability issuer, verifier, A0 lifecycle owner, Product State Authority and external executor. Treat authentication, capability, authorization and trust as separate.
3. **Lifecycle/reliability graph:** check admission, queue ownership, atomic claim/lease, fencing, retries, idempotency, cancellation, timeout, worker loss, restart, duplicate delivery, partial results, stale results and recovery.
4. **Data/security graph:** classify data, secret/key flow, network/egress, local-only mode, provider fallback, log redaction, retention, revocation and incident containment.
5. **Hardware/profile graph:** map each requirement to HW-MINI-2018/HW-MINI-SERVER-2011 only after owner-supplied OS/storage/network facts; use explicit capability profiles rather than model-name assumptions.
6. **Build/deployment graph:** source revision → dependency lock/SBOM → reproducible artifact → signed manifest → staged installation → health gates → rollback/restore → observation → independent qualification/acceptance. This pass is design/evidence review only.
7. **Contradiction closure:** retain conflicting source clauses verbatim with refs and SHA; prepare bounded options and recommendation. Do not silently edit normative sources or claim that a proposal was accepted.
8. **Traceability sweep:** requirement → contract → component → failure control → verification method → qualification evidence → acceptance authority. Mark each item EVIDENCED, PARTIAL, UNKNOWN, CONFLICT, BLOCKED or ACCEPTED only with appropriate evidence.

## 5. Explicit non-claims and restrictions

- This is not a completed full-system verification. It is a documented source-level review pass plus a concrete plan for the remaining cross-domain closure.
- No tests, test suites, security scans, qualification, model/provider calls, installation, credential use, host/runtime inspection, infrastructure changes, deployment, migration, merge, rebase or cherry-pick were performed.
- The reported 2018/2011 hardware has not been independently inspected. No OS, storage, network, model or workload facts were inferred.
- No issuer, protocol, token format, key store, task schema or second signer disposition is selected by this checkpoint.
- No source change is made to accepted Baseline 2.0 or normative primary contracts. DEC-DEV identifiers and historical provenance are preserved.

## 6. Next bounded step

WB-10: complete the source-pinned contract graph for task/approval/command/capability/result paths and build the first cross-domain requirement → failure control → verification evidence matrix. Prioritize the Jarvis→A0 ingress edge and queue lifecycle conflict; continue independent source review while keeping all unproven runtime claims and hardware-specific deployment decisions gated.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
