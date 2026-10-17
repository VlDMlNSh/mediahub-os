# MediaHub OS — Session Skills and Free Gemini Dispatch Path, Wave 64

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **SKILL INVENTORY COMPLETE / USER-REPORTED RUN SUCCESS / CURRENT-SESSION DISPATCH CAPABILITY GAP**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Queue acceptance: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Prior launch guide: https://github.com/VlDMlNSh/mediahub-os/blob/docs/gemini-manual-launch-wave63-20261017/docs/operations/MEDIAHUB-GEMINI-THREE-AGENT-MANUAL-LAUNCH-GUIDE-WAVE-63-2026-10-17.md

## 1. Goal

Select the smallest useful skill set for repeated, evidence-backed Gemini workflow launches from an agent session, while keeping execution on GitHub-hosted Actions and avoiding owner-operated servers.

The owner reports a successful launch. The exact run URL/ID was not included in this request, so this document treats that success as owner-reported rather than independently verified runtime evidence.

## 2. Skill selection

### Required for the current workflow

| Skill | Source | Use |
|---|---|---|
| Find Skills | `skills://plugins/skills/find-skills/skill.md` | Discover additional capabilities as needs change. Already available in this session. |
| Code Verification | `skills://plugins/codex-engineering-guardrails/code-verification/skill.md` | Independently inspect run evidence, artifacts, PR diffs and acceptance criteria. Already available in this session. |
| Session Handoff | `skills://plugins/codex-dev-workflows/session-handoff/skill.md` | Preserve exact task IDs, run URLs, artifact refs, PRs, blockers and next action across sessions. Already available in this session. |
| Orchestrate Work | `skills://plugins/codex-dev-workflows/orchestrate-work/skill.md` | Sequence Agent 1 → Agent 2 → Agent 3 and keep each agent's scope separate. Already available in this session. |
| Verification Before Completion | `skills://plugins/superpowers/verification-before-completion/skill.md` | Require fresh evidence before marking a run or task successful. Already available in this session. |

### Optional, only if a browser runtime is actually connected

| Skill | Source | Use and limitation |
|---|---|---|
| agent-browser | `skills://plugins/agent-browser/agent-browser/skill.md`; upstream: https://github.com/vercel-labs/agent-browser | Automate the GitHub Actions UI when a supported browser session and the CLI are available. The skill file is available in this session's catalog, but its documented execution path requires the `agent-browser` CLI and browser runtime. No CLI installation or host inspection was performed. |

No separate GitHub skill is needed for repository reads, source updates and PR work: the GitHub connector already exposes those operations directly. The current connector tool set inspected for this pass does not expose a workflow-dispatch action.

## 3. Recommended minimal set

For work in this ChatGPT session, use these already-available skills:
1. `find-skills` for capability discovery.
2. `code-verification` for review of each run and its PR.
3. `orchestrate-work` for ordering the three agents and keeping scopes distinct.
4. `session-handoff` for durable evidence and continuation.
5. `verification-before-completion` as the completion gate.

Treat `agent-browser` as an optional route, not as an installed or operational browser. Its presence in the skill catalog alone does not create a signed-in browser session or provide a workflow-dispatch API.

## 4. Can the current session launch workflows for free?

Current evidence supports this answer:

- **GitHub Actions UI:** manual launch is available to an authorized repository user. GitHub-hosted runners and Gemini API usage remain subject to the applicable free quotas, account/project policy, runner minutes and model availability.
- **GitHub connector in this session:** repository source reads, file operations and PR operations are exposed; a workflow-dispatch operation was absent from the tool inventory inspected in this pass.
- **agent-browser:** may automate UI interactions in a compatible browser runtime, but the documented CLI route requires `agent-browser` to be installed and a browser to be connected. No such installation or runtime inspection was authorized/performed.
- **TinyFish browser automation:** its tool description states that automation is metered against a wallet. It is therefore excluded from the requested free-only route.
- **Skills themselves:** reading skill instructions from the available catalog does not require an additional model-provider call. Installing a CLI, connecting a browser profile or changing repository settings is a separate action with separate requirements.

Therefore, the lowest-friction free path currently evidenced is the GitHub Actions UI, using existing workflow files and existing GitHub/Gemini quota. Launching the workflow directly from this session requires either a supported workflow-dispatch connector action or an explicitly authorized, already-available browser session. A skill alone cannot grant missing API permissions.

## 5. No bypass or hidden cost

- Do not route around exhausted Gemini quotas by rotating keys contrary to provider limits.
- Do not use paid fallback, metered browser automation, proxies or region spoofing for this free-only path.
- Keep all Gemini key values in GitHub Actions Secrets.
- Preserve the distinction between a successful single workflow run and a qualified durable multi-agent queue.
- Do not install CLI software, inspect a host/runtime, change infrastructure, dispatch a provider workflow, run tests or qualify without the corresponding explicit authorization.
- Keep the queue acceptance issue #301 as the source of truth for queue lifecycle work.

## 6. Evidence needed to close the session-launch gap

Preferred route:
1. Provide or expose a GitHub connector operation that dispatches a named workflow with validated `workflow_dispatch` inputs, if the integration supports it.
2. Restrict it to the three known workflow paths and the `main` ref.
3. Require a bounded task ID and explicit Contour A scope.
4. Return the created run URL/ID.
5. Read back run conclusion, jobs, artifact list and resulting PR.
6. Record evidence in issue #301 and the continuation checkpoint.

Alternative route:
- Use an already-authorized browser session with an appropriate browser skill, only after the user explicitly authorizes UI interaction and the session's availability is confirmed. Avoid CLI installation or host inspection until separately authorized.

## 7. Evidence boundary

This pass read the canonical map, bootstrap instruction, continuation checkpoint, Master Roadmap, issue #301, PR #324 and the relevant skill instructions. It created this documentation on a dedicated documentation branch and performed read-back verification.

No workflow dispatch, Gemini provider call, secret read/change, settings change, software installation, host/runtime inspection, test, qualification, deployment, merge or branch integration occurred.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
