# MediaHub OS — Canonical Source Registry and Security Evidence Ledger, Wave 03

- Date: 2026-10-16
- Repository: `VlDMlNSh/mediahub-os`
- Review ref: `main`
- Documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD snapshot: `b45324009ac3aa65322a702c28069b12190bc4b8`
- Status: **SOURCE-ANCHORED CONTROL ARTIFACT / PROPOSED / NOT NORMATIVE / NOT A SECURITY QUALIFICATION**
- Purpose: establish a compact, SHA-bound register of authority-bearing sources and security evidence gaps without replacing accepted contracts or implying implementation.

## 1. Registry rules

1. Functional authority remains Functional Baseline 2.0 on `main`; Baseline 1.0 is historical provenance.
2. A source's existence or status label does not imply implementation, verification, qualification, release, deployment, or production acceptance.
3. `main` and the documentation ref are separate evidence contexts. Live compare at this pass: DIVERGED, documentation ref ahead 1,649 / behind 10, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No branch integration is part of this work.
4. Blob SHA identifies the retrieved file content. HEAD/commit context is recorded separately; this pass has exact live blob SHAs for the listed paths and a pinned main tree snapshot, rather than a claim that every listed file was individually resolved to a commit object.
5. UNKNOWN means evidence was unavailable through the current connector or no direct evidence was retrieved. It never means clean, absent, or passed.
6. The registry is a control index. It does not amend contracts, appoint authority, grant permissions, or satisfy owner/governance gates.

## 2. Canonical and control source registry

