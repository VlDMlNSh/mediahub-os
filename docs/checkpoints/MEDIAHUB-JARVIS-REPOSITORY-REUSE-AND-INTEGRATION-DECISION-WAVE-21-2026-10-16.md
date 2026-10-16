# MediaHub OS — Jarvis Repository Reuse and Integration Decision, Wave 21

- Date: 2026-10-16
- ID: MH-JARVIS-REUSE-21
- Contour: A — Developer Fabric
- Status: DOCUMENTARY DECISION / REUSE-FIRST / EXACT JARVIS UPSTREAM UNRESOLVED / NO INSTALLATION
- Scope: explain why a public repository called Jarvis has not been installed or added as the project implementation, and establish the repository-intake path without changing the project architecture.

## 1. Direct answer

MediaHub OS should reuse an existing repository where it satisfies the required capability and governance gates. Jarvis itself is the owner-defined umbrella architecture for engineering orchestration, project memory, planning, bounded execution, independent verification and release preparation. The current source set treats Jarvis as an architecture label, not as the identity of one already-selected upstream repository.

Therefore, the project is not intended to reimplement every subsystem from scratch. It also must not install an arbitrary repository solely because its name is Jarvis. Several unrelated public repositories use that name, and the current owner blueprint does not identify one exact upstream URL, release/tag or immutable commit as the intended Jarvis implementation.

## 2. Source evidence

| Source | Ref / SHA | What it establishes |
|---|---|---|
| Jarvis blueprint gap reconciliation, historical path `MEDIAHUB-ASTRO-BLUEPRINT-GAP-RECONCILIATION-01.md` | docs branch / `39720b11e5e6777b86ffd71e0fec1214982e0d95` | Jarvis is the umbrella architecture; ASTRA is a candidate execution/queue/evidence subsystem; reuse must be selective and authority boundaries remain |
| System Passport v3 | docs branch / `2b5d81236b85d44d284015cfb02d9401ab0e7482` | Jarvis is a working architecture label, not evidence of a deployed runtime or a renamed repository |
| Canonical Component Manifest 2.0 | main / `45988bf9da202c9597d0ca2de50e92e5c2e6ed55` | Reuse is preferred when a capability gap is evidenced, provenance/version is pinned, authority boundaries are preserved, qualification evidence is attached and replacement is feasible |
| Jarvis blueprint §16 repository snapshot | report SHA above | Seven public candidates were inventoried for subsystem roles; they were discovery candidates, not selected or qualified Jarvis upstreams |

The seven previously inventoried candidates were Temporal Server, LangGraph, Microsoft Agent Framework, Pydantic AI, OpenHands application, OpenHands Software Agent SDK and AutoGen. They solve different subsystem problems; they are not interchangeable complete Jarvis distributions. The report recommends avoiding duplicate queue/lifecycle owners and comparing OpenHands application versus SDK before selecting either.

## 3. Why no Jarvis repository was installed or added as the implementation

1. **Identity ambiguity:** the source set defines Jarvis as an umbrella architecture but supplies no exact upstream repository identity for a single Jarvis distribution.
2. **Capability mapping:** a repository must be mapped to specific Jarvis capabilities and interfaces; name similarity alone supplies no architecture fit evidence.
3. **Lifecycle ownership:** ASTRA already has workflow, claims, leases, scheduling and evidence contracts. A second scheduler/queue could create conflicting lifecycle authority.
4. **Security and data boundaries:** agent runtime, tool permissions, filesystem/network access, secret handling, provider egress and product-state authority require review before admission.
5. **Reproducibility and legal posture:** exact immutable commit/tag, license scope, transitive dependencies, provenance, release status, supported platforms and SBOM must be recorded.
6. **Deployment is a separate gate:** selecting a repository is distinct from adding it as a dependency, packaging it, installing it on one of the three servers, qualifying it or deploying it.

This is a deliberate source-selection and authority-control gap, rather than a requirement to write Jarvis from scratch.

## 4. Reuse-first integration sequence

1. **Identify the intended upstream:** exact repository URL and intended subsystem; if the owner means a particular repository named Jarvis, use that exact source as the initial candidate.
2. **Read-only intake:** repository metadata, default branch, immutable commit/tag, license files, release history, security policy/advisories, dependency manifests, supported OS/architecture and offline/local operation.
3. **Capability crosswalk:** map repository modules to Jarvis requirements and MH-01…MH-25 contracts; mark supported, adapter-required, gap, conflict or out-of-scope.
4. **Authority review:** one lifecycle owner; preserve MediaHub Product State Authority; isolate task state; define identity, lease, cancellation, retry/idempotency, provenance, quarantine and independent verification.
5. **Composition choice:** reuse the whole repository only if its boundaries fit; otherwise reuse selected modules behind adapters, or select a smaller SDK. Avoid duplicate schedulers and parallel state authorities.
6. **Reproducible package design:** immutable source pin, dependency lock, SBOM, license inventory, signed/provenance-bound artifact, per-target manifest, preflight, health gates, backup/rollback and evidence capture.
7. **Separate authorization gates:** source review and architecture proposal first; installation, tests, qualification, host inspection and deployment each require their applicable explicit authorization.

## 5. Three-server topology and deployment boundary

Keep the existing topology unchanged:
- Mac mini 2018 — macOS
- Mac mini 2011 — Linux
- Remote video server

A selected upstream does not automatically run on all three nodes. Each target needs a capability profile and compatibility evidence. Hosted ephemeral workers remain an additive execution lane where approved. Credentials, provider access and product-state authority remain controlled by the existing contracts.

## 6. Candidate decision

- **Jarvis as umbrella architecture:** retained as the working design direction.
- **Exact upstream repository called Jarvis:** UNKNOWN / owner source identity unresolved in the inspected repository documents.
- **Existing subsystem candidates:** reuse-first candidates already inventoried; exact pins and independent qualification remain open.
- **Implementation/install/deployment:** NOT PERFORMED.
- **Next bounded action:** establish the exact intended upstream repository identity, then perform read-only source intake and a module-to-contract crosswalk. No installation is part of this step.

## 7. Boundaries

This pass used GitHub source reads and documentary writes. No repository was cloned or installed; no test or model/provider was run; no credential was accessed; no host/runtime was inspected; no infrastructure, deployment or branch integration was performed.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
