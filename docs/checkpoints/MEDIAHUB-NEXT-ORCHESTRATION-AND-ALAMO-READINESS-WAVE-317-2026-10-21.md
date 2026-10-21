# Wave 317 — per-/next role orchestration and Alamo readiness (2026-10-21)

## Executive result

Wave 317 updates the Draft Gemini controller to select roadmap-driven assignments on every eligible /next bridge event and retain three distinct roles under one shared immutable target SHA. It also formalizes the ChatGPT-turn-to-Issue-#301 bridge and the separate Alamo-only Claude executor contract in the canonical Bootstrap.

This does **not** mean the system is live. The controller exists only in Draft PR #432; main still has the legacy reusable-workflow controller and does not contain the GitHub API dispatch or issue_comment bridge. The PR is unmerged and has no formal review. Agent-mode remains NOT RUN.

## Canonical references

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Current checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/432

## Refs and implementation

- main HEAD at verification: 1f9fe47f986376a733fb0ddfa5e3b567b2613d5c.
- Canonical docs branch HEAD before this report: 5a30ec133f6de8297f50b99911e6454af36fb14b.
- PR #432 head/base: 269b57b8b9c412261c97c4811bd49cbb4122ba03 / f16e5bae202a78584f273132e7f88c6e25d3142e; OPEN, DRAFT, UNMERGED.
- Controller blob on PR branch: 9453403bba899a2400ee3fb874d32badd034c704.
- Controller transport contract test blob: 081ba101a1b56553577abd7b469b3c9bf6f31196.
- Wave 292 controller contract blob: 84a92e514c930c55d411bf74ad390109b7ed0d4b.
- Bootstrap blob after the new bridge/executor contract: 6a8035d724a3597f78106aefcf151b7026876b42.

Controller behavior currently in the Draft:
- GitHub API dispatch of three separate workflow_dispatch children only from trusted main, using the controller-only MEDIAHUB_GITHUB_TOKEN; the same immutable target SHA is supplied to all three.
- HMAC-signed bounded inputs verified in child jobs before provider/model execution.
- Per-agent dispatch attempts recorded before POST; explicit non-408 4xx rejection is terminal failure; transport/5xx/408 uncertainty is reconciled by the unique correlation ID; complete batch summary and fail-closed nonzero result on missing/failed child.
- A candidate owner-only /next bridge on non-PR Issue #301, exact comment body, replay marker next-comment-<comment-id>, and an explicit MEDIAHUB_GEMINI_BATCH_ENABLED repository-variable gate. Unset/false must skip all child dispatch.
- Updated per-/next assignments:
  1. Agent 1: read canonical map/Bootstrap/checkpoint/Roadmap/Issue #301, select the highest-priority open and unblocked task, complete one bounded implementation/evidence pass.
  2. Agent 2: independently map current acceptance criteria to source/tests and report exact reproducible evidence; explicitly does not claim to review Agent 1's concurrently created changes.
  3. Agent 3: audit transport, secret separation, HMAC, issuer/capability, least privilege, provenance and fail-closed behavior without reading secret values.
- No secrets: inherit; no Alamo/SentinelX use for Gemini; no merge/deployment/qualification authority given to agents.

## Exact-head CI

