# MediaHub OS — Chat Context Archive (2026-10-31)

Status: DRAFT DOCUMENTATION RECORD; NOT MERGED.
Repository: https://github.com/VlDMlNSh/mediahub-os
Canonical documentation base: `docs/mediahub-chat-tree-map-20261012` at `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
Main snapshot checked: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.

## User direction and priorities
- Keep all meaningful engineering and research evidence in GitHub.
- Contour A Cloud Pool is the first priority; server hardware only after deployment and independent acceptance. Contour B follows Contour A acceptance.
- Research mature OSS before bespoke implementation.
- Preserve Baseline 2.0, historical IDs, issuer/capability controls and the separate authority boundaries of Jarvis, ASTRA A0 and MediaHub Product State Authority.
- GitHub-hosted ephemeral workers are the default; no owner-operated always-on server or public inbound listener as a prerequisite.
- No paid fallback, secret exposure, provider call, agent dispatch, merge or deployment without the relevant governance gates.
- Empty CI/review results mean NOT VERIFIED, not PASS.

## Governance and repository sources checked
- Bootstrap blob: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical map blob: `75f62685459ec99ebf8be478f4e9096cdb842b1d`; Contents API returned empty content, so no map body was inferred.
- Checkpoint blob: `fd312ded05dd1898bd36d776a9669bb02920720d`.
- Master Roadmap blob: `ea7e94e921045253f3e6494438e197c4bafae3a0`.
- Issue #301 is OPEN: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Issue #301 gates include A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy; accepted runner/workspace/network manifest; JSON Schema Draft 2020-12 meta-validation and positive/negative fixtures; independent schema review; hardened source-bound read-only workers; controlled dispatch with run/job/artifact evidence; separate promotion/merge/deployment gates.
- Canonical docs branch exists. Main HEAD and docs base were checked before archiving.

## Existing OSS governance inspected
Files on main:
- `oss/README.md`: blob `b8f25ad20bf922264971afeb5a3dbf87d004ba3f`.
- `oss/manifests/components.yaml`: blob `7141dd16e9ce9dba3440b1799a56e2ac4da4106d`.
- `architecture/COMPONENT-ARCHITECTURE-DECISIONS.md`: blob `42b2701f0d6a1014435e96118e41e33025dbff08`.
- `architecture/COMPONENT-INTEGRATION-BOUNDARY.md`: blob `d80f369ed126ac470ab60296559781e45cd203a4`.
- Reconciliation 2.3: blob `7fd870134f34a951fe872fe2d79a28554e24c5ca`.
- MH-20 architecture: blob `4a0b09976e80dac03ce9ab89fd767de3bd783100`.

Existing policy remains unchanged: upstream software is used only behind bounded adapters; MediaHub retains domain and authorization authority. Qualification requires immutable versions/digests, license review, provenance, SBOM, vulnerability scan, adapter contracts, negative tests, degraded/recovery/rollback tests and independent review. Temporal remains FUTURE_GATED. Kubernetes/K3s and Argo CD are reference-only. Telemetry is observational.

## Waves 490–492 recorded in this chat

### Wave 490 — Microsoft developer tooling
- VS Code recommended as the primary cross-platform workbench.
- Dev Containers selected for further evaluation.
- Codespaces optional and cost-gated; Copilot optional and policy-gated.
- Reuse existing Copilot instructions and agent profiles; do not create a second registry.
- PR #604: https://github.com/VlDMlNSh/mediahub-os/pull/604
- Branch `docs/wave490-microsoft-devtools-integration-research-20261031`; head `1b1bc26ad8ac0548a59f7930d027c706e192c60a`.
- Draft/open/unmerged; checks, runs and reviews were empty: NOT VERIFIED.

### Wave 491 — Dev Container toolchain inventory
- CI workflows were inventoried; most use Python 3.12, while specialized Claude FCC tooling uses Python 3.14.7.
- `requirements-dev.txt` had PyYAML/pytest ranges and no lockfile.
- A universal Dev Container was deferred pending dependency lock strategy, immutable base image digest/provenance, OS baseline, extension allowlist and optional tools profile.
- Core profile proposal: Python 3.12, Git/shell, PyYAML/pytest, non-root, narrow workspace, no secrets, no privileged mode, no Docker socket, no host network and no inbound listeners.
- PR #605: https://github.com/VlDMlNSh/mediahub-os/pull/605
- Branch `docs/wave491-devcontainer-toolchain-inventory-20261031`; head `6e3d039d114b84f861d279659c06bc4651225ca3`.
- Draft/open/unmerged; exact-head statuses, runs and reviews empty: NOT VERIFIED.

### Wave 492 — Mature OSS shortlist
Research report: https://github.com/VlDMlNSh/mediahub-os/pull/606
Branch `docs/wave492-mature-oss-research-shortlist-20261031`.
Head `b8f7c8b57a3c385738989c60020da081faabfb9d`; base `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
PR #606 is OPEN/DRAFT/UNMERGED; 3 files, 216 additions, 0 deletions. Compare: 3 commits ahead, 0 behind. Exact-head statuses, workflow runs and reviews empty: NOT VERIFIED.
Files reread and blob SHAs:
- Report: `33d90a16281e18a344e4a3343045f001f871b55c`.
- Map addendum: `7dc23a71f78991c8982bc5a4195fcaf1c73fcd7c`.
- Continuation addendum: `62c2b0e6bd399c719e79ee4e2b317426b22fccfc`.

Shortlist:
- P0 OpenHands Software Agent SDK: https://github.com/OpenHands/software-agent-sdk — investigate SDK/Agent Server/workspace only; exclude Automation Server/dispatcher and any second control plane.
- P0 Open Policy Agent: https://github.com/open-policy-agent/opa — offline policy evaluation only; cannot mint identities/capabilities or replace MediaHub authority.
- P0 Dagger: https://github.com/dagger/dagger — bounded build/test tasks only; not a replacement for GitHub Actions/controller/release authority.
- P0 Dev Containers Spec/CLI: https://containers.dev/ and https://github.com/devcontainers/cli — validate config, lockfiles, image provenance and safe developer environment.
- P1 GitHub Artifact Attestations/SLSA: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations and https://slsa.dev/ — provenance evidence, not correctness/acceptance.
- P1 OpenTelemetry Collector: https://github.com/open-telemetry/opentelemetry-collector — synthetic telemetry, redaction and allowlisted exporters; non-authoritative.
- Temporal stays FUTURE_GATED until a measured durable-workflow gap exists.
- Actions Runner Controller is not selected for current Contour A default: it manages Kubernetes-hosted self-hosted runners, not GitHub-hosted ephemeral workers.

No component was installed, integrated, qualified or accepted. No dependencies, secrets, provider calls, agent/controller dispatch, billing, merge or deployment were changed.

## Next bounded pass
1. Inspect OpenHands SDK at an immutable upstream commit/tag: provenance, license, dependencies, workspace/tool isolation, APIs and security advisories.
2. Inspect OPA at an immutable upstream commit/tag: provenance, license, dependencies, Rego evaluation API, policy bundles, tests and failure semantics.
3. Map both to Task Envelope, Agent Registry, Runner Registry, issuer/capability, evidence and audit contracts.
4. Produce threat models and non-executing integration plans.
5. Do not install either component or dispatch a live agent in that pass.
6. Keep all draft PRs unmerged until exact-head CI, review and governance evidence exist.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
