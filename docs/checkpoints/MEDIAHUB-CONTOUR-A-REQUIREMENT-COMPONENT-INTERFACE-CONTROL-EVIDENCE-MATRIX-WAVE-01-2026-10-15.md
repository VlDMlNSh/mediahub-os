# MediaHub OS — Contour A Requirement / Component / Interface / Control / Evidence Matrix, Wave 01

- Date: 2026-10-15
- Status: SOURCE-BOUND DESIGN MATRIX / CANDIDATES ONLY / NOT NORMATIVE / NO COMPONENT ADMITTED / NOT IMPLEMENTED OR QUALIFIED
- Scope: greenfield Contour A — Jarvis, ASTRA A0/Astra Gold, admitted autonomous controllers and local/external executors. Contour B product development remains gated until Contour A deployment and independent acceptance.
- Source boundary: uses current repository documentation and source anchors; no live host inventory, installation, test, provider call or upstream release audit was performed.
- Owner direction: new hardware and a new verifiable system. Prior old-server installations/routes are historical and are not target configuration.

## 1. Admission rule

A capability requirement is not a component selection. A component candidate is not an admitted component. Repository presence, README text, manifest status or a previous failed installation does not prove target compatibility, implementation, qualification or acceptance.

For each candidate, admission requires: a concrete capability gap; authoritative upstream repository and immutable release/commit; license and provenance; dependency/SBOM and vulnerability review; target OS/hardware/resource fit; security/isolation/egress review; explicit interface and authority fit; recovery/rollback; source-bound acceptance criteria; independent qualification evidence; and any required owner/governance decision. This matrix does not grant permission to perform those activities.

## 2. Authority and hard constraints

| Constraint | Required design/control | Evidence required before admission or execution |
|---|---|---|
| Jarvis corporation coordination | Jarvis plans missions, selects only permitted routes/executors, tracks mission results; no direct ASTRA queue writes | Accepted mission ingress and route-selection contracts; source/target revision-bound audit |
| ASTRA engineering lifecycle | A0 is sole writer for ASTRA queue/claim/lease/heartbeat/retry/cancel/recovery and ASTRA evidence/gates within accepted scope | Accepted A0 API; lease/fencing and publisher contract; independent gate evidence |
| Product State Authority | Sole canonical Contour B product-state mutator | Accepted primary state contract and separate Contour B authorization; no inferred authority |
| Identity/capability | Explicit principal, issuer, audience, operation/resource/scope, constraints, provenance, lifetime, revocation and audit; fail closed | Accepted issuer/attester and verifier contract, replay handling, rotation/revocation evidence |
| Routing/egress | Distinguish executor, controller, gateway, provider, model and transport identities; LOCAL_ONLY never silently falls back to cloud | Versioned route policy, route decision evidence, provider/egress identity and denial tests after authorization |
| Evidence and promotion | Separate design, implementation, test, verification, qualification, release, deployment and acceptance | Immutable artifact digests, target SHA, policy/schema revisions, independent verifier identity and disposition |
| Greenfield topology | Target-specific component placement and trust boundaries, not copied old node IDs | Owner-confirmed hardware/OS/network/workspace inventory and compatibility evidence |

## 3. Requirement → candidate → interface → control → evidence matrix

