# MediaHub OS — Canonical Source Registry Addendum, Wave 36

- Date: 2026-10-17
- Parent register: docs/checkpoints/MEDIAHUB-CANONICAL-SOURCE-REGISTRY-AND-SECURITY-EVIDENCE-LEDGER-WAVE-03-2026-10-16.md
- Primary reconciliation: docs/checkpoints/MEDIAHUB-EXISTING-AGENT-REGISTRY-A0-ADMISSION-AND-EGRESS-RECONCILIATION-WAVE-36-2026-10-17.md
- Status: **SOURCE-BOUND ADDENDUM / PROPOSED / RUNTIME UNVERIFIED**

## 1. Source entries

| Addendum key | Source | Ref | Blob SHA | Supported claim | Boundary |
|---|---|---|---|---|---|
| W36-SRC-01 | Agent catalog | main:profiles/agent-registry.json | 993cbbe1b2b2a88da7d8884a897b404f055981a8 | Existing catalog ID/version are mediahub.ai.agent-registry 1.2.0 | Catalog values do not establish authentication or qualification |
| W36-SRC-02 | Role-fabric registry | main:.github/agent-system/registry.yaml | 0317d1e794aa80cd0fa22bd953b95921b26aafd3 | One A0/Astra coordinator and architect/builder/verifier roles with task-scoped workers | Declaration is not proof of active runtime state |
| W36-SRC-03 | Provider selection schema | main:schemas/ai/ai-provider-registry.schema.json | 9537a64bc948b1bea3e2a640670f48e107760a50 | Provider selection is represented by provider ID, enabled, priority and selection policy | This schema is insufficient as a task-admission or data-egress authorization record |
| W36-SRC-04 | Provider adapter schema | main:schemas/ai/ai-provider-adapter.schema.json | e0dab7002222451579e649a7d1d29985393d9a42 | Adapter identity, provider/adapter type, operations, capabilities, availability, endpoint and config reference are schema-controlled | Adapter readiness is not admission or qualification |
| W36-SRC-05 | 23-lane execution manifest | main:ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json | b948f0beb510f24399d82aaefcb7f95584e99cab | Existing queue/lane manifest and current WAIT/READY/CLAIMED/VERIFY/BLOCKED/CLOSED vocabulary | Most owner/lease/source SHA/worker values are UNKNOWN |
| W36-SRC-06 | Claim/lease primitive | main:runtime/mediahub_runtime/agent_fabric.py | 3c70dda5df8c6caa9411201d754ead6b3bfdf6dd | Local claim files, flock, overlap checks, heartbeat and expiry exist | Independent cross-runner atomicity remains unproven |
| W36-SRC-07 | Unified ASTRA development-system model | main:architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml | adc852009c3a79d0e64265a3af8a4910a1388057 | A0 coordinates, A1 architects, A2 implements, A3 independently verifies; cloud/executor/transport have no authority | Does not create a P0-07 authorization-context issuer |
| W36-SRC-08 | Qualification and launch schema | main:architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml | aef6229477ed8ec45e45170f98ea87f7ba75ca29 | G0–G11, fresh evidence, fail-closed and human launch requirements | Current qualification truth remains BLOCKED |
| W36-SRC-09 | ASTRA governance contract | main:architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml | 1d3ac25e7817f365807ad85d0d7c9007bd48bebf | Credential lifecycle/limits, role boundaries and claim concurrency bounds | Canonical design contract does not itself establish current runtime pass |
| W36-SRC-10 | MH-12 secret lifecycle | main:docs/architecture/MH-12-secrets.md | 4e4faf00e3d24c1de5a394e78670c68786ac9a1e | Secret lifecycle and exclusion from source/logs/prompts/evidence; store requires evidence/ADR | Specific secret store remains open |
| W36-SRC-11 | MH-21 data egress | main:docs/architecture/MH-21-data-egress.md | 242b3090d41f52866889b8c8cf587ff4c95eadb3 | Classification, purpose, destination, privacy/security, authorization, minimization and bounded transfer required | Status PROPOSED |
| W36-SRC-12 | MH-21 egress control | main:docs/architecture/MH-21-egress-control.md | aae23e11a70b1a7094d05709f8669040f60c1dcd | Destinations must be explicit, identifiable, policy-controlled, logged and bounded | Runtime enforcement remains to prove |
| W36-SRC-13 | MH-21 provider trust | main:docs/architecture/MH-21-provider-trust.md | ad7226a2e7eeeaf412f94e08440db72ac4fe13cf | Provider approval states, review dimensions and revocability are specified | Provider-specific evidence is still needed |
| W36-SRC-14 | P0-07 trusted context proposal | docs:P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md | c0ae0d3fe340c3e50382b7d4aa8da7b6b5f56d9f | Trusted issuer/lifecycle is a separate proposed authority boundary | NOT ACCEPTED / NOT FROZEN |
| W36-SRC-15 | R-06 governance route reconciliation | docs:MEDIAHUB-P0-07-R06-AUDIT-PRIVACY-GOVERNANCE-ROUTE-RECONCILIATION-WAVE-06-2026-10-16.md | 452d3531c9897679d52cedc7b5311234f98b8fa8 | Reviewed records do not establish an accountable R-06 approval route | OPEN |
| W36-SRC-16 | R-06 disposition template | docs:MEDIAHUB-P0-07-R06-GOVERNANCE-DISPOSITION-TEMPLATE-WAVE-07-2026-10-16.md | 834fd1ab70eee88355844ba2ebba6c2b6c47ecdb | Governance template covers audit/privacy decisions | UNFILLED |
| W36-SRC-17 | Canonical Component Manifest 2.0 | main:docs/checkpoints/mediahub-github-component-final-manifest-2.0.md | 45988bf9da202c9597d0ca2de50e92e5c2e6ed55 | Existing component selection authority and target/future gate rules | Must not be substituted for a target deployment manifest |
| W36-SRC-18 | GitHub OIDC documentation | https://docs.github.com/en/actions/concepts/security/openid-connect | retrieved 2026-10-17 | Supported trust relationships can provide short-lived tokens to specific workflow jobs | Requires exact provider support and trust policy; no universal API-key replacement |
| W36-SRC-19 | GitHub-hosted runner IP documentation | https://docs.github.com/en/actions/reference/runners/github-hosted-runners | retrieved 2026-10-17 | Hosted-runner network source and IP ranges are real service properties; ranges can be broad/dynamic | Does not prove provider region acceptance |
| W36-SRC-20 | GitHub cloud-agent responsibility/security reference | https://github.com/github/docs/blob/main/content/copilot/responsible-use/agents.md | retrieved 2026-10-17 | Official reference describes scoped repo/branch write and isolation of secrets to an appropriate environment | Capability reference only; no MediaHub admission |

