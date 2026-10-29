# MediaHub OS — Master Prompt for New-Chat Continuation

Updated: 2026-10-29  
Repository: https://github.com/VlDMlNSh/mediahub-os

## Copy/paste command for a new chat

```text
/next — продолжай MediaHub OS строго по актуальному состоянию GitHub. Сначала прочитай и проверь Bootstrap, каноническую карту, текущий checkpoint, Master Roadmap, Issue #301 и связанные PR/CI. Используй этот файл как контекстный указатель, но считай GitHub и актуальные SHA единственным источником истины. Делай один небольшой, проверяемый микро-шаг за проход; избегай больших параллельных запросов и длинных серий действий, которые могут прерваться. После шага перечитай изменённые файлы, проверь SHA, зафиксируй датированный отчёт и обнови checkpoint/карту при необходимости. Укажи доказательства, статусы, блокеры и ровно следующий микро-шаг. Не утверждай успех без проверок. Не запускай заблокированный controller и не обходи governance.
```

## Sources of truth — read at the start of every /next

1. Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
2. Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
3. Current checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
4. Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
5. Main orchestration issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
6. Gemini controller PR: https://github.com/VlDMlNSh/mediahub-os/pull/437
7. Related evidence PR: https://github.com/VlDMlNSh/mediahub-os/pull/441
8. Controller hardening PR: https://github.com/VlDMlNSh/mediahub-os/pull/583
9. Mature upstream research PR: https://github.com/VlDMlNSh/mediahub-os/pull/585

## Project mission and boundaries

- Main goal: deliver Contour A as a verifiable autonomous engineering environment using GitHub-hosted executors, safe free-cloud model routing with resumable quotas, secret isolation, auditable provenance and governance.
- Contour B must not start until Contour A is deployed and independently accepted.
- Preserve historical IDs and Baseline 2.0 as the canonical functional reference.
- GitHub is for cloud development/routing; servers are for local computation only.
- Search for stable, mature upstream components before building equivalents.
- Separate design, implementation, testing, verification, qualification, release, deployment and acceptance.
- Technical capability does not imply authorization.
- Never bypass issuer/capability checks or blur Jarvis, ASTRA A0 and MediaHub Product State Authority.
- Protect secrets and budget limits; do not inspect or expose secret values.
- Do not merge, deploy, dispatch agents or claim acceptance without explicit evidence and required gates.

## Executor and controller policy

- Gemini Agents 1/2/3 may only be dispatched through the approved workflow `.github/workflows/gemini-batch-dispatch-controller.yml`.
- Before any controller run, verify current workflow contract, exact input compatibility, required Secrets/Variables names against workflow code, governance gates, target immutable SHA, and branch/CI state.
- If any required name/configuration is mismatched or unverified, mark **BLOCKED / NOT RUN** and continue with safe independent work.
- Do not create aliases or rename secrets without a reviewed contract change.
- Do not claim an agent received an individual task unless the controller input and child run evidence prove it.
- For each authorized run record target SHA, controller run ID, child run/job IDs, terminal statuses, artifacts/digests, tests and independent verification. Missing evidence stays **NOT VERIFIED**.
- Claude Code local work is allowed only on the confirmed third server with verified SentinelX host ID/capabilities/allowlist and a qualified approved free route without paid fallback. Server 3 is not for Gemini transport or execution.
- Read current agent-browser instructions and verify browser availability before browser tasks.

## Last confirmed baseline in this continuation

Microstep report created and re-read successfully:
- Report: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-REF-BASELINE-MICROSTEP-2026-10-29.md
- Report blob SHA: `b404d7a25e0a8483f44e7b50439d43f434408d91`
- `main` observed HEAD: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Canonical documentation branch HEAD after creating that report: `dcd2d07e5ece21dc46f7d8900eb707e4e34118ff`
- The docs branch HEAD above is the last observed value for that microstep only. Re-fetch all refs before further work.
- PR #583 and #585 metadata were queued as the next small read-only check but were not confirmed in the final tool output after the microstep report. Re-fetch their current state and exact head SHAs.
- Prior Wave 446 evidence (re-check before relying on it):
  - PR #585 head previously observed: `c2fc46bbab80301106764060d77336b3bea57e82`
  - Astra Verify run `40831136343`: completed/success for that head.
  - Astra Cloud Runtime Validation run `40831136328`: completed/success for that head.
  - Combined status was pending with zero contexts; formal reviews were zero; effective branch protection/required checks remained **NOT VERIFIED** because the branch-protection API returned HTTP 403.
  - PR #583 head previously observed: `265a6116874739d1826fc5c7dda84b5b8b8f9eeb`; two admission/dispatch checks were skipped, so this was not an agent batch.
  - These are historical observations, not a current state claim. Re-check exact head and workflow evidence.
- Upstream candidate register previously had 128 entries: 99 CANDIDATE, 22 CONDITIONAL, 2 REFERENCE_ONLY, 5 EXCLUDED_FROM_ACTIVE_SHORTLIST. Discovery was open/not frozen; comparison/adoption not started. Three entries (zizmor, Trivy, gVisor) had release/tag commit SHAs/blob IDs, but lockfile audits, advisory reviews, upstream exact-CI audits and default-branch HEAD equivalence checks were still zero. Re-verify before relying on counts.
- No Gemini dispatch, child agent runs, model inference, secret access, local executor run, merge, deployment, qualification, component adoption or acceptance was evidenced in Wave 446.

## Required /next procedure — keep it small

1. **One small step only.** Begin with read-only state discovery, and limit the first step to a small set of refs/files. Do not launch many parallel operations.
2. Read Bootstrap, map, checkpoint and Roadmap in bounded chunks as needed. If Contents API returns empty content, fetch the blob by SHA or use raw content. Record the exact ref and SHA.
3. Check current `main` and canonical docs branch HEAD, then the active PR/Issue and exact-head CI. Do not infer current state from this file.
4. Select one bounded action that advances the highest-priority open Roadmap item and does not cross an unmet governance gate.
5. Prepare a small package with one immutable target SHA, goal, inputs, explicit prohibitions and acceptance criteria if delegation is authorized.
6. Before any change, check provenance, current file SHA and branch destination. Avoid overwriting concurrent work.
7. After a change, re-read the entire changed file, confirm blob SHA and new commit/HEAD, run only relevant safe tests, and inspect exact-head CI.
8. Write a dated report. Update checkpoint and map pointers when needed; update Master Roadmap only when its state materially changes. Link reports directly.
9. Report status with these exact distinctions: **PLANNED, DISPATCHED, RUNNING, SUCCEEDED, VERIFIED, QUALIFIED, ACCEPTED, NOT RUN, BLOCKED, FAILED, NOT VERIFIED**.
10. End with evidence links, blockers, the canonical map link, and exactly one next microstep. If owner action is required, append a separate final bold uppercase section with step-by-step links, exact copy text and expected result.

## First next microstep

Perform a small read-only check of current PR #583 and PR #585 metadata only: state, draft flag, merged flag, base/head refs, exact head SHA, updated timestamp, and current review/check evidence if readily available. Do not modify either PR and do not dispatch Gemini. Record results in the next dated report only after the state has been re-checked.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