| ID | Source / ref | Live blob SHA | Authority scope | Status / acceptance boundary | Depends on / downstream use |
|---|---|---|---|---|---|
| SRC-001 | `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Accepted functional reference for MediaHub OS / MediaHub iOS | ACCEPTED canonical functional baseline; implementation and qualification remain separate states | All domain requirements, component admission, acceptance criteria |
| SRC-002 | `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` | Not re-fetched in this pass | Historical provenance only | Historical source; any main-side edit requires provenance review before use | Baseline 2.0 change-control lineage |
| SRC-003 | `docs/checkpoints/mediahub-github-component-final-manifest-2.0.md@main` | `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Canonical development component-selection input | CANONICAL DEVELOPMENT INPUT; selection is not production qualification | Source pinning, license/security review, target profile, qualification gates |
| SRC-004 | `architecture/SECURITY-TRUST-AUTHORIZATION-CONTRACT.md@main` | `8d831c2a8fa333977dd86524099568bae2a8db0e` | Security/trust/authorization architectural baseline | PROPOSED ARCHITECTURAL BASELINE; default-deny and least-privilege principles documented | Identity, capability, policy, consumer boundary, State Authority |
| SRC-005 | `docs/architecture/MH-12-security-architecture.md@main` | `cf4ebfd5bf471ca676f075c51d3a24906504e490` | MH-12 security authority boundaries and security lifecycle | ARCHITECTURE COMPLETE / GOVERNANCE REVIEW REQUIRED | Identity, authentication, trust, capability, authorization, policy, secrets, audit |
| SRC-006 | `docs/architecture/MH-13-master-prompt.md@main` | `de00bea7f972fca30295c0855b0d324f845c0bc4` | MH-13 privacy/data-governance operating boundary | Architecture reference; not product mutation or implementation authority | Privacy classification, egress, retention, data governance |
| SRC-007 | `docs/architecture/MH-13-governance-state.md@main` | `7bd2624c3072ecf0a08a430bb8b8214b3d55d3fa` | MH-13 reconstruction acceptance state | ACCEPTED RECONSTRUCTION; historical original unrecovered; freeze NO; production implementation NOT AUTHORIZED; independent verification gate remains | MH-13 privacy crosswalk and R-06 audit/privacy decision |
| SRC-008 | `docs/checkpoints/MEDIAHUB-UNIFIED-CONTRACT-AND-TRACEABILITY-MATRIX-WAVE-01-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `a496f221f2dd5a8816f725f41504c64ad7a70476` | Proposed cross-project requirement/contract traceability | ANALYSIS / PROPOSED CONTROL ARTIFACT / NOT ACCEPTED AS NORMATIVE | Requirement-to-source, dependency, evidence, acceptance links |
| SRC-009 | `docs/checkpoints/MEDIAHUB-GITHUB-SECURITY-AND-UNIFIED-MATRIX-WAVE-02-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `5d7484a0dac931a6e6f671df1a1749bacc242982` | Static GitHub security review and Wave 02 findings | STATIC REVIEW; owner triage required; no qualification claim | Security workflow review, evidence collection, remediation planning |
| SRC-010 | `.github/workflows/astra-chat-control.yml@main` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Comment-triggered Astra control workflow | HIGH-priority review target; workflow grants contents/issues/actions write; target identity inconsistency recorded in Wave 02 | Issuer authentication, command integrity/replay, target binding, least privilege |
| SRC-011 | `.github/workflows/astra-autonomous-supervisor.yml@main` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Autonomous supervisor and downstream workflow dispatch | HIGH-priority review target; actions write and signed-command path require scoped review | Dispatch target constraints, HMAC claims, credential persistence, job permissions |
| SRC-012 | `.github/workflows/gemini-readonly-audit.yml@main` | `0d10efdda251f2ceca43175981c919102303572b` | Read-only advisory architecture audit | Source shows read-only contents scope and bounded context controls; run provenance/ref pinning still requires review | Immutable commit pin, context digests, untrusted output handling |
| SRC-013 | `.github/workflows/gemini-readonly-audit-retry.yml@main` | `96fcc9ed4e45659d0118f0b9f3593a0c736200f0` | Bounded retry path for read-only Gemini audit | Static source review only; runtime behavior is a separate evidence item | Retry ceilings, error suppression, artifact retention, run identity |
| SRC-014 | `tests/test_repo_secret_hygiene.py@main` | `21991478bac150146b73beffea7a10a4375e52d4` | Secret-shape and repository hygiene regression gate | Source exists; execution/current branch-protection requirement UNKNOWN | Secret scanner, test results, narrowly scoped synthetic-value exception |
| SRC-015 | `.github/workflows/astra-verify.yml@main` | `ae59d954f1ca6569a8d047589a2a54fd03e47f5b` | Astra verification workflow including synthetic HMAC smoke value | Static source reviewed; test-data exception is a follow-up review item | Secret hygiene rule scope, test-only value provenance |
| SRC-016 | `docs/checkpoints/mediahub-owner-decision-register-2026-10-14.md@docs/mediahub-chat-tree-map-20261012` | `d4d9a5aa3c1578fa0f345de704dd2c7bcda017a8` | Navigation/support register for owner-reserved decisions | Partial resolution; supporting register, not a normative contract or proof of delegated authority | Explicit owner/governance gates and accountable acceptance path |
| SRC-017 | `docs/checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md@docs/mediahub-chat-tree-map-20261012` | `81f07f292c1c7bb42edb69e2fa28cf9b21c40d03` | Proposed cross-domain requirement, control, dependency and evidence traceability | PROPOSED / INVENTORY AND RECONCILIATION DRAFT / NOT ACCEPTED / NOT FROZEN | All domains; matrix is the integration register, while source contracts retain authority within scope |
| SRC-018 | `docs/checkpoints/mediahub-unified-architecture-and-deployment-contract-v0.1.md@docs/mediahub-chat-tree-map-20261012` | `71ae0e68cc6ad494f85f33f64cde09ef5c4273d7` | Proposed cross-domain architecture/component admission/deployment gates | PROPOSED / NOT ACCEPTED / NOT FROZEN; qualification NO-GO | Baseline 2.0, target manifest, component admission, recovery and independent qualification |
| SRC-019 | `docs/checkpoints/MEDIAHUB-ACCELERATED-INTEGRATED-CONTRACT-AND-DEPLOYMENT-READINESS-WAVE-06-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `5ef7713c509e003c138fd87ce7eaeeb857df2383` | Accelerated convergence plan and source-anchored ASTRA workflow P0 remediation design | PLAN / SOURCE-ANCHORED / NOT ACCEPTED / NOT FROZEN | P0 remediation, project-wide matrix schema, readiness gates and five-day integration target |
| SRC-020 | `docs/checkpoints/MEDIAHUB-UNIFIED-SECURITY-CONTROL-MATRIX-AND-VERIFIABLE-CONTRACT-WAVE-05-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `ea9e9b0743d45fd9e29299642bd9a4b5d223097e` | ASTRA workflow security controls, evidence envelope and acceptance gates | PROPOSED / SOURCE-ANCHORED / NOT ACCEPTED / NOT FROZEN | Workflow source findings, P0/P1/P2 remediation and revision-bound evidence |
| SRC-021 | `docs/checkpoints/MEDIAHUB-FREE-CLOUD-AGENT-ONBOARDING-WAVE-01-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `18d99ea96e0f51d9dcd2245b46594371e29a0f56` | Free cloud-agent entry-point inventory and manual Gemini audit runbook | INVENTORY / PROPOSED / NOT RUNTIME-VERIFIED; additional agents NOT CONNECTED | Gemini workflow source, manually verified secret metadata, run ID/artifact digest and data-egress review |
| SRC-022 | `docs/checkpoints/MEDIAHUB-UNIFIED-CONTRACT-AND-TRACEABILITY-MATRIX-WAVE-01-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `a496f221f2dd5a8816f725f41504c64ad7a70476` | Initial project-wide traceability control-artifact proposal | PROPOSED / NOT ACCEPTED AS NORMATIVE; bounded scan only | Matrix lineage, source authority, branch evidence and cross-domain gap register |
| SRC-023 | `docs/checkpoints/MEDIAHUB-COMPONENT-ADMISSION-CROSSWALK-WAVE-01-2026-10-14.md@docs/mediahub-chat-tree-map-20261012` | `6550062d5fe5af206df5ea987f4c8d8ad287d11e` | Component provenance/admission crosswalk and lifecycle/recovery evaluation | CANDIDATES ONLY / NOT OWNER-APPROVED / NO COMPONENT ADMITTED | Canonical component manifest, scoped YAML admission subset, pinned provenance and target qualification |
| SRC-024 | `docs/checkpoints/MEDIAHUB-JARVIS-CONTROL-PLANE-GITHUB-ADAPTER-CONTRACT-DRAFT-01-2026-10-14.md@docs/mediahub-chat-tree-map-20261012` | `916df43726fb8f41038d5e9896be7e205284416f` | Proposed Jarvis engineering control plane, GitHub adapter, mission lifecycle and evidence contract | DESIGN DRAFT / NOT ACCEPTED / NOT IMPLEMENTED / NOT QUALIFIED | ASTRA A0 ingress, identity/capability, executor/provider routing, target profile and evidence gates |
| SRC-025 | `docs/checkpoints/MEDIAHUB-FREE-CLOUD-AGENT-ONBOARDING-WAVE-01-2026-10-16.md@docs/mediahub-chat-tree-map-20261012` | `18d99ea96e0f51d9dcd2245b46594371e29a0f56` | Read-only Gemini audit workflow operating runbook | Manual dispatch required; secret metadata and workflow execution unavailable through connected tool surface | Owner-side Actions UI, run/artifact evidence, bounded source review; no extra agent inferred |

