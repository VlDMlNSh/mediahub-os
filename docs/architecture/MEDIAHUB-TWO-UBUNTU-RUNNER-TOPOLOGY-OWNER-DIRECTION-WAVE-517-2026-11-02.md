# Wave 517 — owner-directed two-Ubuntu-runner target topology

Date: 2026-11-02

## Owner-directed placement

The target is two distinct Ubuntu runner roles:

| Runner | Co-located responsibilities | Explicit exclusions |
|---|---|---|
| **Runner 1** | Ollama local model runtime, FCC, Claude Code client and selected ECC skills/instructions | No Gemini controller or Gemini agents |
| **Runner 2** | One approved Gemini controller and Gemini Agent 1, Agent 2 and Agent 3 on the same admitted runner host per batch | No Ollama dependency and no transport through Runner 1 |

Other cloud agents may be onboarded later through a governed agent/provider registry and API adapters. Each added agent requires its own identity, credential scope, capability set, provider/model allowlist, quota, budget, data-egress policy, fallback rules and evidence contract.

The name “Alamo/Allamo” was an erroneous/legacy label for the local Ollama inference route, not a separate host identity. Historical documents remain intact as audit history; their Alamo/server-3-only binding is superseded by this owner direction. No new Alamo host is to be invented or provisioned.

## Runner 1 — Ollama / FCC / Claude Code / ECC

- Ollama is the local inference server; its endpoint must be loopback-only for the local smoke unless a separately approved network boundary exists.
- FCC is a client/proxy/control component, not a model. Claude Code is the coding-agent client, not the provider/model.
- ECC is selected, pinned guidance/instructions only unless a separate reviewed permission explicitly admits hooks/MCP/plugins.
- The effective FCC config must bind the exact `MODEL=ollama/<tag>` and loopback `OLLAMA_BASE_URL`; reject custom providers, provider proxies, all cloud provider credentials, model-tier overrides and model fallback lists in local-only mode.
- The local FCC bearer token remains separate from provider credentials. Never print it or package it in artifacts.
- Claude Code may execute only after the exact FCC authentication mode, upstream/provider identity, permitted non-paid/free billing basis, current terms, usage limits, egress, version and route are verified. Anthropic API auth, paid API routes, paid proxy backends and paid fallbacks are prohibited. Unknown route classification means Claude Code **BLOCKED / NOT RUN**, not a guessed free route.
- Ollama local inference can be verified independently of Claude Code route qualification.
- A PR contract job that skips install/model/auth/Claude execution proves source contract CI only; it is not installation evidence or qualification.

## Runner 2 — controller and three Gemini agents

- The controller and all three Gemini agents must execute on one admitted Ubuntu runner host for a batch.
- Use three distinct isolated agent containers/workspaces with separate output directories, filesystem boundaries, resource quotas and least-privilege credentials.
- Controller GitHub API token and dispatch HMAC key must never be inherited, mounted or copied into agent environments, prompts, logs or artifacts.
- Agent credentials, if required, are separately scoped and explicitly injected. Agent filesystem/network access and tools remain task-specific.
- All three tasks carry the same immutable target SHA and signed bounded task envelope. Preserve correlation IDs, run/container/job IDs, terminal statuses, artifact digests and independent verification.
- Before batch admission, measure vCPU, available RAM, free disk, filesystem capacity and actual runner labels/OS/architecture. Bound concurrency or refuse admission when resource thresholds are not met. Never infer three-agent capacity from a runner label alone.
- The existing main controller currently uses GitHub API dispatch to three separate child workflows, each with its own `ubuntu-latest` runner allocation. That implementation does **not** yet satisfy same-host co-location. A reviewed controller/worker architecture change and behavioral security tests are required before describing Runner 2 as implemented or dispatching the three-agent batch.
- No alternate transport, SentinelX Gemini launch, local Gemini CLI or ad-hoc dispatch script is permitted.

## Hosted versus persistent execution

“Runner 1” and “Runner 2” are logical placement roles, not proof of persistent infrastructure. Every execution must record whether it uses a GitHub-hosted ephemeral VM or a self-hosted/persistent Ubuntu VM, the actual runner name/ID, OS/architecture, vCPU, available RAM, free disk, labels, lifecycle and cleanup behavior.

A GitHub-hosted `ubuntu-latest` job is ephemeral. It does not retain a running Ollama daemon or model after the job. A workflow using it must reinstall or restore model artifacts through a digest-verified cache each time. Persistent self-hosted runner provisioning remains subject to the authoritative runner/workspace/network target manifest, resource admission, security isolation and governance. This direction does not authorize physical-server procurement or supersede Contour A cloud-pool priority.

## Current evidence at proposal creation

- PR #623 candidate branch `feat/ollama-runner-ecc-wave-510`, exact HEAD `4ded07da6c262aa47fdca19289e5479a1580318d`, contains the Runner 1 source contract.
- Workflow blob `12b684bbd3d475d64cac7e37bbaf64c65ce40529`; test blob `a3cf0c8fffbe5fd049144619d388354b4704b1d8`.
- Exact-head CI on that SHA: all eight checks SUCCESS, including the five required main-ruleset contexts. The PR-event runner job skipped every live install/runtime step; Ollama installation, model inference, FCC auth and Claude invocation remain NOT RUN.
- Main controller blob `0a1246f6755020faf8b7e48d07bfff790bbaece3` dispatches three separate child workflows, each with its own Ubuntu hosted runner. Same-host Runner 2 co-location is NOT IMPLEMENTED.
- SentinelX active host `host_5f7264034bdf0b51` is macOS ARM64 `Voktors-Mini.Dlink`; it is not an Ubuntu runner. Desktop Commander lists `mh-dev-01` and `mh-dev-02` offline. No persistent Ubuntu runner was verified.
- PR #623 has zero submitted formal reviews and zero inline threads. Independent security review is NOT VERIFIED.
- Gemini Agents 1/2/3: NOT RUN. Controller live dispatch remains BLOCKED pending independent security review, secret/variable presence and scope evidence, trusted-main no-secret probe and all existing governance gates.

## Required implementation sequence

1. Amend the controller to run the three isolated agent sandboxes on one admitted Runner 2 host without exposing controller credentials.
2. Add behavioral tests for cross-container secret isolation, filesystem boundaries, network allowlists, shared immutable SHA, replay prevention, cancellation, resource admission and evidence completeness.
3. Resolve the Runner 1 owner-approved non-paid FCC/Claude route and preserve Ollama-only fail-closed behavior.
4. Verify actual Ubuntu runner capacity and lifecycle; do not provision or label unknown hosts.
5. Complete independent review and all existing CI/governance/probe gates.
6. Only then run the bounded live Runner 1 and Runner 2 qualification passes and record exact run/job/container/artifact IDs and digests.

## Status

**PROPOSED / NOT IMPLEMENTED / NOT QUALIFIED / NOT ACCEPTED.**

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).  
Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md).  
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301.  
Runner 1 code candidate: https://github.com/VlDMlNSh/mediahub-os/pull/623.
