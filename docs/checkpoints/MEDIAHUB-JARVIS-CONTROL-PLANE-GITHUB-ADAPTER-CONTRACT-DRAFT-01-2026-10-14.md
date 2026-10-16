# MediaHub OS — Jarvis Control Plane and GitHub Adapter Contract, Draft 01

- Date: 2026-10-14
- Status: **DESIGN DRAFT / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED**
- Scope: Jarvis engineering control plane, mission submission to A0-ASTRA, GitHub access, per-task executor/provider routing, evidence and lifecycle gates.
- Governing baseline: accepted Functional Baseline 2.0. Baseline 1.0 remains historical unless a specific change is accepted.
- Related evidence: [Wave 02 unified local inventory](MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md); [partial PASS ledger and portable profiles](MEDIAHUB-PARTIAL-PASS-EVIDENCE-AND-PORTABLE-DEPLOYMENT-PROFILES-WAVE-01-2026-10-14.md); [unified deployment contract v0.1](mediahub-unified-architecture-and-deployment-contract-v0.1.md); [unified traceability matrix v0.1](mediahub-unified-system-traceability-matrix-v0.1.md).

## 1. Intent and non-goals

Define one verifiable contract between Jarvis, ASTRA, GitHub, execution routes and evidence records. This document is a proposed bridge across existing domain contracts; it does not supersede them, grant permissions, or assert that any component is deployed.

This draft does not authorize installation, tests, qualification, model/provider invocation, credential access, host/runtime inspection, infrastructure changes, deployment, merge, release, production mutation, migration or governance bypass.

## 2. Authority boundaries

| Authority / actor | May do within an accepted policy | Must not do by implication |
|---|---|---|
| Jarvis Control Plane | Normalize a request into a bounded engineering mission; choose an eligible executor route; submit mission through the documented A0-ASTRA interface; track returned status/evidence | Directly mutate ASTRA internal queue/claim/lease/gate state; mutate canonical product state; widen permissions or approve its own output |
| ASTRA A0 / queue authority | Sole writer for ASTRA-internal queue, claim, lease, heartbeat, retry/cancellation and gate transitions according to ASTRA's own accepted contract | Become MediaHub Product State Authority; treat Jarvis/GitHub as an alternate queue-state writer |
| MediaHub Product State Authority | Sole canonical product-state mutation authority, as defined by its primary contract | Delegate canonical mutation to Jarvis, ASTRA, model, provider or GitHub adapter by inference |
| GitHub Adapter | Read permitted refs/files/status; create a narrowly authorized branch/commit/PR or update explicitly allowlisted documentation paths only when capability is granted | Merge, release, deploy, alter protected governance, change workflow permissions/secrets, bypass review, or write outside granted paths |
| Executor (Claude Code, Codex, local worker, other admitted tool) | Perform one bounded mission inside a pinned isolated workspace with declared capabilities | Select its own authority, bypass route policy, read secrets outside scope, change target SHA or promote its own result to PASS |
| Independent reviewer / A3 | Verify output against mission, target SHA, contract and evidence; record independent disposition | Review its own output as the sole reviewer where policy requires independence |

The exact A0-ASTRA API, authentication, issuer and queue-state interfaces must be sourced from the accepted ASTRA contract before implementation. This draft intentionally does not invent an endpoint, signature, queue schema or authorization mechanism.

## 3. Mission envelope (proposed logical fields)

A submitted mission must bind at minimum:

- stable `mission_id`, idempotency key and schema revision;
- request origin, authenticated principal and granted capability reference;
- mission class, objective, bounded scope, explicit exclusions and expected artifacts;
- immutable repository/ref/target SHA and allowlisted paths;
- data classification, egress class and eligible executor/provider set;
- budget/time/token/resource ceiling and cancellation/deadline policy;
- workspace/worktree identity, lease owner and lease expiry when applicable;
- acceptance criteria, required independent review and evidence schema revision;
- creation time, policy revision and audit correlation ID.

The envelope is a design requirement, not a deployed wire format. Required fields cannot be populated with invented defaults. Missing mandatory authorization or evidence fields means reject/hold, not permissive execution.

