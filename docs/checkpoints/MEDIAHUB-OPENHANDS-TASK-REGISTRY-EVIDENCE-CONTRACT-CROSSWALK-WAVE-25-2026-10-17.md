# MediaHub OS — OpenHands Task / Registry / Evidence Contract Crosswalk, Wave 25

- Date: 2026-10-17
- ID: MH-OPENHANDS-CONTRACT-CROSSWALK-25
- Contour: A — Developer Fabric
- Status: DOCUMENTARY SOURCE CROSSWALK / CANDIDATE ONLY / RUNTIME BLOCKED
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Parent: [Wave 24 source pin](MEDIAHUB-JARVIS-SOURCE-PIN-AND-CAPABILITY-CROSSWALK-WAVE-24-2026-10-17.md)
- Reuse-first control: [Wave 23 gate](MEDIAHUB-REUSE-FIRST-UPSTREAM-DISCOVERY-GATE-WAVE-23-2026-10-17.md)

## 1. Bounded scope and source anchors

This pass compares the pinned OpenHands Software Agent SDK source description with the existing MediaHub cloud-agent contract candidates. It is source reading only. It performs no clone, install, execution, test, qualification, model/provider invocation, credential use, host/runtime inspection, infrastructure change, deployment, or branch integration.

| Source | Ref / immutable anchor | Live blob SHA | Use |
|---|---|---|---|
| OpenHands SDK README | `OpenHands/software-agent-sdk@6530325e9dd0ea1b6b4f1994d7dab52764cfc3f1:README.md` | `386dc8945133cb51969192b0b29c8396719cbff6` | Python, TypeScript and REST APIs; Agent/Conversation/Tool abstractions; local or ephemeral workspace model |
| MediaHub task envelope v0.2 | docs branch | `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a` | Task intent, authority refs, bounded scope, data policy, routing, budget, deadline, retry, review and evidence linkage |
| MediaHub agent registry v0.2 | docs branch | `b49b89b8fbdfc180862e3dc78f8198f35e486035` | Agent identity, capability declaration, provider routes, execution bounds, authorization/lifecycle/evidence refs |
| MediaHub evidence manifest v0.2 | docs branch | `40c402432fd0f3899d45fde0fa0a8af4d34c593a` | Execution/source/input/artifact/disposition/review/schema refs plus separate verification and qualification records |
| A0/MH-12 source trace | docs branch | `49ca0b69737bf8d44fe3a42daa47fd9157c9097d` | Existing authority boundary and unresolved ingress/issuer/lease/fencing/replay/cancellation semantics |
| Clean target manifest reconciliation | docs branch | `1f748bf80e08067fd85a7e1b0821cc4d12bda676` | Current target remains UNKNOWN/BLOCKED |
| R-06 governance disposition template | docs branch | `834fd1ab70eee88355844ba2ebba6c2b6c47ecdb` | Audit/privacy governance decision remains unfilled/open |

The three v0.2 schemas explicitly identify themselves as PROPOSED ONLY. Their presence and structural detail grant no runtime authority.

## 2. Capability-to-contract crosswalk

| OpenHands capability/source concept | Reusable MediaHub contract surface | Adapter responsibility | Admission state |
|---|---|---|---|
| SDK Agent / Conversation | Task envelope `task_type`, bounded `scope`, `budget`, `deadline`, `retry`, `review` | Validate envelope against an immutable schema pin; translate only allowlisted task types, prompts and execution options; preserve task and attempt identity | DESIGN MAPPING ONLY |
| Tool registration | Registry `capabilities.effects`, `allowed_paths`, `forbidden_paths`, `max_changed_files` | Construct the smallest tool allowlist; enforce path and operation limits outside model-authored instructions; reject excess authority | POLICY/ENFORCEMENT UNPROVEN |
| Workspace selection | Envelope source/ref and scope; registry execution bounds; evidence source SHA | Allocate an isolated, revision-bound workspace; bind workspace lease and cleanup evidence to accepted target profile | TARGET-GATED |
| Agent Server / REST / WebSocket | Envelope authority and routing references; A0 ingress contract | Keep ingress MediaHub-controlled; verify caller, issuer, audience, expiry, revocation, scope, target and replay semantics before dispatch; apply network/CORS restrictions | BLOCKED |
| Provider/model routing | Envelope `routing.authorized_destinations`; registry `provider_routes`; policy refs | Resolve provider/model IDs to accepted egress policy and immutable route evidence; forbid silent fallback across data classes or paid/free policy boundaries | GOVERNANCE-GATED |
| Conversation/event persistence | Evidence manifest execution and artifact references | Treat upstream conversation state as execution-local; export only minimized, classified, policy-approved evidence; never elevate it to canonical MediaHub task/product state | ADAPTER DESIGN OPEN |
| Returned changes/artifacts | Evidence manifest `artifacts`, `disposition`, `review`, `verification`, `qualification` | Bind every artifact to task, attempt, source commit, workflow/action SHAs and schema/policy revisions; treat output as untrusted until independent review | VERIFICATION OPEN |

