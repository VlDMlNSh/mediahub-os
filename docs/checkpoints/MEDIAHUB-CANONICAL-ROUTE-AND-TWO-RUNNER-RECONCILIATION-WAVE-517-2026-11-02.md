# Wave 517 — canonical route conflict and two-runner status reconciliation (2026-11-02)

## Immutable refs
- Main HEAD: `af200c4323bd4cb7cfa4c47dab4accc10049d1ec`.
- Runner 1 branch: `feat/ollama-runner-ecc-wave-510`.
- PR #623 HEAD: `4ded07da6c262aa47fdca19289e5479a1580318d`; OPEN / READY / UNMERGED; 19 ahead / 0 behind; mergeable=true.
- Active ruleset: `MediaHub-main-autonomous-merge`, ID `26108066`.
- Issue #301 reconciliation comment: [6569293637](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6569293637).

## Exact-head CI
All 8 checks on `4ded07da6c262aa47fdca19289e5479a1580318d` completed SUCCESS:
- Runner workflow: [41389418223](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389418223)
- AI Factory: [41389418145](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389418145)
- Astra Cloud Runtime: [41389418174](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389418174)
- Astra Verify: [41389418114](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389418114)
- Provider contract: [41389418149](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389418149)
- Gemini workflow contract: [41389418133](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41389418133)

The five required ruleset contexts are all SUCCESS. PR #623 has zero formal reviews and zero inline review threads. Independent A3 review is NOT VERIFIED.

## Runner 1 — Ollama/FCC/Claude Code/ECC
Wave 516 updated Ollama to `0.40.13`, used the versioned release installer with checksum verification, and added FCC effective-config assertions for the local Ollama model, loopback endpoint, no fallbacks, no custom providers, no cloud credentials and no provider proxies. Contract tests reported 13/13 PASS on source target `830f5acb56153fe3bc9e1ebc651f78507c4f3aa9`.

The PR event intentionally skips live runtime operations. Ollama installation, model pull/inference, FCC authentication smoke, ECC live checkout and Claude Code invocation are NOT RUN. The workflow uses ephemeral `ubuntu-latest`; it does not provision a persistent Ubuntu runner or retain installed models. No disk/CPU/RAM capacity qualification exists.

## Binding canonical architecture conflict
The current canonical Bootstrap at blob `75f30750183efe8c6877368e9f0ada48f8e81ea7` states:
- §1: server 3 / Alamo is the separate local Claude Code executor path.
- §1A: Claude Code is to run on Alamo/server 3 only; never substitute Voktors-Mini, mh-dev-01, mh-dev-02 or a GitHub-hosted runner.
- §1A: FCC is conditional on verified permitted non-paid auth, upstream terms, billing class, version, egress and Alamo binding.
- §1C: Gemini controller gates remain mandatory; owner direction to operate autonomously does not waive security/governance requirements.

Wave 272 blob `010a6dcf08f76c05e9df7ba4a1d794f4b6602c58` and Wave 273 blob `0439b40a8f3252562ef1fcfc258eae5ab8a90e32` independently repeat Alamo-only Claude execution, no Anthropic API or paid routes/fallbacks, and fail-closed requirements for unknown auth/terms/egress/host binding.

The owner's requested Runner 1 topology includes Claude Code on Ubuntu. This changes a canonical hard constraint and requires an explicit reviewed architecture amendment and route qualification. It is not automatically authorized by a workflow implementation. Until then, Claude Code on Ubuntu is BLOCKED / NOT RUN. Do not bypass provider account controls, terms, paid-route restrictions or fallback restrictions.

Current host inventory:
- SentinelX operational host: `host_5f7264034bdf0b51`, `Voktors-Mini.Dlink`, macOS ARM64; not a qualified Ubuntu host.
- `mh-dev-01` and `mh-dev-02` are disabled/offline.
- No persistent Ubuntu runner was verified.

## Runner 2 — Gemini controller
Main controller dispatches three independent child workflows, each on a separate `ubuntu-latest` job allocation; controller itself also runs separately. This does not satisfy one shared second runner with three co-located isolated agents.

Gemini Agents 1–3 remain NOT RUN. No controller batch ID, child run/job IDs, provider calls or agent artifacts are claimed. Dispatch gates remain BLOCKED / NOT VERIFIED: independent security review, effective secret/variable presence and scope metadata, effective governance, and trusted-main no-secret probe.

## Current status
- Runner 1 source/contract CI: VERIFIED.
- Runner 1 live install/inference/authentication: NOT RUN.
- Persistent Runner 1 capacity: NOT VERIFIED.
- Claude-on-Ubuntu route: BLOCKED pending reviewed architecture amendment and route qualification.
- Runner 2 co-location: NOT IMPLEMENTED.
- Gemini dispatch: BLOCKED / NOT RUN.
- PR #623 independent review: NOT VERIFIED.
- Merge/deployment/qualification/acceptance: NOT performed.
- Contour A NOT ACCEPTED; Contour B GATED.

## Next bounded steps
1. Obtain independent A3 security review of PR #623.
2. Resolve the owner-requested Claude-on-Ubuntu change through a reviewed architecture amendment before any Ubuntu invocation; otherwise retain Alamo-only execution.
3. Split independently admissible Ollama/FCC/ECC work from the Claude executor gate.
4. Design Runner 2 as one host with three isolated agent sandboxes and controller-only transport credentials.
5. Re-run dispatch gates before any Gemini probe or batch.

## Canonical references
- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [Wave 515](MEDIAHUB-TWO-RUNNER-PLACEMENT-AND-GOVERNANCE-WAVE-515-2026-11-02.md)
- [Wave 516](MEDIAHUB-OLLAMA-PIN-AND-FCC-LOCAL-ROUTE-HARDENING-WAVE-516-2026-11-02.md)