## 4. GitHub Adapter capability model

Every operation must be authorized by a short-lived, auditable capability whose scope is no broader than the mission. The concrete token type and issuer remain governed by the repository's security/identity contracts.

| Capability | Minimum scope | Default |
|---|---|---|
| Read repository metadata | Named repository, refs and commit metadata | Deny until configured |
| Read source/docs | Explicit path prefixes and immutable ref | Deny until configured |
| Create isolated branch/commit | Named repository, allowed branch prefix, mission ID and target SHA | Deny until configured |
| Update documentation | Explicit allowlisted docs paths only; no protected normative contracts unless separately approved | Deny |
| Open/update pull request | Named base/head, required reviewers and evidence links | Deny until configured |
| Merge | Protected branch, governance and review policy | **Prohibited absent separate explicit authorization** |
| Release/deploy/production mutation | Named environment and release gate | **Prohibited absent separate explicit authorization** |
| Secrets/workflow administration | Secret values, Actions permissions, runner groups or environment protection | **Prohibited absent separate explicit authorization** |

Every write must log actor, capability ID (not secret token), mission ID, repository, operation, path/ref, before/after SHA, timestamp, decision, result and evidence URI. Logs must not contain credentials, model prompts containing restricted data, or secret-bearing environment values.

## 5. Executor/provider routing contract

Before dispatch, Jarvis must create an immutable routing decision record bound to the mission and policy revision:

- task and data classification;
- allowed egress class and destination/provider allowlist;
- chosen executor and exact provider identity;
- exact model identifier, immutable digest/revision when available, and runtime version;
- route type: local-only, approved hybrid, or approved cloud;
- reason/policy rule for the choice;
- budget/quota and authorization reference;
- fallback policy and whether fallback was actually used;
- timestamp, config/policy revision and audit correlation ID.

### Required rules

1. **Local-only is fail-closed.** If the approved local route is unavailable, incompatible or unverified, hold/fail the mission; never silently fall back to Anthropic, OmniRoute, FreeLLMAPI or another cloud route.
2. Claude Code is an engineering client/agent surface, not proof of which model/provider executed the request.
3. Ollama/Alamo, FCC, FreeLLMAPI, OmniRoute and UnoRouter are distinct component identities until their implementation, endpoint and deployment relationships are pinned by evidence.
4. Similar names are not identity evidence. In particular, UnoRouter, OmniRoute and OpenRouter must not be merged by assumption.
5. FreeLLMAPI's `local_gateway` registry classification conflicts semantically with cloud/provider wording in the distributed AI architecture. Resolve service location, upstream, data egress and model identity before enabling a route.
6. A local model tag is not a verified model identity. Require source/provenance, digest, license and runtime compatibility before qualification.
7. No route is considered connected or qualified merely because a CLI exists or a process is running.

## 6. Workspace, lease and worker admission

- Each mission targets an immutable source SHA and a unique isolated workspace.
- A worker must have a valid lease before writing; stale lease or expired claim means stop/hold and reconcile with ASTRA's single writer.
- A directory named as a worktree is not proof it exists, is clean, belongs to a live worker or holds a valid lease.
- Historical inventory note (2026-10-14): an earlier snapshot recorded nine auxiliary worktree entries as prunable. This is stale historical provenance only; it is not a statement about the clean target, current filesystem, or current worker/lease state. Do not inspect, clean up, restore or repurpose any legacy worktree as part of this design. The new target inventory must be established independently under separately authorized read-only inspection.
- A worker may produce a patch and evidence but cannot self-approve, merge, release or mark system qualification PASS.

## 7. Evidence and lifecycle state machine

Keep these statuses distinct:

`DESIGNED → IMPLEMENTED → TESTED → VERIFIED → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → ACCEPTED`

Transitions are not automatic; each requires its own defined gate and evidence. Not every component uses every state, but no state may be inferred from a prior state.

### PASS evidence tuple

