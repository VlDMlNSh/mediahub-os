# MediaHub OS — Reuse-First Upstream Discovery Gate, Wave 23

- Date: 2026-10-17
- ID: MH-REUSE-FIRST-GATE-23
- Contour: A — Developer Fabric
- Status: NORMATIVE PROCESS PROPOSAL / DOCUMENTARY / IMPLEMENTATION UNCHANGED
- Canonical component authority: [Canonical Component Manifest 2.0](mediahub-github-component-final-manifest-2.0.md)
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Purpose and decision

This pass formalizes the owner's stated operating principle:

**Reuse First — Discover → Verify → Compare → Integrate → Extend.**

Before starting each new development stage or implementing a capability, perform and record a GitHub-first discovery pass. The default is to reuse a stable, maintained, license-compatible project that already provides the required capability. New implementation is justified only by a documented gap, integration adapter, MediaHub-owned contract/authority, or project-specific logic that upstream projects do not provide.

This is a development process gate, not authorization to install software, execute code, run tests, use credentials, change infrastructure, or deploy.

## 2. Mandatory stage-entry gate

Every new development stage starts with a Component Discovery Record (CDR). No implementation ticket should be marked READY until the record contains:

1. Capability statement and acceptance criteria, mapped to MediaHub architecture/contract IDs.
2. Search date, exact GitHub queries, repository URLs, branches/tags/immutable SHAs and reviewed source files.
3. Existing manifest matches, existing repository reuse options, official upstream docs, SDKs, libraries, APIs and interoperable implementations.
4. Candidate comparison: functional coverage, maintenance/release cadence, issues/advisories, license/redistribution, dependencies, provenance, platform/resource support, data handling, security boundary, integration cost, exit/replacement path.
5. Evidence-backed decision for each candidate: reuse, adapter, extend upstream, defer, reject, or implement a missing capability.
6. Explicit gap statement explaining which required behavior remains uncovered by existing eligible projects and why the gap cannot be closed by configuration, composition or an adapter.
7. Required target/qualification gates and any blocked unknowns.
8. Reviewer, source pins, evidence links and decision date.

A missing CDR is a stage-entry blocker. A completed search does not automatically approve a dependency.

## 3. GitHub-first discovery procedure

For every capability:

- Search GitHub code/repositories/releases and official upstream documentation using capability terms, known standards, language/runtime and integration protocol; search both exact names and synonyms.
- Check the canonical component manifest and the machine-readable admission subset before adding a new dependency.
- Check the repository's actual source, default branch, latest stable release, tags/commit history, license files, security policy/advisories, dependency lockfiles, release workflow, supported platforms and known limitations.
- Prefer official upstream sources and immutable revision pins. Treat README claims, stars and repository activity as leads, not proof of operational stability.
- Compare at least one existing implementation when credible candidates exist; when no credible candidate is found, preserve the queries/results and document why.
- Consider composition of multiple mature components before building a bespoke subsystem.
- Preserve a negative result: “no suitable component found” requires recorded queries, candidate exclusions and the precise capability gap.

A search result or source review is documentary evidence only. Running a project, installing it, exercising tests, benchmarking, qualification or deployment requires its own applicable authorization and target gates.

## 4. Reuse decision hierarchy

Use the first suitable option:

1. **Already selected and qualified component** — use within its documented boundary.
2. **Existing manifest component with compatible target profile** — complete its applicable qualification and admission.
3. **Maintained upstream project with matching capability** — evaluate exact release and wrap it behind a MediaHub-owned adapter.
4. **Composable set of existing projects** — define contracts and authority boundaries between them.
5. **Extension/fork** — only when configuration, plugin API or a small upstream contribution cannot close the gap; preserve upstream provenance and an update/rebase strategy.
6. **New implementation** — only after a written gap analysis shows eligible existing projects cannot satisfy the required contract, safety boundary, target, license or operational constraints.

“Stable” must be evidenced by a release/tag, maintenance signals, reproducible source identity, security posture, compatibility and qualification evidence appropriate to the risk. Popularity alone is insufficient.

## 5. Explicitly preserve MediaHub-owned responsibilities

Reuse does not transfer MediaHub authority. Third-party components remain behind MediaHub-owned interfaces for:
- domain models and public contracts;
- mission, identity, authorization and policy;
- canonical product state and state mutation;
- user-data/privacy boundaries;
- recovery/update/release authority;
- evidence, provenance, audit and production admission.

For the Jarvis workstream, Personal Jarvis remains a personal-agent/desktop candidate and OpenHands Software Agent SDK remains an execution-subsystem candidate. Neither is approved as the complete Jarvis implementation. Continue with source-pinned intake and module-to-contract crosswalk before selecting either.

The three-server topology remains unchanged: Mac mini 2018/macOS, Mac mini 2011/Linux and the remote video server. Hosted execution may be considered only as an additive lane under the existing target-manifest and authority gates.

## 6. Exceptions and implementation readiness

An exception to the reuse-first order requires a recorded rationale tied to one or more of:
- no suitable maintained/licensed upstream exists after a recorded search;
- upstream violates a canonical security, privacy, authority or data-residency contract;
- target platform or resource constraints make it ineligible;
- integration or lifecycle semantics cannot be safely adapted;
- measured capability evidence proves a material gap;
- upstream license or provenance prevents permitted use.

The exception record must identify the exact missing behavior, candidates reviewed, evidence, alternatives and replacement path. Product strategy or an owner's explicit decision may govern business-priority exceptions; technical convenience alone is insufficient.

This policy does not bypass the Canonical Component Manifest 2.0 17-point qualification gate. Existing component presence, source availability or upstream tests alone do not establish MediaHub production readiness.

## 7. Wave 23 outcome and limitations

- Reuse-first is now expressed as a per-stage discovery gate and an implementation-readiness checklist.
- The current manifest already states that Astra must prefer reuse over reimplementation; Wave 23 operationalizes that rule before each development stage.
- The current YAML is an admission subset, not a full catalogue; its scope declaration and omission semantics remain authoritative.
- No canonical component selection was changed. No component was installed, cloned, executed, tested, qualified or deployed.
- The canonical map's Contents API retrieval is still empty for the large file; this report is linked from a separate navigation addendum rather than replacing the canonical map.

## 8. Next action

Apply this CDR gate to the next implementation-bound stage. First complete pinned source intake and module-to-contract crosswalk for Personal Jarvis and OpenHands SDK; reconcile each candidate against the canonical manifest, exact target roles, A0/R-06 constraints and the three-server target manifest. Only then prepare a narrowly scoped integration proposal.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
