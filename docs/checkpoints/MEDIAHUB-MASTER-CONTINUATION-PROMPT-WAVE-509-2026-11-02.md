# MASTER CONTINUATION PROMPT — MediaHub OS / Wave 509
Version date: 2026-11-02
Repository: https://github.com/VlDMlNSh/mediahub-os

Continue the ongoing MediaHub OS engineering program across prior ChatGPT conversations. This is a continuation, not a new project. Do not discard, replace, or reinterpret accepted history. Use the repository's canonical records as the durable source of truth and reconstruct relevant context before acting.

## 1. First action on every /next

At the start of every /next, fetch and verify live GitHub state:
- main HEAD/ref/SHA and canonical docs branch HEAD/ref/SHA;
- Bootstrap, canonical map, current continuation checkpoint, Master Roadmap and Baseline 2.0;
- Issue #301 and governing Issues/PRs;
- PR heads, diffs, formal reviews, review threads, active rulesets and exact-head Check Runs;
- controller, child workflows, schemas/contracts, agent registries and executor manifests;
- SentinelX host inventory/capabilities/allowlist, if local execution is in scope.

Do not rely on stale SHAs in this prompt. Re-read current sources. If Contents API returns empty, fetch blob by Git blob SHA or raw content. Record SHA and source ref. Never claim a source was read if its content was not received and inspected.

Starting refs at Wave509 audit (revalidate before use):
- main: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7
- canonical docs branch at audit start: d9a289b9113f7567711b641a7017eb814d6c259d
- Wave508/509 docs PR branch: docs/wave508-pr-review-and-governance-revalidation-2026-11-02
- Wave509 code branch: contour-a/alamo-fcc-claude-hosted-runner-20261031 (legacy branch slug only; not runtime identity)

## 2. Source hierarchy and preservation of history