## 3. Source-backed conclusions

1. OpenHands exposes useful reusable agent, tool, workspace and remote execution abstractions. It does not, from the reviewed README evidence, provide native conformance to MediaHub's proposed task-envelope, agent-registry or evidence-manifest schemas.
2. The correct integration shape is a narrow adapter around upstream SDK/server interfaces, not a second MediaHub task queue, identity authority, provider registry or canonical evidence store.
3. The Wave 24 source review records Agent Server default binding to `0.0.0.0` and broad access to its configured workspace. Direct exposure is therefore excluded from the candidate path until target-specific ingress and isolation controls are source-bound and independently qualified.
4. Schema references, authority references and policy references are strings in the proposed contracts; the consumer must resolve them to accepted, immutable, scope-correct revisions. Schema validation alone cannot establish authorization, freshness, provenance or qualification.
5. The evidence manifest deliberately separates execution, verification and qualification. A successful upstream task must not be represented as a verified, qualified, released, deployed or accepted MediaHub change without the corresponding independent evidence.
6. Current Personal Jarvis upstream identity remains unresolved. Repeated repository search did not produce a reliable owner-qualified canonical record in the connector response; lookalike repositories remain provenance leads only. No upstream selection follows from this pass.

## 4. Required adapter acceptance evidence

Before any runtime admission proposal can be considered, the future adapter package must specify and later evidence:

- accepted API/transport and exact request/response schemas, all pinned by immutable revision;
- authenticated caller identity and A0 issuer/grant verification, including audience, expiry, revocation, key rotation and fail-closed behavior;
- monotonic lease/fencing semantics, cancellation races, idempotency scope, replay handling and reconciliation after ambiguous completion;
- target manifest, isolated workspace boundaries, cleanup/recovery, filesystem and tool capability enforcement;
- provider/model route authorization, data classification, egress restrictions, quota and fallback policy;
- privacy-minimized audit event contract, durable acknowledgement, outage behavior, retention/deletion and reader authorization under an accepted R-06 disposition;
- source/action/runtime dependency inventory, license and provenance review, vulnerability disposition and target compatibility;
- negative/degraded-mode tests, independent review, qualification evidence and separate release/deployment/acceptance decisions.

These are closure criteria, not executed tests or an authorization to run them.

## 5. Decision and next step

**Disposition:** retain OpenHands as a source-pinned candidate for a bounded engineering-task execution subsystem. Reuse its SDK/tool/workspace abstractions through a MediaHub-owned adapter only after contract and security gates close. Keep runtime use BLOCKED and candidate selection provisional.

Next bounded pass: source-pin and crosswalk the actual OpenHands Agent Server routes/configuration and workspace/tool enforcement at the same commit, then compare each control with the A0/MH-12/R-06 gaps. Continue the Personal Jarvis provenance search independently; no lookalike may be promoted without authoritative repository identity, immutable release, license and provenance evidence.

## 6. Verification boundary

GitHub source reads and live ref comparison only. No implementation, install, test, qualification, provider/model call, credential use, host/runtime inspection, infrastructure change, deployment or branch integration occurred.
