# MediaHub OS — Jarvis Upstream Candidate Intake, Wave 22

- Date: 2026-10-17
- ID: MH-JARVIS-INTAKE-22
- Contour: A — Developer Fabric
- Status: READ-ONLY CANDIDATE REVIEW / REUSE-FIRST / NO SELECTION OR INSTALLATION
- Scope: research public upstream candidates after Wave 21, compare product fit with MediaHub Jarvis's umbrella architecture, and define the next controlled intake step.
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Decision summary

The user's direction is consistent with the Canonical Component Manifest 2.0: prefer reuse over reimplementation when capability fit, authority boundaries, immutable provenance, licensing, security and qualification gates pass.

Wave 21 established that “Jarvis” in MediaHub's blueprint is an umbrella architecture label; it did not identify one exact upstream distribution. This pass finds a stronger named candidate worth intake: `PersonalJarvis/PersonalJarvis`. It is a candidate for the personal-agent/desktop interaction layer, not an automatic replacement for MediaHub's engineering control plane, ASTRA A0, task authority, evidence pipeline or product-state boundaries.

Recommendation: advance Personal Jarvis to a bounded, read-only repository intake and capability crosswalk; evaluate OpenHands Software Agent SDK separately as an execution-engine candidate. Keep the older `sukeesh/jarvis` CLI project out of the primary shortlist because its own README describes a “Personal Non-AI Assistant” with command-line utility tasks, which does not match the intended autonomous engineering fabric.

No candidate is selected, pinned, installed, qualified or deployed by this report. The exact owner-intended upstream identity remains unresolved until the owner confirms whether Personal Jarvis is the intended repository or provides the preferred URL.

## 2. Public source evidence reviewed

### Candidate A — Personal Jarvis

- Repository: https://github.com/PersonalJarvis/PersonalJarvis
- README: https://github.com/PersonalJarvis/PersonalJarvis/blob/main/README.md
- Architecture overview: https://github.com/PersonalJarvis/PersonalJarvis/blob/main/docs/architecture-overview.md
- Security policy: https://github.com/PersonalJarvis/PersonalJarvis/security
- Licensing details: https://github.com/PersonalJarvis/PersonalJarvis/blob/main/docs/licensing.md
- Observed project scope: desktop/personal agent application; multi-agent coding workspace; voice; browser and desktop interaction; plugin/MCP integration; model/provider configuration; local-file knowledge wiki; routines; CLI and headless-server mode.
- Observed platform claim: Windows, macOS and Linux.
- License note from the project's licensing document: current `main` is Apache-2.0 from the 2.0.0 line; releases through 1.6.0 remain MIT. The exact version/commit and bundled third-party license inventory must be pinned and reviewed before reuse.
- Security-policy note: the project describes local data storage, tool risk tiers and private vulnerability reporting. These are upstream design claims, not independent security verification. Its broad computer-use capabilities and configured provider access require an isolated adapter and explicit tool allowlists.
- Fit assessment: HIGH for candidate review of personal-agent UX, voice, local memory, provider adapters and desktop interaction; UNKNOWN for full MediaHub engineering-control-plane compatibility; TARGET QUALIFICATION OPEN.

### Candidate B — OpenHands Software Agent SDK

- Repository: https://github.com/OpenHands/software-agent-sdk
- README: https://github.com/OpenHands/software-agent-sdk/blob/main/README.md
- License: https://github.com/OpenHands/software-agent-sdk/blob/main/LICENSE
- Agent Server README: https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/README.md
- Observed project scope: Python SDK, TypeScript client, agent server, tools, conversations, workspaces, events and REST/WebSocket APIs; local or ephemeral workspaces are supported.
- Observed license: MIT in the fetched repository LICENSE.
- Fit assessment: HIGH as a developer-agent execution substrate candidate; LOW as a standalone replacement for the full Jarvis umbrella UX and MediaHub mission authority. The upstream server documentation describes a default bind address of `0.0.0.0` and workspace filesystem access; any eventual deployment requires network binding, authentication, workspace isolation and secret handling to be explicitly hardened.
- Compatibility gate: its current package metadata declares Python `>=3.12`; verify each intended target's runtime capability before any admission. No target qualification is implied.

