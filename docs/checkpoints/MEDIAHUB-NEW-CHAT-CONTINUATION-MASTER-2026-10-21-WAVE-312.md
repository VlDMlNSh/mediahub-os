# MediaHub OS — New-Chat Continuation Master
**Date:** 2026-10-21  
**Purpose:** Restore operational context from the MediaHub OS project chat and continue the next bounded engineering pass without losing architecture constraints or evidence.

## Canonical sources of truth

- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) — https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md) — https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md) — https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- [Master Development Roadmap 1.0](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md) — https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- [Governance Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Current repair PR #432](https://github.com/VlDMlNSh/mediahub-os/pull/432)
- [Earlier transport repair PR #431](https://github.com/VlDMlNSh/mediahub-os/pull/431)

## Mandatory architecture boundary — do not reinterpret

1. **Gemini Agents 1–3 are dispatched only through the approved GitHub Actions controller using GitHub API transport and repository secret `MEDIAHUB_GITHUB_TOKEN`.**
2. `MEDIAHUB_GITHUB_TOKEN` is a GitHub transport credential, not a Gemini provider key. Keep it confined to the controller dispatch/monitoring step. Never pass it into a child workflow, model/prompt, shell arguments, artifact, log, job summary, or generated report. Never use `secrets: inherit`.
3. Provider credentials (`GEMINI_API_KEY*`) are separate and scoped only to their corresponding child model step.
4. **Alamo/server 3 is only for local Claude Code and browser-agent work. It is never the Gemini transport and never a fallback for Gemini.** Verify host identity, capabilities, allowlist, and approved free/non-paid route before attempting local Claude/browser work.
5. Do not treat technical capability as authorization. Preserve issuer/capability boundaries and the separation of Jarvis, ASTRA A0, and MediaHub Product State Authority.
6. Preserve Baseline 2.0 and historical IDs. Contour B cannot start before Contour A is deployed and independently accepted.
7. Do not launch Gemini agent mode until controller/child implementation, effective governance, token permissions, independent security review, exact-head CI, and trusted no-secret probe evidence all pass.

## State at handoff

### Repository / documentation
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Canonical map blob last checked: `8c526be39a7d58e009862b9eca2f350d3d948d8f`. Contents API returned zero text bytes for the map in this read; this is not evidence that the file is empty. Use raw/blob-by-SHA if the contents endpoint is blank.
- Bootstrap blob last checked: `c6ae5c09b95e708f547b8eaae1aab3913bf10288`.
- Current checkpoint blob last checked: `8db6a2fd0633e108c2bfe1147e33dc179bfd98d7`.
- Master roadmap blob last checked: `ba1a503f5ad6309bafee3cd7ec4e7de112af79fd`.
- Governance Issue #301 remains OPEN.
- Do not update the canonical map merely to claim progress; change it only if navigation/architecture truth materially changes.

### Gemini controller repairs — distinguish the two PRs

**PR #431** — https://github.com/VlDMlNSh/mediahub-os/pull/431  
- Existing earlier transport repair documented in the current checkpoint.
- Checkpoint reports branch `fix/gemini-github-api-transport-wave-312`, head `8177cce6859624e7740db204e0c19cb2bcdfe7ca`, open, non-draft, mergeable at the time of that report.
- Its recorded exact-head checks succeeded: workflow contract validation run `39600483390`, negative caller-context probe `39600483597`, Astra Cloud Runtime Validation `39600483360`, controller no-secret probe `39600483335`, Astra Verify `39600483400`.
- Formal independent security review was still missing. These facts must be rechecked live before relying on them.

**PR #432** — https://github.com/VlDMlNSh/mediahub-os/pull/432  
- This chat's follow-up repair attempt, branch `fix/gemini-controller-api-dispatch-wave312-final`.
- Last checked PR head: `ea637eb55c87d44f0ce22730588e744c7470ee1d`; base SHA returned by PR API: `f16e5bae202a78584f273132e7f88c6e25d3142e`; PR OPEN, DRAFT, mergeable at the last read.
- Latest checked file blob SHAs on that branch:
  - Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: `3268dbf08cbcf4869b6ec608c9d61c34ac213154`
  - Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: `a4160266e4da8dce00862936c6d4a3a7c17026f5`
  - Agent 2 `.github/workflows/gemini-agent-2.yml`: `71adf89707c45fbfabdcfdb35fe0381d4583d647`
  - Agent 3 `.github/workflows/gemini-agent-3.yml`: `507aa2cadefb3e8bdd8d210713c011152b202529`
  - `tests/test_gemini_controller_context_probe_wave284_contract.py`: `980d3868a2f9adbac842da7802289f4755f5e083`
  - `tests/test_gemini_controller_positive_context_probe_wave292_contract.py`: `5ab7799653ec51696939a2115d6e5c02ed18c8f6`
- PR #432 adds an HMAC-signed dispatch envelope, a controller-only `MEDIAHUB_GITHUB_TOKEN`, common target SHA, explicit opt-in, and child-side signature checks. It also adds a dependency on repository secret `MEDIAHUB_DISPATCH_HMAC_KEY`; its existence/configuration and least-privilege setup have **not** been verified. Do not read or print secret values.
- The existing Wave 284 contract test originally expected reusable `workflow_call` children. It was edited on the #432 branch to require signed `workflow_dispatch` children, but the latest result of that test has **not** been verified. A prior run of contract validation exposed an incompatible old assertion; exact-head test status must be checked again.
- The #432 approach has not been independently security-reviewed or accepted. In particular, inspect HMAC canonicalization parity between controller and children, the dispatch-to-run correlation method, child workflow input compatibility, event/ref trust conditions, target SHA checkout, token permissions, and whether any child job can access provider credentials before authorization.
- **Do not merge #432, do not dispatch agent mode, and do not assume #431 and #432 can be combined without conflict.** Compare both implementations and select one coherent path after rechecking live refs and CI. Do not duplicate or overwrite evidence.

## Executor status

- Gemini Agent 1–3: **NOT RUN** in this chat. No dispatch run IDs or child run IDs were generated here.
- Claude Code on Alamo: **NOT RUN**; identity and approved free/non-paid route have not been positively verified in this handoff.
- Browser agent on server 3: **NOT RUN**; do not assume the known operational SentinelX host is Alamo.
- Prior SentinelX observation in project context: operational host `host_5f7264034bdf0b51`, hostname `Voktors-Mini.Dlink`; it was not proven to be designated Alamo. Two other hosts (`mh-dev-01`, `mh-dev-02`) were disabled at that observation. Recheck before using.
- No token values were read or exposed by this work.

## Required next pass (do these in order)

1. Re-fetch live `main`, documentation branch, PRs #431/#432, their current head/base SHAs, latest commit/blob SHAs, checks, formal review submissions, issue #301, and repository/org branch protection and Actions permissions. Do not rely on the snapshots above without revalidation.
2. Read Bootstrap §1D, current checkpoint, master roadmap, the canonical map, the normative transport/security contracts, and all controller/child workflow files on both PR branches. Search for stale contradictory text such as “no transport token required,” “no REST dispatch,” or “do not use REST dispatch”; reconcile active guidance without rewriting history inaccurately.
3. Compare #431 vs #432. Choose a single minimal implementation. Ensure all three child workflows expose the exact workflow_dispatch inputs expected by the controller, share one immutable 40-character target SHA, verify authorization before model/provider steps, and fail closed. Verify GitHub API endpoint/permissions and actual run correlation; do not assume `display_title` always provides a safe unique correlation key.
4. Run the relevant workflow contract tests and YAML/lint checks locally if an authorized runner is available; otherwise use PR CI. Re-read every changed file after edits and record exact blob SHA.
5. Obtain a genuinely independent security review (not a self-review or a comment from the PR author). Verify effective governance and least-privilege token permissions. Keep PR draft/unmerged until those gates pass.
6. Run only the default non-launching no-secret probe first, from trusted main after permitted integration. Verify its exact run ID and jobs. Only after all gates pass may the approved controller be explicitly invoked with `mode=agents` and `confirm=yes`; record controller run ID, all three child run IDs/statuses, immutable target SHA, artifacts/digests, and independent verification.
7. If gates cannot be satisfied, record the exact blocker and keep Gemini agents **NOT RUN**. Continue safe, independent documentation/code review instead.
8. Update the dated report and current checkpoint on the canonical docs branch. Update the canonical map or roadmap only if justified by actual state changes. Re-read edited docs and record blob SHAs.
9. Always provide the direct canonical map link in the response: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Acceptance language

Use these statuses accurately: **PLANNED**, **DISPATCHED**, **RUNNING**, **SUCCEEDED**, **VERIFIED**, **QUALIFIED**, **ACCEPTED**. A successful CI run is not security acceptance. A draft PR is not integrated. A merged PR is not deployment. Do not state the controller is fixed/accepted until exact-head tests, independent review, governance and trusted probe evidence support that conclusion.

## Owner-action rule

Do not ask the owner for work unless a real owner-only permission or approval is proven necessary. If owner action becomes necessary, put a separate final section in the response with a bold uppercase action statement, exact links, step-by-step instructions, exact text to paste when applicable, and the expected result. If no owner action is required, omit that section.

## First message to paste in the new chat

`/next. Прочитай MEDIAHUB-NEW-CHAT-CONTINUATION-MASTER-2026-10-21-WAVE-312.md и все канонические источники. Сначала перепроверь live refs/HEAD/SHA, PR #431/#432, CI, formal reviews, Issue #301, governance и executor availability. Не запускай Gemini до прохождения всех gates. Сравни обе реализации контроллера, выбери одну безопасную, доведи до проверяемого PR, зафиксируй результаты и обнови checkpoint.`
