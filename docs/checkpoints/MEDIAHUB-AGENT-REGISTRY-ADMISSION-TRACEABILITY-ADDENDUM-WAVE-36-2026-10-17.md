# MediaHub OS — Agent Registry and Admission Traceability Addendum, Wave 36

- Date: 2026-10-17
- Parent matrix: docs/checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md
- Primary crosswalk: docs/checkpoints/MEDIAHUB-EXISTING-AGENT-REGISTRY-A0-ADMISSION-AND-EGRESS-RECONCILIATION-WAVE-36-2026-10-17.md
- Roadmap companion: docs/checkpoints/MEDIAHUB-MASTER-ROADMAP-EXECUTION-ADDENDUM-WAVE-36-2026-10-17.md
- Status: **PROPOSED / SOURCE-BOUND TRACEABILITY / NOT ACCEPTED / RUNTIME UNVERIFIED**

## 1. Requirement-to-component crosswalk

| Requirement ID | Required invariant | Existing component | Evidence / SHA | Current state | Required proof |
|---|---|---|---|---|---|
| CAF-36-01 | Known agents/providers are catalogued without secret values | profiles/agent-registry.json | main blob 993cbbe1b2b2a88da7d8884a897b404f055981a8 | Catalog exists, v1.2.0; schema validation of full catalog is not evidenced | Versioned schema and compatibility validation on exact catalog SHA |
| CAF-36-02 | Engineering roles remain architect/builder/verifier under one coordinator | .github/agent-system/registry.yaml | main blob 0317d1e794aa80cd0fa22bd953b95921b26aafd3 | Declared role registry exists; runtime/authority conformance remains to prove | Registry-to-A0 mapping, task-scoped worker evidence, duplicate coordinator rejection |
| CAF-36-03 | Provider route selection is separate from task authorization | schemas/ai/ai-provider-registry.schema.json | main blob 9537a64bc948b1bea3e2a640670f48e107760a50 | Provider selection schema exists; route-level data-class/destination/fallback authorization is outside this schema | Task envelope and MH-21 policy gate evidence |
| CAF-36-04 | Adapter configuration does not grant authority | schemas/ai/ai-provider-adapter.schema.json | main blob e0dab7002222451579e649a7d1d29985393d9a42 | Adapter boundary exists; endpoint and configuration refs require policy validation | Rejection of unknown endpoint and independent policy decision |
| CAF-36-05 | One A0 queue lifecycle governs lane state | ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json | main blob b948f0beb510f24399d82aaefcb7f95584e99cab | 23-lane manifest exists; global dependencies/leases/owners contain UNKNOWN values | Complete dependency/owner/lease crosswalk and exact-SHA evidence |
| CAF-36-06 | Parallel independent runners cannot claim overlapping work or share mutable authority without atomic claim control | runtime/mediahub_runtime/agent_fabric.py | main blob 3c70dda5df8c6caa9411201d754ead6b3bfdf6dd | File-backed claim store; only local lock boundary is evidenced | Distributed atomic claim, fencing, lease expiration, cancel/replay/recovery proof |
| CAF-36-07 | A0 admission authority is distinct from the trusted authorization-context issuer | ASTRA unified system model; P0-07 D2 proposal | main blob adc852009c3a79d0e64265a3af8a4910a1388057; docs blob c0ae0d3fe340c3e50382b7d4aa8da7b6b5f56d9f | D2 issuer/ingress proposal remains open | Accepted issuer, audience, lifecycle, expiry, revocation, binding and consumer validation contract |
| CAF-36-08 | Secret lifecycle excludes raw values from Git, evidence, logs and prompts | docs/architecture/MH-12-secrets.md | main blob 4e4faf00e3d24c1de5a394e78670c68786ac9a1e | Lifecycle requirement exists; exact store is non-canonical | Approved store ADR, provider/job isolation, rotation/revocation evidence |
| CAF-36-09 | Every outbound request is bound to data class, purpose and approved destination | MH-21 data-egress / egress-control / provider-trust | main blobs 242b3090d41f52866889b8c8cf587ff4c95eadb3, aae23e11a70b1a7094d05709f8669040f60c1dcd, ad7226a2e7eeeaf412f94e08440db72ac4fe13cf | Policies are PROPOSED; runtime enforcement remains unproven | Destination allowlist, data class/purpose authorization, bounded request and sanitized audit |
| CAF-36-10 | Audit evidence has an accepted privacy, retention, outage and reconciliation contract | R-06 reconciliation/template | docs blobs 452d3531c9897679d52cedc7b5311234f98b8fa8, 834fd1ab70eee88355844ba2ebba6c2b6c47ecdb | OPEN; approval route unestablished, template unfilled | Actual governance disposition and exact versioned evidence contract |
| CAF-36-11 | Component selection is reused; new framework is added only for an evidenced gap | Canonical Component Manifest 2.0 | main blob 45988bf9da202c9597d0ca2de50e92e5c2e6ed55 | Canonical selection manifest exists; target deployment manifest unresolved in reviewed set | Gap statement, target profile and explicit admission record |
| CAF-36-12 | Candidate output never qualifies itself and cannot promote release/launch | ASTRA qualification schema and Current Truth | main blobs aef6229477ed8ec45e45170f98ea87f7ba75ca29, 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731 | G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED | Fresh source-bound evidence, independent A3, 24h soak and human launch authorization as applicable |

## 2. Proposed state mapping

Keep the existing 23-lane disposition vocabulary authoritative for lane progress: WAIT, READY, CLAIMED, VERIFY, BLOCKED, CLOSED.

Agent admission is a separate subordinate state vocabulary:
DISCOVERED → REVIEW_PENDING → WAITING_AUTH → AUTH_VERIFIED → READ_ONLY_ADMITTED → PATCH_ADMITTED → QUALIFIED → ACTIVE.
DEGRADED, BLOCKED, QUARANTINED, REVOKED and EXPIRED are explicit stop states.

Provider adapter readiness (uninitialized/initializing/ready/degraded/failed/stopped) remains a runtime-health field. Provider selection enabled/disabled remains a route configuration field. Neither maps directly to qualification or admission. All mappings must be explicit, versioned, and lossless.

## 3. Key custody and egress evidence rule

Host-independent credential custody means the secret reference follows provider/account/project or authorized repository/environment identity; it does not mean that a network request has no source location. GitHub OIDC may provide short-lived credentials only when a supported destination has an explicit trust relationship. Static-key services need a scoped approved secret store. The destination and data class remain policy-bound before request execution.

## 4. Verification status

The evidence above is from current-main source reads and current documentation-branch proposal records. No source code or runtime registry was changed in this pass. No provider or model was invoked, and no qualification evidence was generated. The addendum records requirements and gaps; it does not promote any agent, lane or gate.