## 3. Security evidence ledger

| Evidence ID | Control / claim | Evidence presently available | Status | Evidence required to close |
|---|---|---|---|---|
| EVD-001 | Branch protection on `main` and docs ref | Branch-protection API request returned 403; rulesets endpoint returned an empty list | UNKNOWN | Owner-visible settings export or screenshots with branch, date, required checks, review policy, force-push/admin bypass controls |
| EVD-002 | Code scanning alerts | Connector could not retrieve code-scanning alert endpoint | UNKNOWN | Security-tab export/API result, coverage period, alert states and dismissal rationale |
| EVD-003 | Dependabot/dependency alerts | Connector could not retrieve Dependabot alerts; no SCA execution occurred | UNKNOWN | Alert inventory plus dependency graph/manifests and reviewed lock/SBOM evidence |
| EVD-004 | Secret-scanning alerts and push protection | Connector could not retrieve secret-scanning alerts | UNKNOWN | Secret alert inventory, push-protection state, remediation/dismissal evidence |
| EVD-005 | SAST workflow coverage | No dedicated CodeQL/Semgrep workflow found by exact-path inventory in the reviewed main tree | GAP CANDIDATE / STATIC INVENTORY ONLY | Full workflow/path policy review and an approved scanner workflow with pinned actions and retained results |
| EVD-006 | SCA/SBOM coverage | Canonical component manifest selects Syft and Trivy; no scanner execution or SBOM artifact inspected in this pass | SOURCE POLICY EXISTS / EXECUTION UNKNOWN | Commit-bound SBOM, scanner versions/configuration, complete manifest coverage and result retention |
| EVD-007 | Astra comment issuer authorization | Workflow source checks OWNER/MEMBER/COLLABORATOR association; no cryptographic command provenance verified | HIGH-PRIORITY REVIEW | Threat model, accepted issuer policy, command signing/integrity, replay handling and adversarial evidence |
| EVD-008 | Astra token least privilege | Chat-control workflow has workflow-level contents/issues/actions write permissions | HIGH-PRIORITY REVIEW | Per-job permission map and source-backed justification for each write capability |
| EVD-009 | Astra target identity consistency | Workflow parser accepts legacy target labels; execution path uses conflicting node identities | HIGH-PRIORITY REVIEW | Approved target registry and one immutable target binding from parse through execution |
| EVD-010 | Supervisor dispatch and credentials | Supervisor has actions write; source includes downstream dispatch and credential-persistence behavior | HIGH-PRIORITY REVIEW | Dispatch allowlist, per-job permissions, credential-persistence rationale and signed-command validation evidence |
| EVD-011 | Gemini context provenance | Workflow allows caller-supplied ref/task/context paths and includes several bounded input controls | PARTIAL SOURCE CONTROL / PROVENANCE OPEN | Resolve and record immutable commit SHA, per-file digest, path allowlist and explicit advisory-only output classification |
| EVD-012 | Secret-hygiene regression gate | Test source exists; execution and required-check status unavailable | SOURCE PRESENT / EXECUTION UNKNOWN | Commit-bound test run, result URL/SHA and branch protection evidence |
| EVD-013 | Synthetic HMAC exception scope | Astra verification workflow contains a synthetic smoke value; hygiene test exception is file-level | FOLLOW-UP | Narrow exception to exact test fixture or generate ephemeral value; preserve reproducible test semantics |
| EVD-014 | Gemini API generation | Existing checkpoint records successful run `38940264004` and non-empty artifact, with marker mismatch | REQUEST/GENERATION VERIFIED IN PRIOR CHECKPOINT; MARKER UNVERIFIED | Read-only artifact/run provenance check if refreshed evidence is required; do not infer product qualification |
| EVD-015 | Repository-wide scanner clean status | No SAST/SCA/secret scan executed in this pass; alert endpoints unavailable | UNKNOWN | Evidence from each scanner and alert source, tied to immutable commit and scope |