A component/gate PASS is independently attributable only when the record binds:
- stable component and gate IDs plus gate-contract revision;
- exact source/target SHA;
- run/execution ID and UTC start/end;
- environment/node identity and relevant tool/provider/model versions;
- expected assertion, observed result and exit/disposition;
- immutable artifact URI plus digest;
- redaction/secrets-suppression declaration;
- freshness/expiry policy;
- independent reviewer and review result where required.

The owner reported on 2026-10-14 that some individual services/gates had returned PASS, while ASTRA end-to-end autonomous queue completion had not been achieved. Until exact identifiers and artifacts are linked, preserve these as `OWNER_REPORTED_PARTIAL_PASS / EVIDENCE_LINK_PENDING`. Do not invent missing gate IDs, run IDs, SHAs or logs. Overall ASTRA queue, worker dispatch, lease integrity, A3 and end-to-end completion remain NOT ACHIEVED / NOT PROVEN on the current evidence record.

## 8. Clean target deployment boundary

The current owner direction is a **new, clean, reproducible deployment**. Historical hostnames, legacy node identities, prior failed installations, old worktree records and earlier hardware-placement suggestions are not target inventory, deployment instructions, or proof of current hardware/runtime state.

The previous hardware list in this draft is retained only as historical provenance and is superseded for target planning by this section. Do not use Mac Pro 2013, Mac mini 2011, mh-dev-01, mh-dev-02, Voktors-Mini.Dlink, Voktors-Mac-mini.local, or any other legacy identity as a deployment target merely because it appears in older records.

Current target-role concepts, pending owner confirmation and fresh evidence:

- developer workstation;
- low-resource auxiliary/control server;
- optional future owned GPU/video-generation server;
- developer clients;
- restricted API-key workflow host.

These are role categories, not identified or qualified machines. Exact hardware identity, OS/build, CPU/GPU/accelerator, memory, storage, firmware, network, security-maintenance status, workload suitability and resource envelope remain **UNKNOWN until independently evidenced for the new target**. Do not infer a physical machine from an old nickname or map a role to a legacy host.

Any future host inspection, provisioning, installation, qualification or deployment requires its own explicit authorization. This draft authorizes none of those activities.
## 9. Acceptance gates before implementation

| Gate | Required evidence | Current disposition |
|---|---|---|
| G1 Source contract | Accepted ASTRA A0 interface, queue-state owner and Product State Authority contract mapped without conflict | OPEN |
| G2 Identity/capabilities | Issuer, audience, expiry, revocation, scope, replay handling and audit requirements resolved against security primary source | OPEN |
| G3 Routing/egress | FreeLLMAPI/OmniRoute/UnoRouter/FCC/Ollama identities and local/cloud boundary pinned; local-only fail-closed semantics | OPEN |
| G4 Component provenance | Version/source/digest/license/runtime for every admitted executable/model | OPEN |
| G5 Portable hardware | Exact host inventory and compatibility evidence for each selected profile | OPEN |
| G6 Evidence linkage | Historical partial PASS records mapped to exact gates, target SHAs and immutable artifacts | OPEN |
| G7 Independent review | A3/reviewer independence, review input and evidence capture specified | OPEN |
| G8 Lifecycle and rollback | Install/update/rollback/recovery/health gate contract accepted | OPEN |
| G9 Governance | Explicit owner/governance acceptance of this draft and affected domain changes | NOT GRANTED |
| G10 Qualification | Separately authorized full qualification run and evidence bundle | NOT RUN / NO-GO |

## 10. Next actions

1. Map historical service/gate PASS artifacts to exact IDs and immutable evidence, preserving their original scope.
2. Resolve provider semantic conflict and component identities by source/config inspection without reading secrets or invoking providers.
3. Complete the machine-readable evidence schema and align the project-wide matrix to it.
4. Prepare a clean target-role inventory worksheet with explicit UNKNOWN fields; bind any later physical host only after owner identification and separately authorized read-only inspection.
5. Keep installation, tests, qualification, provider calls, infrastructure changes, deployment, merge and release separately authorized.

**Conclusion:** this draft provides a proposed control-plane/GitHub Adapter contract and deployment boundary. It is not accepted, implemented, qualified or deployed. ASTRA end-to-end autonomous queue remains NOT ACHIEVED on current evidence.