| Requirement ID | Required capability | Candidate/component family already evidenced in repository | Required interface seam | Mandatory control | Evidence/gate | Current disposition |
|---|---|---|---|---|---|---|
| CA-R01 | Corporation mission coordination | Jarvis Control Plane (owner-directed target role; implementation not proven) | Request intake → mission envelope → route decision → mission status/result | No direct A0 internal-state writes; bounded mission and explicit policy revision | Accepted request/mission schema, route-decision record, owner-approved authority trace | REQUIREMENT ACCEPTED AS DIRECTION / IMPLEMENTATION OPEN |
| CA-R02 | ASTRA engineering workflow lifecycle | ASTRA GOLD / A0 (existing source contracts; target deployment unproven) | Jarvis → accepted A0 ingress; A0 → claim/lease → executor; executor → A0 publication | A0 sole internal queue writer; same-target-SHA dependencies; fencing, stale-lease rejection, bounded retry/recovery | Accepted ingress and result API, lease/fencing semantics, independent gate evidence | CRITICAL BLOCKER: NO ACCEPTED JARVIS→A0 API |
| CA-R03 | Authenticated, least-privilege delegation | MH-12 security architecture defines semantics; no concrete issuer implementation selected | Identity provider/issuer → capability verifier → consumer boundary | No self-issuance; no privilege expansion; bind audience/scope/target/lifetime/revocation; fail closed | Accepted issuer authority, signed/attested representation, expiry/revocation/replay/audit contract | CRITICAL BLOCKER: ISSUER/VERIFIER LIFECYCLE OPEN |
| CA-R04 | Bounded autonomous coding worker | OpenHands Software Agent SDK is a research candidate in admission crosswalk; not manifest-admitted | A0/approved dispatcher → isolated worker adapter → patch/artifact + provenance → verifier | Isolated pinned workspace, short-lived scoped capability, no self-merge/release/state mutation, resource limits | Immutable upstream pin, license/SBOM, sandbox/egress evidence, artifact digest, independent review | RESEARCH CANDIDATE ONLY; GAP JUSTIFICATION AND DUE DILIGENCE REQUIRED |
| CA-R05 | Specialist-agent workflow composition | LangGraph and Microsoft Agent Framework are screened alternatives, not selected | Jarvis or worker adapter → bounded graph/runtime → typed tool/task interfaces | Select one only after overlap assessment; no duplicate mission or ASTRA authority; per-tool authorization | Immutable release pin, persistence/recovery semantics, tool isolation, contract compatibility, comparative rationale | ALTERNATIVES; NO SELECTION |
| CA-R06 | Durable long-running workflow, if a gap exists outside A0 | Temporal Python SDK is a screened candidate; overlaps ASTRA lifecycle | Explicitly bounded non-ASTRA workflow API → workflow service/worker | Do not add a second authority for ASTRA queue/lease/gates; require documented use case and service ownership | Gap statement, self-host/resource model, deterministic execution fit, recovery and rollback evidence | FUTURE CANDIDATE; NO JUSTIFIED ADMISSION YET |
| CA-R07 | Bounded tool/resource interface | MCP Python SDK is a screened interface candidate | Approved client → identified tool server → schema-validated tool/resource | Protocol is not authorization; explicit server identity, per-tool capability, audit and egress policy | Versioned protocol pin, server identity, tool allowlist, validation/isolation and negative-path evidence | INTERFACE CANDIDATE; NOT SELECTED |
| CA-R08 | Policy evaluation/enforcement | Open Policy Agent is a policy-fit candidate, not a selected authority | Policy input/context → decision point → enforcing boundary | Policy engine cannot grant itself authority or become product-state authority; unavailable/ambiguous policy fails closed | Policy ownership/version distribution, input provenance, enforcement coverage, denial-path evidence | CANDIDATE; SECURITY/ARCHITECTURE REVIEW REQUIRED |
| CA-R09 | Local-first telemetry and audit | OpenTelemetry Collector is an observability candidate, not admitted | Bounded component telemetry → local collection/filtering → approved sink | Sensitive-data filtering, local retention defaults, no unapproved external egress; telemetry alone is not qualification | Pinned version, data classification, retention/export policy, resource fit, trace-to-artifact linkage | CANDIDATE; PRIVACY/EGRESS GATE OPEN |
| CA-R10 | Local inference route | ONNX Runtime and llama.cpp are target-gated in the canonical component set; “Alamo” is a target endpoint label, not proof of a selected runtime | Jarvis route selector → Alamo endpoint/adapter → identified runtime/model | Local-only fail closed; exact model/runtime identity; no inference schema repurposed as mission DAG | Owner-approved hardware profile, runtime/API/model digest/license, tool-call compatibility, route/egress evidence | TARGET-GATED; HARDWARE/IDENTITY EVIDENCE OPEN |
| CA-R11 | External cloud controller as one bounded executor | External controller/ECC is owner-directed as a possible executor-side arrangement; ECC itself NOT ASSESSED/NOT ADOPTED | MediaHub adapter → external executor contract → untrusted result/artifacts | MediaHub does not manage external internal queue/secrets; no access to A0 internals or Product State Authority | Upstream pin/license/security review, API/auth contract, data-egress/retention terms, isolated execution and result verification | DESIGN DIRECTION; COMPONENT NOT ADMITTED |
| CA-R12 | Mission/task/result/evidence interoperability | Corporation mission/task/result schemas Draft 01; existing inference and component-evidence schemas remain narrower domains | Mission/DAG/result/evidence envelope → A0/worker/verifier adapters | Unique IDs and explicit version policy; never repurpose inference schema IDs; no secret material; digest-bound provenance | Accepted namespace/version policy, producer-consumer trace, schema compatibility and independent verifier | DRAFT ONLY; NOT A WIRE CONTRACT |
| CA-R13 | Greenfield hardware placement | Mac Pro, Mac mini/server and remote video server are owner-directed target nodes; exact models/OS/resources not yet pinned in reviewed evidence | Role placement → network/trust boundary → local/remote worker admission | Do not import old hostnames, users, paths, model tags, runner labels or service identities | Owner-provided inventory, connectivity/trust map, OS support and capacity evidence | TARGET REQUIREMENT; INVENTORY OPEN |
| CA-R14 | Recovery, backup and artifact durability | restic is target-gated backup/restore candidate; existing ASTRA recovery semantics remain authoritative within A0 | Artifact/evidence store → backup/restore boundary → verifier | Recovery must reconcile authoritative persisted state; do not infer lease or mission authority from worker memory | Restore evidence, encryption/retention, consistency and rollback criteria; no promotion from candidate label | TARGET-GATED CANDIDATE; STORAGE/RECOVERY DESIGN OPEN |
| CA-R15 | Component provenance and admission ledger | Canonical Manifest 2.0, machine-readable component manifest, unified candidate register and admission crosswalk | Upstream source/release → pinned component record → SBOM/license/security gate → target qualification | Do not infer that omission is approval or defect; reconcile manifest scope before adding rows | Immutable source pin, manifest crosswalk, SBOM, license, vulnerability and owner/governance evidence | PROCESS INPUTS EXIST; SCOPE RECONCILIATION OPEN |

