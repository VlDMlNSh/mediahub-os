# Wave 527 — exact-head CI correction and Runner 2 component assessment

Date: 2026-11-05  
Status: **SOURCE/CI RECONCILIATION VERIFIED / RUNNER 2 DESIGN NOT IMPLEMENTED / GEMINI NOT RUN / CONTOUR A NOT ACCEPTED**

## Immutable source refs

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Main HEAD: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical documentation HEAD: `d9a289b9113f7567711b641a7017eb814d6c259d`
- Bootstrap blob: `75f30750183efe8c6877368e9f0ada48f8e81ea7`
- Canonical map blob: `75f62685459ec99ebf8be478f4e9096cdb842b1d`
- Continuation checkpoint blob: `fd312ded05dd1898bd36d776a9669bb02920720d`
- Master Roadmap blob: `ea7e94e921045253f3e6494438e197c4bafae3a0`
- Active ruleset: `26108066` (enforcement active)

## 1. Required CI context correction

The five required ruleset contexts are present in workflows and run on pull requests targeting `main`. The main branch HEAD itself is not a valid substitute for checking PR-triggered contexts; three workflows are PR-only, while the exact main push check set is a different event surface.

PR #610 exact head `cac44b8a867945d4b544c3e46bd819bc42373f36` has all five required contexts SUCCESS:

| Required context | Check-run ID | Result |
|---|---:|---|
| Astra Cloud Runtime Validation | 125090595169 | SUCCESS |
| AI Factory verification | 125090595532 | SUCCESS |
| provider contract verification | 125090595204 | SUCCESS |
| Astra Verify | 125090595994 | SUCCESS |
| Gemini workflow contract validation (Wave 284) | 125090595758 | SUCCESS |

This corrects the previous Wave 526 chat assessment that implied the contexts were missing from the project. Their absence from the `main` push check-run list is expected for PR-only workflows; the exact PR evidence demonstrates the five contexts can be produced.

## 2. Runner 1 PR #610 disposition

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/610
- Exact head: `cac44b8a867945d4b544c3e46bd819bc42373f36`
- Base: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Compare against current main: 102 commits ahead, 2 behind; GitHub reports `mergeable=false`.
- The five required ruleset contexts and five additional Runner 1/preflight checks are SUCCESS.
- Formal review history contains only an owner-authored COMMENTED review; independent review is NOT VERIFIED. Inline review comments: 0.
- Runner job 125090679978 completed SUCCESS only because the PR no-op step succeeded. FCC/ECC checkout, capacity/install, Ollama, model inference, FCC, Claude Code and artifact upload steps were SKIPPED. Runtime is NOT RUN / NOT QUALIFIED.
- PR #610 is an older overlapping implementation candidate. Do not merge or cherry-pick its broad branch without file/commit-level reconciliation against the already integrated PR #623/current main.

## 3. Runner 2 and documentation PR state

- Main controller blob: `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- Agent 1/2/3 workflow blobs: `155a02159912ca371e6f826c51325ca269857aad`, `fff1820a6b97d379b23674f36bd62227b7d4dec2`, `781df56e8aa7c75ba453c08378611857862b2e44`.
- Each child workflow declares `runs-on: ubuntu-latest`; the controller dispatches independent workflow runs. Same-host Runner 2 co-location remains NOT IMPLEMENTED.
- PR #625 current head: `01efb5e6264b4cb84aee1d9c0c162be77cd1f264`, base canonical docs head `d9a289b9113f7567711b641a7017eb814d6c259d`; six changed files; formal reviews 0; inline review threads 0; exact-head checks 0. It remains a proposal, not accepted architecture.
- PR #631 head `71d82f96526a55714db9edfd202048d65c69afb9` and PR #632 head `d7ba6f1690cf36ea9af9eb36885979e20e2a2611` are Draft documentation proposals with zero exact-head checks. Their docs-branch base is not `main`; do not interpret absence of PR-to-main checks as a failed required CI result.
- Canonical map and checkpoint are stale relative to the working PR evidence: map currently indexes Wave 477; checkpoint begins at Wave 392. Master Roadmap currently begins at Wave 458. Working PR evidence through Wave 526 is not canonical until accepted.

## 4. Mature component reconnaissance for Runner 2

Reviewed upstream sources before proposing new implementation:

- Google’s official `google-github-actions/run-gemini-cli` is a maintained, verified GitHub Action for Gemini CLI integration. It is a candidate execution component to evaluate, not proof that it supports this project’s signed controller envelope, per-agent isolation or same-host lifecycle: https://github.com/google-github-actions/run-gemini-cli
- GitHub’s Agentic Workflows security architecture describes an action-runner VM with isolated containers, controlled egress, a trusted MCP gateway and an API proxy that retains LLM credentials outside the agent container: https://github.blog/ai-and-ml/generative-ai/under-the-hood-security-architecture-of-github-agentic-workflows/
- OpenHands documents Docker sandboxing as its recommended isolated runtime, while warning that a host-side manager with Docker socket access has elevated control over Docker: https://github.com/OpenHands/docs/blob/main/openhands/usage/sandboxes/docker.mdx

Assessment: reuse the official Gemini CLI integration if its auth and execution contracts fit; borrow the separation-of-duties pattern from GitHub Agentic Workflows. Do not add OpenHands as a dependency solely to obtain containers. A single GitHub-hosted job can be the host coordinator for three separately constrained containers, but the agent containers must not receive the Docker socket or controller transport/HMAC credentials. This is a design candidate only; no Runner 2 code was changed.

Required behavioral acceptance for a future Runner 2 implementation:
1. One admitted Ubuntu host per batch and one shared immutable target SHA.
2. Three separately isolated workspaces/containers with per-agent filesystem boundaries.
3. No controller/GitHub transport/HMAC credential inheritance into agent containers.
4. Per-agent provider credentials scoped only to the intended worker; no cross-agent access.
5. No Docker socket, host credential mounts, privileged mode or unbounded host filesystem access inside agents.
6. CPU/RAM/disk admission and bounded concurrency; deterministic cancellation/cleanup.
7. Signed task envelope, run/job/container IDs, artifact digests and commit provenance recorded.
8. Synthetic-key tests for signature tampering, workspace isolation, secret non-inheritance, resource exhaustion, cancellation, replay and partial-failure recovery.
9. Exact-head required CI and independent security review before any agent-mode dispatch.

## 5. Controller and supervisor disposition

- No Gemini controller dispatch was made in this pass; Agents 1/2/3: NOT RUN.
- No child run IDs, agent artifacts or provider inference evidence were created.
- Latest observed scheduled supervisor run `42076974507` remained PENDING when checked; its jobs endpoint returned no jobs. Execution status is NOT VERIFIED, not a healthy-running claim.
- No secret values were read. Secret/variable metadata and scope, trusted-main no-secret probe, and independent controller security review remain NOT VERIFIED.
- No server mutation, paid route, deployment, merge, qualification or acceptance occurred.
- Contour A NOT ACCEPTED; Contour B GATED.

## Next bounded step

Prepare a Runner 2 controller design and behavioral test contract on a dedicated implementation branch, after comparing the official Gemini CLI Action and GitHub Agentic Workflows primitives against the current signed-dispatch controller. Do not launch Gemini until effective governance, secret metadata, trusted-main no-secret probe and independent security review are verified.

## Canonical links

- Map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