## 4. Recommended sequence (technical recommendation; formal gates preserved)

1. **P0 — reduce controller authority exposure:** conduct a source-only per-job permission and issuer/target-binding review of `astra-chat-control.yml` and `astra-autonomous-supervisor.yml`. Do not activate, dispatch or execute control commands as part of this review.
2. **P0 — recover authoritative security evidence:** obtain owner-visible branch-protection and Security-tab evidence for `main` and the docs ref. Keep UNKNOWN statuses until evidence is available.
3. **P1 — establish reproducible scanner evidence:** define a commit-bound SAST/SCA/secret-scan/SBOM evidence format; scanner configuration and execution require the appropriate separate authorization.
4. **P1 — tighten evidence provenance:** bind workflow-generated reports to resolved commit SHA, selected file digests, workflow run ID and advisory-only status.
5. **P2 — reconcile canonical source registry:** extend source coverage by requirement IDs and dependencies after the high-risk workflows are reviewed. Keep the accepted Baseline 2.0 and existing contracts intact.

## 5. Scope and limitations

- Source/ref/blob identities above were retrieved live through the connected GitHub integration on 2026-10-16.
- Main tree snapshot used by Wave 02 is `b45324009ac3aa65322a702c28069b12190bc4b8`; the documentation branch has additional documents that are absent from main. Do not treat documentation-only records as merged into main.
- Branch comparison at this pass: DIVERGED, documentation ref ahead 1,649 / behind 10, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- No tests, scanners, qualification, provider/model calls, credential use, host/runtime inspection, installation, infrastructure changes, deployment, migration, merge, rebase or cherry-pick were performed.
- This registry is an index and evidence ledger, not a replacement for contracts, a security approval, or a clean security report.

## 6. Next bounded step

Read the exact full source and relevant permission context for `astra-chat-control.yml` and `astra-autonomous-supervisor.yml`; create a source-only per-job authority table with trigger, issuer check, token permissions, untrusted inputs, dispatch targets, credential lifetime, target binding and evidence gaps. Preserve both workflows and all branches unchanged during that review.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