### Candidate C — legacy Jarvis CLI

- Repository: https://github.com/sukeesh/jarvis
- README: https://github.com/sukeesh/jarvis/blob/master/README.md
- License: https://github.com/sukeesh/jarvis/blob/master/LICENSE
- Observed project scope: command-line personal assistant with utility tasks and optional voice; README explicitly labels it a “Personal Non-AI Assistant”.
- Observed license: MIT.
- Fit assessment: LOW for MediaHub's autonomous engineering Jarvis; retain only as a historical/name-collision reference, not a primary implementation candidate.

## 3. Proposed composition

Keep MediaHub Jarvis as the architecture and contract owner. Reuse candidate repositories as bounded subsystems behind MediaHub-owned interfaces:

1. **Jarvis personal-agent layer:** evaluate Personal Jarvis for voice, desktop UX, personal memory and provider-facing user interactions.
2. **Engineering agent execution:** evaluate OpenHands SDK/Agent Server for isolated code-task execution, ephemeral workspaces, tools and result streaming.
3. **Mission coordination and durable lifecycle:** keep the accepted MediaHub/Jarvis-to-ASTRA A0 boundaries authoritative. Any scheduler or automation component must be evaluated against the existing single-lifecycle-owner decision before admission.
4. **Evidence and promotion:** MediaHub-owned task envelope, source pin, artifact provenance, independent verification and promotion gates remain authoritative.
5. **Product authority:** neither upstream gains canonical MediaHub product-state mutation authority. Product work remains Contour B-gated on independent Contour A acceptance.

This composition intentionally avoids treating one public application as the entire MediaHub architecture. It also avoids rewriting voice, UI, agent execution or workspace primitives before the source audit establishes a real gap.

## 4. Repository admission checklist

Before a component is admitted:
- exact upstream URL, default branch and immutable commit/tag;
- release and maintenance posture;
- full license/NOTICE/third-party license inventory and redistribution obligations;
- dependency lock, SBOM, provenance/signature evidence and vulnerability/advisory review;
- data-flow map for prompts, files, voice, screenshots, telemetry, logs and provider requests;
- tool/desktop/network/filesystem permission map and prompt-injection boundary;
- authentication, secret custody, API binding and workspace isolation;
- platform/resource compatibility for Mac mini 2018/macOS, Mac mini 2011/Linux and remote video server;
- MediaHub interface and lifecycle-authority crosswalk;
- removal/replacement plan;
- authorized tests, negative-path tests, resource benchmarks and independent qualification.

The component manifest's 17-point qualification gate remains controlling. This report closes none of those gates.

## 5. Status and next step

- Personal Jarvis: CANDIDATE FOR READ-ONLY INTAKE; exact immutable source pin OPEN.
- OpenHands Software Agent SDK: EXECUTION-SUBSYSTEM CANDIDATE; exact immutable source pin and target compatibility OPEN.
- `sukeesh/jarvis`: LOW-FIT / NOT SHORTLISTED FOR PRIMARY ADOPTION.
- Exact owner-intended Jarvis repository: UNKNOWN until the source identity is confirmed.
- Installation, tests, qualification, host/runtime inspection, provider calls, credentials, infrastructure changes and deployment: NOT PERFORMED.

Next bounded pass: fetch the exact source files at pinned refs for the selected candidate, build a module-to-MH-01…MH-25 contract crosswalk, record dependency/license/security findings, and preserve the three-server topology. Runtime activity remains behind separate explicit authorization.

## 6. Source links

- MediaHub Canonical Component Manifest 2.0: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-github-component-final-manifest-2.0.md
- Wave 21 reuse decision: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-JARVIS-REPOSITORY-REUSE-AND-INTEGRATION-DECISION-WAVE-21-2026-10-16.md
- Wave 21 map addendum: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-21-2026-10-16.md
