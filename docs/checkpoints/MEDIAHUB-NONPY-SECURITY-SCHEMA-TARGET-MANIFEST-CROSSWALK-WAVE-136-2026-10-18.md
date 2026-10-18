# MediaHub OS — Non-Python Security Schema and Target-Manifest Crosswalk, Wave 136

- Date: 2026-10-18
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Status: **BOUNDED SOURCE CROSSWALK / TWO TRUST ROUTES MUST REMAIN DISTINCT / ACCEPTANCE GATES OPEN**
- Scope: inspect selected non-Python security, identity, capability, trust, runner and ingress artifacts by exact ref/blob; this is not a full content scan of all non-Python files, implementation, runtime qualification or product acceptance.

## 1. Executive finding

The repository has adjacent files whose names contain “capability”, “trust”, “identity”, “runner” and “authorization”, but the reviewed files govern different concerns. They must not be treated as interchangeable evidence for a trusted capability issuer.

More importantly, there are **two distinct trust routes**:

1. **Jarvis → ASTRA A0 engineering-mission ingress**: external caller identity, mission admission, idempotency, lease/fencing, cancellation/recovery, result provenance and R-06 audit. The best-evidenced current code ingress is a local file-based Task Contract consumer; a separate signed operational-command path also exists. WB-14Z says neither is proven to be the accepted Jarvis mission producer-to-A0 consumer chain. WB-14AA remains a proposal and decisions A0-ING-01…09 remain open.
2. **P0-07 → P0-05 → P0-04 canonical product-state mutation**: operation/policy decision, trusted authorization context at the Consumer Boundary, and independent State Authority transaction authorization. The in-process `AuthorizationContext` seam inspected in Waves 133–135 belongs to this route; it is not evidence that Jarvis→A0 mission ingress is authenticated.

An A0 mission-admission result must not be treated as canonical product-state mutation authority. Conversely, a product-state `AuthorizationContext`, a signed operational-command envelope, or an executor/runner registry record must not be reused as proof of Jarvis→A0 authorization without an accepted cross-route contract.

## 2. Non-Python schema crosswalk

| Artifact | Ref / blob SHA | What it actually represents | Boundary |
|---|---|---|---|
| `architecture/mesh/capability.schema.json` | `main` / `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c` | Mesh executable/component inventory: provider, version, executable, identity hash, authority classification, qualification state and sandbox. | Not a request-bound grant or issuer/verifier schema; no issuer, audience, resource/scope, expiry or revocation lifecycle. |
| `schemas/domain/capability.schema.json` | `main` / `fe80659b570ac58829f10410feb5c700388f87c0` | Canonical capability exposed by a MediaHub device: commands, events, constraints, dependencies, conflicts and safety class. | Product/domain capability description, not an authenticated caller grant. |
| `schemas/domain/trust.schema.json` | `main` / `6cf5d60a1c038f25a85328c8d5cd3040405812d0` | Trust state record with status, source and timestamp. | No cryptographic attestation, issuer, audience, expiry or revocation protocol. |
| `schemas/domain/identity.schema.json` | `main` / `2caf58faf58eff2de82984a28109eb1aae87675d` | MediaHub device identity fields. | Does not establish authenticated workload identity or authorize an operation. |
| `schemas/identity/identity-boundary.schema.json` | `main` / `1d085bb1f2c458faaeff23bd92d83aa5d1bd3879` | Canonical identifier separation (device, binding, adapter, capability, event, command, execution, request, correlation, causation, recovery). | Identifier schema only, not a credential or capability issuer contract. |
| `schemas/domain/lifecycle.schema.json` | `main` / `f573802fc08d4af90fa5d1c15adcc4334839c05a` | Device lifecycle enum plus timestamp/reason. | Not the A0 mission lifecycle or authorization-context lifecycle. |
| `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md` | `main` / `8d831c2a8fa333977dd86524099568bae2a8db0e` | Useful proposed security baseline and fail-closed requirements. | Explicitly **PROPOSED ARCHITECTURAL BASELINE**, not an accepted issuer protocol. |
| `docs/architecture/MH-12-security-architecture.md` | `main` / `cf4ebfd5bf471ca676f075c51d3a24906504e490` | Accepted security design constraints around distinct identity/authentication/trust/capability/authorization, revocation and fail-closed operation. | Status remains ARCHITECTURE COMPLETE / GOVERNANCE REVIEW REQUIRED; no concrete issuer technology selected. |
| `docs/architecture/MH-CLOUD-AUTH-BASELINE.md` | `main` / `075652ad031e92f7d0c9231db6f40f5f45cd77b8` | Cloud provider API credential naming, routing order, egress and secret hygiene. | Provider-key routing is not the A0 mission issuer or the P0 trusted-context issuer. No credential was read or used. |
| `ops/qualification/authorized-schemes.yaml` | `main` / `5ae1182511486c2961e28c489ce891b74f1252f1` | Fail-closed qualification promotion registry; `authorized_pass` is intentionally empty until fresh exact-SHA evidence; independent A3 and human launch authorization are required. | Not per-request mission ingress authorization and not an `AuthorizationContext` issuer. |
| `docs/security/P0-06-threat-to-test-traceability.md` | `main` / `2c4eeac28e0255bfd5c6213eda8500ec8a148daa` | Accepted generic threat→control→verification traceability, including negative capability tests. | A requirement to produce verification evidence; not evidence that the issuer-specific tests were run or passed. |

The selected files do not establish a normative, request-bound trusted-context schema. This conclusion is limited to the exact artifacts listed; the full 545-blob non-Python content tree was not scanned exhaustively.

## 3. Runner contracts versus accepted clean target manifest

The repository contains runner contract records, but the manifest reconciliation remains unresolved:

