# MediaHub OS — mandatory GitHub cloud-agent transport policy

Date: 2026-10-20
Status: OWNER-DIRECTED WORKING RULE / REQUIRED FOR ALL FUTURE CLOUD-AGENT DISPATCHES

## Binding rule

The GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` is the only authorized entry point for cloud-agent launches. PR #421 merged a `workflow_call` design that conflicted with the owner's required transport contract. Corrective [PR #431](https://github.com/VlDMlNSh/mediahub-os/pull/431) restores controller-side GitHub API dispatch/monitoring using `MEDIAHUB_GITHUB_TOKEN`; server 3/Alamo is exclusively for local Claude Code and browser-agent work, never Gemini transport. Exact-head CI for the implementation passed (see the Wave 312 report); genuine independent security review and effective repository/org governance confirmation remain required before merge or agent-mode dispatch. The controller's explicit `confirm: yes`, capability/issuer, provider/quota, branch protection, and acceptance gates remain mandatory.

This is the sole approved launch transport for cloud agents in this project. Do not launch Gemini or other cloud agents directly from SentinelX, a server shell, a local CLI, an ad-hoc script, an unrelated workflow, or another transport. SentinelX may be used for local computation and for non-agent repository inspection, but not as the agent execution host or an alternate agent launcher. Cloud-agent execution must occur on GitHub-hosted Actions runners through the approved controller/child-workflow path.

## Credential handling

- `MEDIAHUB_GITHUB_TOKEN` is the GitHub API transport credential used only in the controller's dispatch/monitoring steps. It must never be exposed to child/model processes, prompts, logs, summaries, or artifacts. Child workflows receive only their own provider key through their own workflow secret context.
- Never print, echo, decode, upload, place in prompts, pass to Gemini/model tools, or expose the token to child agent processes. Do not copy the token into artifacts, PRs, logs, task payloads, or reports.
- Keep provider credentials (for example, the separately configured Gemini API keys) distinct from the GitHub transport credential.
- Use least privilege and repository/environment secret controls. Do not broaden token permissions or create alternate credentials merely to bypass a denied request.
- Do not treat technical access as authority to bypass issuer/capability, budget, provider policy, branch protection, review, or acceptance gates.

## Dispatch and evidence protocol

1. Dispatch the controller through the approved GitHub Actions workflow entry point with its explicit confirmation input.
2. In the corrected design, the controller snapshots one immutable `main` SHA, dispatches only the three fixed child workflow IDs through GitHub REST with `MEDIAHUB_GITHUB_TOKEN`, and monitors each run using pre-dispatch run-ID baselines. Pass the target SHA as `base_ref` so each child checks out the same source commit. The token remains controller-only; each child receives only its own provider key. Never use `secrets: inherit`.
3. Record the controller run ID, each child run ID/job ID, exact workflow/ref, terminal conclusion, produced artifact/PR, and relevant commit/blob SHA. Never infer success from dispatch acceptance alone.
4. Review agent output as untrusted proposals. Independently inspect source refs, diff, tests, provenance, authority boundaries and exact-head CI before any integration. No automatic merge or qualification follows from a successful agent run.
5. If a child or controller fails, record the observed failure, inspect available logs, correct the demonstrated cause, and retry only after diagnosis. Do not silently switch transports.
6. If this transport is unavailable, continue independent work that does not require launching agents and record the blocker. Do not use a server/local CLI fallback.
7. After any change to this rule or controller, read back the changed GitHub files and verify their blob SHA.

## Enforcement and scope

This rule applies to all future MediaHub OS cloud-agent work and every `/next` wave until changed through explicit owner direction and the project's applicable governance/change-control process. It governs transport only; it does not grant additional product, repository, provider, or deployment authority and does not change Baseline 2.0.

## Current operational status — governance gate (2026-10-20, Wave 243)

The GitHub-hosted Actions controller is the **only policy-authorized cloud-agent/API entry point**. Option A was not proven because effective Actions restrictions and the `MEDIAHUB_GITHUB_TOKEN` principal permissions could not be verified through the available GitHub connection. The owner explicitly approved Option B for implementation in a separate PR at [Issue #301 comment 6289586838](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289586838), then clarified that routine controller-only agent runs are authorized after the implementation gates pass and the PR is integrated; no separate per-run owner prompt is required after that. This does **not** authorize dispatch before those gates, automatic merge, deployment, or Contour A qualification.

PR #421 is merged but its reusable-workflow architecture is a transport-contract mismatch. Corrective [PR #431](https://github.com/VlDMlNSh/mediahub-os/pull/431) restores token-backed GitHub API dispatch/monitoring, explicit no-secret probe mode, per-child provider-key isolation, and immutable source SHA pinning. At the latest read, PR #431 is draft/open and independent review is not yet recorded. Exact-head CI must be verified before merge; no Gemini dispatch is authorized by this documentation update.

**Cloud-agent dispatch remains ON HOLD until the implementation is independently reviewed, required checks pass, and the PR is integrated through the project’s governance gates.** After that, routine bounded runs may use the single controller with explicit `confirm: yes` without another per-run owner prompt. Do not use the old REST dispatch path or any alternate transport. No cloud agent has been launched as part of Wave 243.

## Initial runtime evidence (2026-10-20)

- Controller run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396582084 — dispatch step succeeded using `MEDIAHUB_GITHUB_TOKEN`; monitoring step concluded failure because at least one child did not pass the controller's completion validation.
- Agent 1 run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396593650 — job succeeded; PR #413 was created.
- Agent 2 run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067 — job failed at “Validate Gemini produced an actionable PR result”; this does not prove the Gemini CLI step itself failed.
- Agent 3 run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396598015 — job succeeded; Draft PR #414 was created.
- Thus the transport has demonstrated successful API dispatch and two successful child jobs, but the three-agent batch was not fully successful. No token value was accessed or exposed in this record.

## Navigation

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Governing issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Wave report: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-GITHUB-TRANSPORT-CONTROLLER-WAVE-217-2026-10-20.md


## Owner clarification — autonomous continuation and dispatch posture (Wave 244, 2026-10-20)

The owner clarified that MediaHub OS must continue autonomously and efficiently, including using the available cloud agents as engineering capacity. The prior “dispatch ON HOLD” language is a temporary gate on the unaccepted controller transition, not a project-wide or indefinite prohibition and not a reason to stop independent work. The owner has now authorized routine controller-only cloud-agent runs after the PR #421 controller gates below are satisfied; no separate owner prompt is required for every run.

**Current gate:** PR #421 remains Draft/unmerged and has no independent review recorded at the latest read. Before the first run on the new architecture, obtain genuine independent review, verify the caller-ref guard and secret/permission boundaries, pass a controlled negative caller-context test without launching Gemini, and rerun required checks at the exact latest head. Integrate only through repository/project governance and protection. Then run bounded agent tasks through the single controller with its explicit `confirm: yes` input and record controller/job evidence. This clarification supersedes the earlier requirement for a separate per-run owner authorization after integration, but does not waive the controller gate, review, tests, issuer/capability, budget/provider restrictions, or acceptance requirements.

The only approved route remains GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` → fixed-scope child workflows. Do not launch agents from SentinelX, server/local shell, local CLI, ad-hoc scripts, unrelated workflows, or alternate transports. Never expose `MEDIAHUB_GITHUB_TOKEN` to child/model processes. Do not use `secrets: inherit`; pass only the specific child provider secret. No agent was launched in Wave 244.

Wave report: [MEDIAHUB-CLOUD-AGENT-AUTONOMY-CLARIFICATION-WAVE-244-2026-10-20.md](../checkpoints/MEDIAHUB-CLOUD-AGENT-AUTONOMY-CLARIFICATION-WAVE-244-2026-10-20.md).