## 4. Historical artifacts and non-inheritance rule

The Greenfield / Legacy Artifact Ledger classifies old-node-specific routing YAML, node-role maps, worker scripts, runner workflows, command workflows and host-bound service definitions as LEGACY-OPERATIONAL or SHARED-OR-UNKNOWN. They are not target configuration. They must not be deleted en masse: reverse-reference, historical-ID and shared-contract impact must first be established. Generic policy semantics may be reconsidered only as a separately source-backed requirement; old endpoint, hostname, credential, route, service label or model tag is never inherited by default.

Previously failed installation attempts are historical evidence only. They are not evidence that a candidate is installed, compatible, selected or qualified on new hardware.

## 5. Gate order and blockers

1. **G-A: Owner target inventory** — exact node models, OS versions, RAM/storage/network/accelerator, roles and trust boundaries.
2. **G-B: Contract/authority closure** — accepted Jarvis→A0 ingress; capability issuer/verifier lifecycle; fencing and authoritative result publication; authority wording reconciliation through controlled change.
3. **G-C: Candidate justification** — each capability gap linked to a candidate and alternatives; no duplicate queue/state/policy authority.
4. **G-D: Provenance and compatibility** — immutable upstream version, license, SBOM, dependency/security review, target OS/resource fit.
5. **G-E: Interface and isolation** — explicit schemas, auth, tool allowlists, workspace isolation, egress/local-only semantics, cancellation/recovery.
6. **G-F: Independent qualification** — authorized, source-bound test and evidence plan, separate reviewer and immutable results.
7. **G-G: Contour A deployment and independent acceptance** — required before autonomous Contour B product development; not reached in this document.

Current hard blockers: G-A inventory open; G-B ingress/issuer/fencing/publication unresolved; G-C candidate admission not authorized; G-D through G-F not performed; G-G not reached.

## 6. Source anchors

- Unified Component Candidate & Evaluation Register, docs branch blob `76e22a2db90e4a45f41428f97b848a39884329af`: broad candidate set and status vocabulary; explicitly not an admission or test authorization.
- Greenfield / Legacy Artifact Ledger, docs branch blob `f97d44567328633602cdc2ca52bcd0b20138e082`: old-node artifacts are historical/legacy or shared-unknown; no blanket deletion.
- Jarvis / ASTRA Distributed AI Corporation Target Architecture, docs branch blob `c9f1716de8419d66f181fc0a9c465c65a81c7d5b`: owner-directed authority split and external-controller boundary; design only.
- Mature Component Candidate Screen, docs branch blob `e20570b6f61fed2fb1232cbeb84286ce2e8dca1d`: LangGraph, Temporal, Microsoft Agent Framework, MCP SDK, OPA, OpenTelemetry Collector and A2A are candidate-only; README blob SHAs are not upstream commit pins.
- Component Admission Crosswalk, docs branch blob `e5be83f63e974c6eb559515c6371a93ae36b1f2b`: manifest scope/selection and candidate gates; no component admitted.
- Owner Decisions and Corporation Direction, docs branch blob `70376a2709e055972ceddc4a280d26992977213c`: Jarvis/A0/Product State Authority boundaries and no inherited runtime status.
- Wave 10 interface trace: [Contour A Control-Plane Interface Edge Trace, Wave 10](MEDIAHUB-CONTOUR-A-CONTROL-PLANE-INTERFACE-EDGE-TRACE-WAVE-10-2026-10-15.md): ten source-bound seams; E-02/E-05/E-07 remain blocked.

## 7. Result and next bounded step

This matrix turns the current source-backed target direction into explicit requirements and evidence gates without selecting a component, inventing an API, deleting legacy artifacts or authorizing installation. No candidate is admitted. The next safe step is a statement-level controlled reconciliation proposal for conflicting ASTRA authority wording, while owner input is required for target hardware inventory and governance acceptance is required for ingress/issuer/fencing/publication contracts.

No tests, installations, model/provider calls, credentials, host/runtime inspection, security scan, qualification, infrastructure change, deployment, merge, rebase or cherry-pick occurred.
