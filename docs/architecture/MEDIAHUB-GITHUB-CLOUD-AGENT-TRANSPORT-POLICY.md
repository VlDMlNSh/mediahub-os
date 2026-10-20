# MediaHub OS — mandatory GitHub cloud-agent transport policy

Date: 2026-10-20
Status: OWNER-DIRECTED WORKING RULE / REQUIRED FOR ALL FUTURE CLOUD-AGENT DISPATCHES

## Binding rule

All cloud-agent launches for MediaHub OS MUST use the repository's GitHub-hosted Actions controller workflow `.github/workflows/gemini-batch-dispatch-controller.yml` and its child workflows. The controller's GitHub REST API dispatch and run-monitoring calls MUST authenticate with the repository secret `MEDIAHUB_GITHUB_TOKEN`.

This is the sole approved launch transport for cloud agents in this project. Do not launch Gemini or other cloud agents directly from SentinelX, a server shell, a local CLI, an ad-hoc script, an unrelated workflow, or another transport. SentinelX may be used for local computation and for non-agent repository inspection, but not as the agent execution host or an alternate agent launcher. Cloud-agent execution must occur on GitHub-hosted Actions runners through the approved controller/child-workflow path.

## Credential handling

- `MEDIAHUB_GITHUB_TOKEN` is an API credential used by the controller only for the documented GitHub API operations required to dispatch and monitor the fixed-scope child workflows.
- Never print, echo, decode, upload, place in prompts, pass to Gemini/model tools, or expose the token to child agent processes. Do not copy the token into artifacts, PRs, logs, task payloads, or reports.
- Keep provider credentials (for example, the separately configured Gemini API keys) distinct from the GitHub transport credential.
- Use least privilege and repository/environment secret controls. Do not broaden token permissions or create alternate credentials merely to bypass a denied request.
- Do not treat technical access as authority to bypass issuer/capability, budget, provider policy, branch protection, review, or acceptance gates.

## Dispatch and evidence protocol

1. Dispatch the controller through the approved GitHub Actions workflow entry point with its explicit confirmation input.
2. The controller uses `secrets.MEDIAHUB_GITHUB_TOKEN` for child `workflow_dispatch` calls and run metadata/monitoring. Keep the controller's fixed task scopes and ambiguity/fail-closed behavior.
3. Record the controller run ID, each child run ID/job ID, exact workflow/ref, terminal conclusion, produced artifact/PR, and relevant commit/blob SHA. Never infer success from dispatch acceptance alone.
4. Review agent output as untrusted proposals. Independently inspect source refs, diff, tests, provenance, authority boundaries and exact-head CI before any integration. No automatic merge or qualification follows from a successful agent run.
5. If a child or controller fails, record the observed failure, inspect available logs, correct the demonstrated cause, and retry only after diagnosis. Do not silently switch transports.
6. If this transport is unavailable, continue independent work that does not require launching agents and record the blocker. Do not use a server/local CLI fallback.
7. After any change to this rule or controller, read back the changed GitHub files and verify their blob SHA.

## Enforcement and scope

This rule applies to all future MediaHub OS cloud-agent work and every `/next` wave until changed through explicit owner direction and the project's applicable governance/change-control process. It governs transport only; it does not grant additional product, repository, provider, or deployment authority and does not change Baseline 2.0.

## Current operational status — governance gate (2026-10-20, Wave 243)

The GitHub-hosted Actions controller is the **only policy-authorized cloud-agent/API entry point**. Option A was not proven because effective Actions restrictions and the `MEDIAHUB_GITHUB_TOKEN` principal permissions could not be verified through the available GitHub connection. The owner explicitly approved Option B for implementation in a separate PR at [Issue #301 comment 6289586838](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289586838). This approval authorizes design/implementation only; it does **not** authorize agent dispatch, merge, deployment, or Contour A qualification.

Implementation proposal: [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) converts the three child workflows to `workflow_call`, removes direct `workflow_dispatch`, replaces REST child dispatch with controller-called reusable jobs, and explicitly passes only the corresponding provider key. PR #421 is Draft and remains unaccepted pending exact-head CI, independent review, workflow caller-guard verification, positive/negative contract tests, and secret-boundary checks.

**Cloud-agent dispatch remains ON HOLD** until the implementation is independently reviewed, required checks pass, the PR is integrated through the project’s governance gates, and separate authorization for a real agent run is recorded. Do not use the old REST dispatch path or any alternate transport. No cloud agent has been launched as part of Wave 243.

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