| Artifact | Ref / blob SHA | Exact scope | Not established |
|---|---|---|---|
| `control/qualification/canonical-runner-contract.json` | `main` / `32ec7bbe371b1cfd3f2f46019ee1d2671980aa26` | Runner label `mediahub-control`, node `mh-dev-01`, user `mediahub-runner`, Linux x64 and runtime hostname/user checks. | Complete workspace/mount policy, egress/network/data class, storage/persistence, cleanup, evidence freshness and owner-accepted deployment target. |
| `control/qualification/distributed-runner-contract.json` | `main` / `993f51f07c7937165ffb3bfbe59cd0801ea71ec0` | Three named runner profiles with authority labels; explicitly states runner admission does not grant canonical state authority. | Acceptance/qualification of current physical targets or a complete worker-isolation manifest. |
| [Clean Target Manifest Authority Reconciliation, Wave 10](MEDIAHUB-CLEAN-TARGET-MANIFEST-AUTHORITY-RECONCILIATION-WAVE-10-2026-10-16.md) | docs ref / `1f748bf80e08067fd85a7e1b0821cc4d12bda676` | Bounded source review of exact target authority. | Its explicit disposition is target identity/profile UNKNOWN / BLOCKED; MH-15 NOT ACCEPTED / NOT FROZEN. It states the repository contains no owner-accepted exact clean target manifest in the reviewed source set. |
| [OpenHands route/workspace crosswalk, Wave 26](MEDIAHUB-OPENHANDS-AGENT-SERVER-ROUTE-WORKSPACE-SECURITY-CROSSWALK-WAVE-26-2026-10-17.md) | docs ref / `56671bcce15eca5b5d76ffe30ea4950ad39575a4` | Source-pinned candidate only. | Runtime admission blocked; workspace/network/cleanup controls and accepted target binding remain open. |

Therefore, a runner contract name or host label cannot substitute for the full clean target manifest requested by Issue #301. This is a scope distinction, not proof that the runner JSON files are invalid.

## 4. Ingress and owner-decision crosswalk

- [WB-14Z source-contract census](MEDIAHUB-CONTOUR-A-WB-14Z-A0-INGRESS-SOURCE-CONTRACT-CENSUS-2026-10-16.md), blob `95f3af63705f4ad7cd24405df9c7c396886cb3a3`: local file Task Contract consumer and signed operational-command workflow are separate; no accepted Jarvis producer-to-A0 consumer chain was established.
- [WB-14AA ingress contract candidate](MEDIAHUB-CONTOUR-A-WB-14AA-ASTRA-A0-INGRESS-CONTRACT-CANDIDATE-2026-10-16.md), blob `030273bfe9fd6d44e78b611c011af95d08c88a45`: **PROPOSED / NOT ACCEPTED / NOT FROZEN / NOT IMPLEMENTED**. A0-ING-01…09 cover owner/versioning, issuer/verifier, transport/caller edge, durable admission/idempotency, lifecycle/result/cancellation, freshness/replay, probe semantics, target binding and independent acceptance.
- [WB-05 issuer authority decision packet](MEDIAHUB-CONTOUR-A-WB-05-ISSUER-AUTHORITY-AND-TRUSTED-CONTEXT-OWNER-DECISION-PACKET-2026-10-15.md), blob `1b562c6546b1216f2ee89095cd6a78427a967dc5`: no issuer/verifier ownership option selected.
- [P0-07 D2 trusted-context proposal](P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md), blob `c0ae0d3fe340c3e50382b7d4aa8da7b6b5f56d9f`: owner-approved Option B authorizes proposal preparation only; its status remains proposal/governance review required/not accepted/not frozen. This concerns the P0 product-state trust route, not automatic acceptance of Jarvis→A0 ingress.

DEC-DEV-02 Option C remains binding: Jarvis coordinates corporation-level missions, ASTRA A0 controls ASTRA-internal engineering workflow and its evidence/gate state, while MediaHub Product State Authority alone owns canonical product-state mutation.

## 5. Fresh project state at this pass

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation ref HEAD before this Wave 136 write: `0f6c5b6c049b4dc286a6b9b80579089d40fbcea9`.
- `main` and documentation ref are diverged, documentation branch 2240 ahead / 27 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- [PR #350](https://github.com/VlDMlNSh/mediahub-os/pull/350): open/Draft/unmerged; head `4c1ebafc5d33e8ae075a5bba85771d14aed4ac96`; GitHub API reports `mergeable=false`; no submitted reviews returned.
- [CI run 39078844123](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39078844123) succeeded for schema/fixture/report validation; it does not satisfy issuer/ingress, R-06, independent review or target-manifest gates.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open.
- Current map blob `e6ed792d3e64df994b7895b6ae0aa1d1a69cfff2` still returns empty body via Contents API; full blob retrieval confirms it is approximately 1.06 MB. Main map and main checkpoint were not overwritten.
- The SentinelX inventory in this session showed zero connected hosts; the previously enrolled Mac mini was offline. No host/runtime tests were run.

## 6. Disposition and next bounded action

Do not add an issuer/token format or external endpoint in this pass. The actionable next unit is to reconcile the open owner decisions for the **A0 mission route** separately from the **P0 product-state route** and obtain the accepted target/workspace/network manifest. Only then define contract-backed positive/negative conformance vectors for caller identity, issuer, audience/scope/target, freshness/revocation, replay/idempotency, lease/fencing/cancel/recovery, audit/privacy and fail-closed behavior.

No code, schema, workflow, credentials, provider, host, deployment, merge or branch integration was changed or executed in this pass. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT ACCEPTED**. Contour B remains gated.

## Navigation

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #350](https://github.com/VlDMlNSh/mediahub-os/pull/350)
