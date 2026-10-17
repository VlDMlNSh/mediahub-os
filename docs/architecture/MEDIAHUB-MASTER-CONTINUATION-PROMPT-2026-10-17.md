# MediaHub OS — Master Continuation Prompt for a New Chat

- Created: 2026-10-17
- Repository: `VlDMlNSh/mediahub-os`
- Purpose: resume engineering in a new ChatGPT conversation while retaining a durable, auditable link to the complete project history, decisions, PRs, issues, evidence and checkpoints.
- Status: continuation contract; the GitHub repository remains the source of truth.

## 1. Start here — mandatory source order

Before taking action, fetch the current GitHub refs and inspect their live state. Prior chat summaries, this prompt, cached SHAs and old screenshots are navigation aids only.

1. [Project map](MEDIAHUB-CHAT-TREE-MAP.md) — architecture index, domain routes, history and cross-links.
2. [Bootstrap instruction](MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md) — mandatory protocol, decision rights and safety boundaries.
3. [Current continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md) — latest recorded handoff; inspect the latest dated/wave entry and its evidence.
4. [Master Development Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md) — locate the next open roadmap item and dependencies.
5. Baseline 2.0 at `docs/checkpoints/mediahub-functional-baseline-2.0.md` on the current `main` ref — canonical functional target. Baseline 1.0 is historical provenance.
6. Open and recently closed issues, PRs, commit diffs, workflow runs and review comments related to the next roadmap item. Reconcile actual state with checkpoint claims.
7. Read the domain's primary contracts and evidence registers before implementation.