## 2. Evidence records

| Addendum key | Evidence statement | State | Boundary |
|---|---|---|---|
| W36-EVD-01 | Existing agent catalog, role registry, provider schemas and 23-lane queue can be reconciled without inventing a parallel registry | SOURCE-VERIFIED | Source inspection only |
| W36-EVD-02 | Catalog registration fields are distinct from task-specific authorization and qualification gates | DESIGN REQUIREMENT | Must be encoded in the accepted admission contract |
| W36-EVD-03 | A0's coordination authority is distinct from P0-07 trusted authorization-context issuance | SOURCE-VERIFIED DESIGN BOUNDARY | D2 remains proposed/open |
| W36-EVD-04 | R-06 privacy/audit approval path remains unestablished in the reviewed documents | SOURCE-VERIFIED | Review source scope listed above |
| W36-EVD-05 | Current ASTRA qualification truth is G0–G11 BLOCKED / overall NOT_PROVEN | SOURCE-VERIFIED | Exact current-main artifact read |
| W36-EVD-06 | Hosted-runner credential independence cannot imply zero network egress origin or zero regional signals | OFFICIAL DOC SUPPORTED | Provider-specific destination, terms and region checks remain required |
| W36-EVD-07 | Wave 36 changes documentation only; registries and runtime workflows remain unchanged | CHANGE RECORD | Verify Wave 36 commits and read-back |

## 3. Governance notes

These addendum keys are local to this Wave 36 index and do not replace canonical stable source/evidence IDs. Before folding any record into the parent registry, read the live parent file, identify its current maximum IDs and perform a collision check.

No provider/model call, credential access, test, qualification, workflow dispatch, host/runtime inspection, infrastructure update or deployment occurred in this pass.
