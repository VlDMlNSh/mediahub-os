# MediaHub OS — Wave 410: FCC runtime evidence, local-model probe, and fail-closed Gemini review repair

**Date:** 2026-10-23  
**Disposition:** Cloud FCC smoke **SUCCEEDED**; local Ollama inference **RESPONDED BUT CODING ACCEPTANCE FAILED**; Qwen3 probe **FAILED/TIMED OUT**; Gemini fail-closed repair **IMPLEMENTED / EXACT-HEAD CI PASS / INDEPENDENT REVIEW NOT VERIFIED**; local Claude Code **NOT RUN**.

## Canonical context and immutable refs

- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md (blob `75f30750183efe8c6877368e9f0ada48f8e81ea7`).
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md (blob `78fa7dfa02357fe9e95645843e583f8802867d78`; Contents API returned empty, blob API read-back recovered 1,177,267 characters).
- Canonical checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md (blob `573c26ccb7e1b18b09e7b37e684f2dba18dc5026`).
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md (blob `4b45b4bfeb5fcbf2dd409fb98241832283982c95`).
- Issue #301 remains open; it explicitly separates execution, verification, qualification and acceptance.
- Main target at the start of this pass: `0bbdbc8494f67c0b5f385f2bef69087b229d6f95` (includes merged PR #512).
- Controller repair PR: https://github.com/VlDMlNSh/mediahub-os/pull/513
- PR #513 head SHA: `9a2477c3293cf54d858a9f663bdab94553dd5a80`.
- Review child workflow blob at that head: `168da7bfd4d2be1bf316b7dd2d968361949feddc`.
- Fail-closed contract test blob at that head: `29d47b67ae5761d128867fcb42443c8b69bef381`.

## 1. Cloud Claude Code via FCC — real run

- GitHub Actions run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39893365385
- Run ID: `39893365385`; source SHA: `0bbdbc8494f67c0b5f385f2bef69087b229d6f95`.
- Dispatch gate job `120218030525`: **SUCCESS**.
- Bounded worker job `120218052910`: **SUCCESS**.
- Verified step sequence: pinned FCC checkout/install; Claude Code install; OpenRouter free-router probe; isolated empty workspace; Claude Code invocation; bounded evidence upload.
- Artifact `mediahub-fcc-free-route-smoke-39893365385`, ID `12476185098`, digest `sha256:4dffa6efc93e1649272a2cde72f768eaf862964b014506a4de4bec183a49428e`.
- Artifact read-back on the connected host produced:
  - `MEDIAHUB_FCC_FREE_ROUTE_OK`
  - `selected_model=liquid/lfm-2.5-2.6b:free`
  - `request_id=gen-1792724910-lijsyZvl5IckCU8Ejl5E`
  - `total_tokens=48`
  - `route=openrouter/free`
- The run therefore verifies one real FCC/Claude Code invocation through the selected free route and exact response marker. It does not establish broader provider qualification or zero-cost billing outside the worker's enforced free-only route.
- The install-smoke, contract-test and managed-auth-preflight jobs were skipped on this `workflow_dispatch` event; those jobs run on PR events. The runtime job's own managed bearer-token preflight passed, and token values were withheld.

## 2. Local model — inference response and task-quality failure

- SentinelX host: `host_5f7264034bdf0b51`, `Voktors-Mini.Dlink`, agent `0.23.30`, operational and ping successful.
- Local Ollama API `http://127.0.0.1:11434/api/tags` responded. Models listed included `qwen2.5-coder:3b`, `qwen2.5-coder:1.5b`, and `qwen3:4b`.
- Real inference job `job_607e1309bc33` used `qwen2.5-coder:3b`, completed in 17.14 seconds, exit code 0.
- Prompt asked for a minimal `is_hex_sha(value)` returning true only for 40/64 hex characters, with tests for valid and invalid inputs. **Task acceptance FAILED**: the model returned prose/Markdown instead of code-only output, used `assert False` rather than returning false for invalid input, and included contradictory examples. Model endpoint availability is verified; coding-task correctness is not.
- A second `qwen3:4b` structured coding probe `job_f869c6e7a42f` timed out after 90.14 seconds (curl exit code 28, zero response bytes). This is a concrete local latency/availability failure.
- `which claude` and `which fcc-claude` found no executable in the host PATH; `ollama` was present. No local Claude Code task was executed.

## 3. Gemini review child fail-closed defect and repair

Confirmed defect in the merged review child at the start of this pass:
- The Gemini step had `continue-on-error: true`.
- The validator ran only when `steps.gemini.outcome == 'success'`.
- The artifact uploader ran with `if: always()`.
This allowed the child job to conclude successfully while model execution failed, potentially publishing only a manifest/output artifact without validated review evidence.

Repair in PR #513:
- Removed `continue-on-error`.
- Validator now runs with `if: always()`, receives `GEMINI_OUTCOME`, and explicitly exits nonzero unless Gemini outcome is `success`.
- Added a regression test proving failure remains failure even when a valid-looking output file exists; also checks the successful validation path.
- Read-back confirmed the workflow no longer contains `continue-on-error: true`; the guard and test are present at the recorded blob SHAs.

## 4. Exact-head CI evidence for PR #513

All four retrieved workflow runs completed successfully at head `9a2477c3293cf54d858a9f663bdab94553dd5a80`:
- Gemini workflow contract validation: run `39893857980`, job `120219601380`, **SUCCESS**. Logs show test groups of 3, 4, 7, 12, 13 and 2 tests, all OK (41 tests total), including actionlint.
- Astra Verify: run `39893857752`, job `120219600208`, **SUCCESS**.
- Astra Cloud Runtime Validation: run `39893857851`, job `120219601036`, **SUCCESS**.
- Gemini controller probe: run `39893857883`; no-secret caller-context observation and assertion **SUCCESS**, explicit admission and child dispatch **SKIPPED** as expected for probe mode.
- Combined status endpoint returned no legacy status contexts; workflow run/job results above are the evidence used here.

PR #513 remains open and draft. The available GitHub review endpoint returns no formal review records. An external search/review attempt did not retrieve the actual PR diff and therefore is **not** accepted as an independent review. No merge was performed.

## 5. Claude local execution and controller scope

- Only one SentinelX host is operational; the two enrolled development hosts are disabled. The operational Mac is not verified as the authorized third server required by the project instruction for local Claude Code.
- Local Claude Code remains **BLOCKED / NOT RUN**. This is not substituted with an Ollama model.
- Gemini review mode has not been dispatched. Do not dispatch it until PR #513 is accepted through the normal independent-review and merge gates; the current merged child still contains the defect until that repair lands.
- This pass inspected the FCC runtime workflow, Gemini parent controller/child contract and their targeted tests. It is not a claim that every controller/worker in the repository has been exhaustively audited.

## Status and next steps

| Area | Status |
|---|---|
| Cloud FCC / Claude Code free-route smoke | **SUCCEEDED** |
| Artifact and concrete free model ID read-back | **VERIFIED** |
| Local Ollama API/inference availability | **VERIFIED** |
| Local coding task acceptance | **FAILED** |
| Qwen3 local structured task | **FAILED / TIMEOUT** |
| Local Claude Code | **NOT RUN / BLOCKED** |
| Gemini review child repair | **IMPLEMENTED** |
| PR #513 exact-head CI | **PASS** |
| Independent review of PR #513 | **NOT VERIFIED** |
| Gemini review-mode dispatch | **NOT RUN** |
| Contour A acceptance | **NOT ACCEPTED** |

Next bounded pass: obtain a formal independent review for PR #513; after approval and merge, run the fixed Gemini review mode through the trusted main controller, inspect the actual review artifact and digest, then separately qualify the local model path and only run local Claude on a verified authorized third host. Keep all paid fallback disabled.