All five checks completed SUCCESS on 269b57b8b9c412261c97c4811bd49cbb4122ba03:
- [Workflow contract validation #39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718) — SUCCESS.
- [Astra Verify #39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683) — SUCCESS.
- [Astra Cloud Runtime Validation #39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609) — SUCCESS.
- [Controller non-launching PR-context probe #39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682) — SUCCESS; agent dispatch is not run in PR context.
- [Reusable workflow caller-context probe #39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781) — SUCCESS.

Formal PR #432 reviews: zero. Successful PR-context CI does not prove the trusted-main controller dispatch route, the secret configuration, or external governance.

## ChatGPT /next bridge status

A ChatGPT message is not a GitHub Actions event. The planned bridge therefore requires two distinct steps once accepted:
1. The assistant performs the normal engineering work in the chat.
2. For each eligible ChatGPT /next, it creates exactly one owner-authored Issue #301 comment whose entire body is /next through the authenticated GitHub integration; the workflow then produces its own controller run and child evidence.

This remains **CANDIDATE ONLY / NOT LIVE** until PR #432 is independently reviewed and merged, the trusted-main no-secret probe confirms actual caller context, and secret/permission/governance checks are verified. The current main controller still has no issue_comment bridge and no MEDIAHUB_GITHUB_TOKEN GitHub API dispatch path; the children on main still use the old reusable workflow_call contract. Do not post an automatic trigger or claim a live bridge before integration.

The repository variable MEDIAHUB_GEMINI_BATCH_ENABLED cannot be verified/set via the available GitHub inspection methods in this pass. It must remain unset/false during probes. Do not enable it until all gates are accepted.

## Alamo local Claude status

Fresh SentinelX and Desktop Commander inventory still finds only Voktors-Mini.Dlink online. mh-dev-01 and mh-dev-02 are offline/disabled. SentinelX keyword search for Alamo returned zero contexts; no host is positively identified as Alamo/server 3. Therefore:
- Claude Code on Alamo: **NOT RUN**.
- @SentinelX / agent-browser on Alamo: **NOT RUN**.
- No substitute host was used.
- The candidate route file on main, ops/agent-fabric/providers/local-executor-routing-v2.yaml, remains ASTRA_GOLD_QUALIFICATION_GATED; CLAUDE_FCC is a candidate route, not accepted proof of allowed non-paid auth. The current local-Claude qualification workflow targets mh-dev-02 and a local Ollama/FCC check, not Alamo, so it is not a substitute.

Alamo must be positively bound to an accessible host/session; the approved free/non-paid Claude Code route must prove its actual upstream, auth/cost class, terms, version, egress and no paid Anthropic API fallback before use. No provider credentials were read or emitted.

## Open acceptance gates

1. Independent security review of exact PR head 269b57b8b9c412261c97c4811bd49cbb4122ba03 — NOT VERIFIED.
2. Effective minimum permission scope of MEDIAHUB_GITHUB_TOKEN — NOT VERIFIED.
3. Presence/separation of MEDIAHUB_DISPATCH_HMAC_KEY and provider keys — NOT VERIFIED through a non-disclosing settings check.
4. Repository/org branch protection and Actions governance — NOT VERIFIED; the relevant protection API request is forbidden to this integration.
5. Trusted-main no-secret probe and confirmation of ChatGPT connector-authored issue_comment context — NOT VERIFIED.
6. Repository variable MEDIAHUB_GEMINI_BATCH_ENABLED — not inspected/set; fail-closed until deliberately enabled after gates.
7. Alamo host identity and permitted free Claude Code route — NOT VERIFIED.
8. Gemini Agents 1–3: **NOT RUN**; there is no controller agent-mode run ID or child run/job IDs for Wave 317.
9. Local Claude/browser: **NOT RUN**; no Alamo session/job ID or browser evidence exists.

## Next acceptance sequence

- Obtain a separate independent review of PR #432 at the exact head above; do not self-certify a review.
- Verify effective GitHub Actions token scope, HMAC/provider secret presence and separation without revealing values, and repository/org governance.
- After reviewed integration only, run the controller's no-secret trusted-main probe while the batch variable remains unset/false; verify a ChatGPT-authored owner comment has the expected association and creates one replay-safe controller run without child dispatch.
- Positively register/identify Alamo and qualify the permitted non-paid Claude Code route with no paid fallback.
- Only then enable the batch gate and run a controlled first batch; capture controller ID, three child workflow/run/job IDs, shared SHA, artifact digests and independent verification. Keep Contour B blocked until Contour A is deployed and independently accepted.

No Gemini agent-mode dispatch, local Claude run, secret read, PR merge or deployment occurred in Wave 317. Status: implementation and exact-head CI **VERIFIED**; end-to-end /next orchestration **NOT QUALIFIED / NOT ACCEPTED**.