Read these first:
1. [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
2. [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
3. [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
4. [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/wave508-pr-review-and-governance-revalidation-2026-11-02/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
5. [Baseline 2.0](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md)
6. [Issue #301 — Contour A](https://github.com/VlDMlNSh/mediahub-os/issues/301)
7. [Issue #296 — Ollama/FCC/FreeLLMAPI route](https://github.com/VlDMlNSh/mediahub-os/issues/296)

The map, checkpoint and roadmap contain extensive historical Waves, design decisions, tests, failures, open PRs, blockers and prior chat synchronization records. Load their current complete content, not only the recent top entries. Inspect relevant source contracts and linked evidence for the chosen task. This prompt is not a literal transcript of every past chat; the repository is the durable archive for synchronized work. If a chat contains an owner decision not yet synchronized, preserve it in GitHub before relying on it.

Baseline 2.0 is the current accepted functional baseline. Keep Baseline 1.0 as historical provenance. Do not silently merge older requirements into Baseline 2.0 or alter accepted authority/governance without change control.

## 3. Binding terminology correction — Ollama

**Ollama is the sole canonical name of the local inference runtime.**
- “Alamo/Allamo” in earlier discussions meant the local Ollama runtime. It is not a separate product, service, endpoint, hostname, physical host or executor.
- Original owner instruction: [Issue #301 Wave338](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6326925941).
- Reaffirmation: [Issue #301 Wave509](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6568555691).
- Runtime = Ollama.
- Model = exact tag such as llama3.2:3b.
- Physical host = e.g. Voktors-Mini.Dlink (Mac mini 2018), only where fresh inventory confirms it.
- Client/integration = Claude Code → FCC/ECC → Ollama → selected model, only after route qualification.
- Cloud agent pool = separate GitHub-hosted worker/controller fabric.

Wave364/365 statements that interpreted Alamo as a distinct host/server are superseded. Preserve these documents as historical provenance and annotate them; never use those stale claims as the current architecture. Branch slugs and historical filenames containing the old term may remain as legacy Git history and are not runtime identities. Current source names/job IDs/artifacts must use Ollama.

## 4. Target runner architecture

Runner 1 candidate:
- Ollama local inference runtime;
- FCC/ECC integration;
- Claude Code client/executor;
- local-only, fail-closed, no Anthropic API, no paid API route, no paid proxy, no silent cloud fallback;
- exact version/checksum, endpoint/auth/network binding, model tag, host and route evidence;
- GitHub-hosted Ubuntu is an ephemeral job, not a persistent VM; a physical local host is a separate executor route requiring independent host ID/capability verification.

Runner 2 candidate:
- three Gemini roles plus approved tools such as mini-SWE-agent, Aider, OpenHands SDK and Goose;
- do not install Runner2 tools in Runner1;
- the current Gemini controller dispatches child jobs to separate GitHub-hosted Ubuntu runners; a shared persistent VM2 is not implemented by grouping roles in documentation;
- Gemini transport only through approved .github/workflows/gemini-batch-dispatch-controller.yml, never SentinelX, local Ollama, CLI, arbitrary scripts or another workflow.

Cloud pool must function without the local Ollama host or owner-operated always-on server. Local runtime availability cannot become a hidden dependency for Contour A cloud qualification.

## 5. Architecture and authority invariants

- Jarvis, ASTRA A0 and MediaHub Product State Authority are distinct. Do not mix permissions.
- ASTRA GOLD A0 owns authorized hybrid mission DAG decomposition, admission and cross-route lifecycle where specified by accepted contracts.
- Model runtimes, agents and providers are compute surfaces, never state authorities.
- Enforce issuer, capability, delegation, expiry, revocation and destination admission.
- Maintain one authoritative queue/claim/lease/retry/cancel/recovery owner per route; no ambiguous or duplicate claims.
- Every route declares data classification, locality/egress, upstream/provider identity, authentication and cost/billing class, quota, model, runtime version, host, expiry and evidence requirements.
- Fail closed for unknown identity, policy, source SHA, model/provider, cost, quota, auth, capability, cancellation or evidence.
- No credential values in repository content, workflow prompts, logs, test fixtures, artifacts or final responses.
- Never use a paid fallback when a route requires non-paid execution. Do not bypass provider login, terms, quotas or access controls.
- Keep cloud provider paths (e.g. FreeLLMAPI/OpenRouter) distinct from local Ollama and Anthropic-hosted APIs.

## 6. Gemini controller / multi-agent protocol

- Chat /next is not itself a GitHub Actions event.
- Do not say Gemini agents were dispatched unless a trusted controller run and all correlated child run/job IDs exist.
- Use only the approved controller workflow. Verify controller source SHA, main trust, admission variable MEDIAHUB_GEMINI_BATCH_ENABLED, exact secret names in source (MEDIAHUB_GITHUB_TOKEN, MEDIAHUB_DISPATCH_HMAC_KEY) and provider-key bindings without reading secret values.
- Verify minimum token scope and HMAC separation; never pass GitHub transport tokens to a model or child.
- Controller probe is non-launching; it is not an agent batch. PR no-op success is not inference or dispatch.
- Before agent mode, close independent security review, exact-main CI, branch governance, secret/variable metadata, trusted-main no-secret probe and A0/R-06/lease/recovery/schema prerequisites.
- If permitted, use distinct roles: Agent1 implementation/research; Agent2 independent contract/test review; Agent3 security/authority/provenance. Inspect controller contract to confirm those exact instructions are actually accepted.
- Record controller run ID, target SHA, all child workflow/run/job IDs, terminal states, artifacts/digests, test evidence and independent review.
- Never use the local Ollama host for Gemini transport.

## 7. Claude Code / local Ollama protocol

- Do not assume a local host is available because it is listed.
- Recheck exact SentinelX host ID, operational state, capabilities, allowlist, free slot, OS/architecture, executable versions and working directory.
- Do not target disabled hosts or bypass plan/allowlist constraints.
- Before task execution, verify Ollama API reachability, exact model tag, FCC version/config, auth enforcement, actual upstream, cost/billing terms, no paid/Anthropic fallback and network egress.
- Distinguish model-only inference from FCC request, Claude Code tool execution and a completed bounded engineering task. These are separate evidence levels.
- A /v1/models or /health HTTP 200 does not prove auth or task success.
- Do not send Claude tasks to a local host until all permission/route gates pass. If blocked, mark NOT RUN and continue safe source work.

## 8. PR / CI / review / merge governance

- Active main ruleset last observed: MediaHub-main-autonomous-merge, ID 26108066, enforcement active. Re-fetch it before action.
- Required contexts last observed: Astra Cloud Runtime Validation, Astra Verify, AI Factory verification, provider contract verification, Gemini workflow contract validation (Wave 284).
- Check CI on exact latest PR head SHA, not a prior commit or branch base.
- Empty CI/review result means NOT VERIFIED, not PASS.
- Formal independent review requires an actual submitted GitHub Review with state APPROVED by an independent reviewer. A comment containing “APPROVED” is not a formal review.
- Never merge if required contexts missing, review gates open, conflicts/untrusted sources exist or exact-head checks are unknown.
- Verify ancestry/no data loss before rebase/cherry-pick/merge; re-read files and verify blobs after every change.
- Keep implementation PRs and canonical documentation PRs separate when appropriate.
- Separate design, implementation, test execution, verification, qualification, release, deployment and acceptance.

## 9. Wave509 starting snapshot — revalidate all of it

At the 2026-11-02 audit:
- main: f0448f28c7cfa61e4450c38529f09afbfdbbc7c7.
- canonical docs branch: docs/mediahub-chat-tree-map-20261012 at d9a289b9113f7567711b641a7017eb814d6c259d at audit start.
- PR #610: Ollama runner refactor on legacy branch contour-a/alamo-fcc-claude-hosted-runner-20261031. New workflow .github/workflows/mediahub-ollama-fcc-claude-runner.yml, renamed test tests/test_mediahub_ollama_fcc_runner_contract.py; test update commit 961ad2018ed6b702f501c03511596e519742d9e4 was the latest observed during work. Re-fetch current branch head and exact CI; not merged/qualified.
- PR #620: Wave508/509 documentation draft on docs/wave508-pr-review-and-governance-revalidation-2026-11-02, targeting canonical docs branch. Re-fetch current head, checks and review.
- PR #613: five required contexts success on SHA 237948e03088c3ea43608b0c284327c552d34f4b, but no formal review at Wave508 check.
- PR #619: draft; zero exact-head check runs/reviews at Wave508 check.
- Issues #296 and #301 remain governing; #296 updated to Ollama local model-routing path; #301 has owner terminology reaffirmation.
- SentinelX: one operational host Voktors-Mini.Dlink, host_5f7264034bdf0b51; Free plan one active slot / zero available; mh-dev-01 and mh-dev-02 disabled.
- Gemini dispatch NOT RUN. Local Claude/Ollama task NOT RUN. No secret values read, no model/provider inference, no installation, no merge/deployment in Wave509.
- Contour A NOT ACCEPTED. Contour B GATED.

## 10. Required approach in this new chat

1. Re-read and cross-check all sources in section 2; load relevant historical Waves and prior PR evidence so no work is duplicated.
2. Confirm latest main/docs refs, PR heads, Issue status, controller/runner blobs, ruleset and SentinelX inventory.
3. Search active code/config/contracts for legacy Alamo/Allamo strings. Distinguish historical filenames, audit records and superseded assertions. Correct current semantics, preserve history; do not blindly replace strings across archives.
4. Finish Wave509 verification. For PR #610, run exact runner contract tests, verify current workflow/test have no legacy alias, confirm all five required CI contexts at exact head and obtain genuine independent security review. For PR #620, verify documentation readback, link integrity, exact-head CI and independent review before integrating canonical docs.
5. Continue the highest-priority open Issue #301 / Master Roadmap item, one bounded pass at a time. Reuse mature components before building custom ones.
6. Create a dated report, map addendum, checkpoint and roadmap update as needed. Include refs/SHA, blob SHA, CI run IDs, reviewer state, executor IDs, artifact digests, tests, blockers and next step.
7. Never invent missing history. Search repository checkpoints/map and synced chat artifacts; disclose unsynced chat history that is inaccessible rather than fabricating it.
8. End each pass with current canonical map/checkpoint/report links and next bounded action. When owner action is required, finish with a bold all-caps instruction block with precise steps and copyable text.

## 11. Status vocabulary

Use evidence-backed states only: PLANNED, DISPATCHED, RUNNING, SUCCEEDED, VERIFIED, QUALIFIED, ACCEPTED, NOT RUN, BLOCKED, FAILED, NOT VERIFIED. Distinguish lifecycle stages. No runtime success, qualification or acceptance without exact evidence.

**Immediate next step:** Re-fetch PR #610's actual current head and exact-head checks after the Ollama rename; verify workflow/test and independent review; in parallel validate PR #620 documentation changes. Do not dispatch Gemini, run live Ollama/FCC/Claude, merge or deploy until applicable gates demonstrably pass.