Canonical refs at handoff:
- Documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Working audit branch: `docs/free-agent-pool-secret-audit-wave44-20261017`
- Current audit PR: [#320](https://github.com/VlDMlNSh/mediahub-os/pull/320), source-audit branch against documentation branch. Its live state must be queried at session start.
- Related continuation/audit PR: [#319](https://github.com/VlDMlNSh/mediahub-os/pull/319), live state must be queried.
- Gemini agent PRs: [#317](https://github.com/VlDMlNSh/mediahub-os/pull/317), [#318](https://github.com/VlDMlNSh/mediahub-os/pull/318).
- Cloud multi-agent router ADR, Wave 42: [document](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MEDIAHUB-CLOUD-MULTIAGENT-ROUTER-ADR-WAVE-42-2026-10-17.md).
- GitHub Actions-only Cloud Router ADR, Wave 45: [document](MEDIAHUB-GITHUB-ACTIONS-ONLY-CLOUD-ROUTER-ADR-WAVE-45-2026-10-17.md).
- Provider key-reference/free-agent pool audit, Wave 44: [document](../checkpoints/MEDIAHUB-API-SECRET-REFERENCE-AND-FREE-AGENT-POOL-WAVE-44-2026-10-17.md).

## 2. Continuity and history preservation contract

Treat project history as four linked evidence layers:

1. **Conversation history** — the original ChatGPT conversation and any owner-supplied export/transcript. A new chat cannot assume automatic access to the complete transcript of another chat. If the original conversation is available to the user, preserve it through ChatGPT's export/share facilities or an owner-provided transcript, then archive a sanitized copy in a dedicated history path after checking privacy and secret exposure. Never store raw credentials, private tokens, personal account data or sensitive conversation content in Git.
2. **Decision history** — ADRs, approved contracts, baseline revisions and explicit owner directions in GitHub. Preserve historical decisions; record superseding decisions as dated addenda with provenance.
3. **Implementation history** — commits, PRs, issue timelines, workflow run URLs, review comments and changed-file diffs. Link exact evidence instead of copying mutable summaries as if they were source.
4. **Checkpoint history** — append-only dated/wave entries in the current checkpoint, roadmap and map. Each entry records starting refs/SHAs, scope, evidence, files changed, resulting commit/PR, validation performed, work deliberately omitted, blockers and next bounded step.

A new chat should reconstruct the latest state from GitHub first, then incorporate any transcript supplied by the owner. If a transcript is unavailable, record that limitation and use GitHub evidence as the authoritative development history. Never claim that the complete ChatGPT transcript has been transferred unless an archived transcript exists and its path and integrity are verified.

## 3. Project invariants

- Baseline 2.0 is the canonical functional target; Baseline 1.0 is historical.
- Preserve historical IDs and check collisions before adding identifiers.
- Keep design, implementation, tests, verification, qualification, release, deployment and acceptance as distinct states.
- Contour A is the autonomous development environment; Contour B is the MediaHub OS product. Contour B product development starts only after Contour A deployment and independent acceptance.
- Prefer stable existing GitHub projects and components. Inspect upstream source, release/tag pin, license, security posture, maintenance, interface fit and evidence before designing a replacement.
- Make technical decisions autonomously within approved architecture and permissions. Escalate only genuine product, business-priority, risk-tolerance or authority conflicts.
- Mark facts, hypotheses, proposals, implementations and accepted outcomes distinctly. Claims of success require direct evidence.
- Preserve historical material. Retire or replace it only through source-backed classification and a traceable decision.
- Keep credentials out of prompts, issue bodies, source files, logs, PR diffs, artifacts and checkpoints.

## 4. Binding cloud execution and geography constraint

All cloud model operations and API-key routing run exclusively on GitHub-hosted GitHub Actions runners. This includes provider selection, credential injection, API calls, retry/backoff, quota tracking, cooldown state, failover and cloud task orchestration.

- Cloud execution uses GitHub-hosted ephemeral runners such as `ubuntu-latest`.
- Owner-operated servers and local machines are reserved for local inference and local compute only.
- Cloud orchestration has no dependency on an owner-operated server, self-hosted runner, Supabase function, external database, persistent proxy or always-on gateway.
- Cloud access and model routing are independent of the owner's physical geolocation and internet egress point. Provider access remains subject to provider account eligibility, terms, network reachability from GitHub-hosted runners, and provider-side policy.
- A server can join a local-compute lane only through a separate accepted contract. Cloud errors never trigger silent routing of cloud credentials or payloads to a local server.
- GitHub Actions concurrency is a coordination aid, not a durable FIFO queue. GitHub Issues can hold task envelopes; a versioned state branch can hold redacted quota metadata; artifacts provide per-run evidence. These mechanisms still require concurrency, recovery and acceptance evidence.
- Route quotas by actual provider/account/project/model/metric/reset scope. Key aliases alone do not imply independent quotas. Honor `Retry-After` and documented reset headers, redact credentials, and defer work when eligible free capacity is exhausted.
- Paid fallback, credit purchases, provider calls, workflow dispatch, secret modifications, tests, qualification, infrastructure changes, deployment, merge and branch integration require the authorization specified by the current governance documents.

## 5. Authority boundaries and actions

Absent separate explicit authorization, keep to source review, design, documentation and reviewable GitHub changes. The following require their own approval when applicable: installing software, running tests or qualification, invoking models/providers, using credentials, inspecting host/runtime, changing infrastructure, dispatching operational workflows, deploying, migrating, merging, rebasing or cherry-picking.

Creating a documentation branch or PR is not implementation acceptance. A green existing workflow is evidence only for the exact commit and checks it actually ran.

## 6. Required protocol for every `/next`

1. Query current `main`, documentation branch and relevant working branches; record HEAD SHAs, PR state and divergence. Never merge divergent branches without authorization.
2. Read the current project map, bootstrap instruction, latest checkpoint and Master Roadmap from live GitHub refs.
3. Identify the next unfinished roadmap item and prove its status from primary artifacts.
4. Read existing implementation and search stable upstream projects before creating new components.
5. Choose one bounded, reviewable work slice. Resolve technical details independently within approved constraints.
6. Perform only authorized actions. If an action is gated, continue independent source review and documentation.
7. Re-read every changed file from GitHub; compare expected content and SHA. Inspect the commit diff and PR status.
8. Append the result to checkpoint and roadmap, update the map navigation where relevant, and retain prior history.
9. Report outcome, evidence links, exact commit/PR/SHA, validations, unperformed actions, blockers and next step.
10. Always include the direct project map link: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 7. Handoff state at creation time — 2026-10-17

This section is a dated snapshot, not a claim of current status. Refresh every item at the start of the next chat.

- Repository: `VlDMlNSh/mediahub-os`.
- `main` observed at `4712c30c3e0296cf1d792c4c69e49cdb798d99fe` during Wave 44 inspection.
- Documentation branch observed at `a0c432273914fa5c4bd9e756736f9c9b72b41a77` during Wave 44 inspection.
- PR #320 is an open documentation audit PR as last inspected; refresh state before relying on it.
- The current branch contains a Wave 45 GitHub Actions-only cloud-router architecture decision and updates to the map/checkpoint/roadmap; confirm latest branch HEAD and file SHAs from GitHub before continuing.
- Wave 44 audit distinguishes workflow secret references from actual configured secret presence and credential validity. Actual secret values were never read. SiliconFlow alias mismatch remains a reconciliation item: `SILICON_KEY_2` versus `SILICONFLOW_API_KEY_2`.
- Free-cloud candidates: Cloudflare Workers AI, Groq, Gemini, then account-verified Z.ai, SiliconFlow, Novita, Mistral, OpenRouter and Hugging Face. Conditional/quarantined candidates require current authoritative quota, pricing, model and terms evidence. No paid fallback.
- GitHub Actions-only router design: GitHub-hosted runner, issue-backed task queue, serialized coordinator, redacted quota/cooldown state on a versioned branch, Actions artifacts as evidence. Current design is architecture only until activation gates are satisfied.
- Existing `.github/workflows/astra-provider-qualification.yml` uses a self-hosted runner and is excluded from the cloud route. Gemini Agent 2/3 workflows use GitHub-hosted runners.
- Required activation gates include A0 ingress/lifecycle and task authorization, MH-12 tool enforcement, R-06 privacy/data-egress disposition, accepted target manifest, secret-name reconciliation, and independent concurrency/recovery/redaction review.
- Last recorded source-only pass performed no provider calls, workflow dispatch, tests, qualification, secret reads, infrastructure change, deployment or merge. Verify all later activity against live GitHub evidence.

## 8. Conversation-history archive template

When a sanitized conversation export is supplied, add a dated archive entry with:
- source conversation title/date and user-provided export provenance;
- original transcript file path and SHA-256;
- redaction review outcome;
- related issue/PR/commit/checkpoint links;
- decision and work-item index.

Do not fabricate transcript content or claim access to conversations absent from the active context. GitHub is the durable project-development ledger; the original ChatGPT transcript remains a separate source unless explicitly archived.

## 9. Required opening message for the new chat

Paste the following as the first message in a new chat:

> Continue MediaHub OS from current GitHub state. First read `docs/architecture/MEDIAHUB-MASTER-CONTINUATION-PROMPT-2026-10-17.md`, then the live project map, bootstrap instruction, current continuation checkpoint, Master Development Roadmap and Baseline 2.0. Query current refs/HEADs, PRs, issues and workflow evidence; reconcile branch divergence before action. Preserve all historical decisions, implementation evidence and checkpoint entries. Treat any prior-chat summary as navigation only and incorporate an original transcript only when supplied or verifiably archived. All cloud-model execution and API-key routing must run exclusively on GitHub-hosted Actions, independent of owner geolocation or internet egress point; servers are reserved for local computation. Follow all authority gates. Identify the next unfinished roadmap item, complete one bounded source-backed pass, read back changed files and report evidence, commit/PR/SHA, blockers and next step. Always link the current project map.
