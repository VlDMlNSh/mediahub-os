# GOLD acceptance matrix

| Gate | Required evidence | Current status |
|---|---|---|
| Control Plane architecture | architecture contract + focused regression | PASS — contract recorded; focused tests pass |
| P0/P1 state safety | idempotency, fencing, lease, retry, ambiguity, duplicate-owner tests | PASS — existing qualified suite + focused regression |
| Task lifecycle | strict stage transitions + machine-verifiable DoD | PASS — implemented and tested |
| Local model registry | capability/status-aware routing gate | PASS — implemented; legacy qualified records preserved |
| DF3 Ollama | live marker + coding patch + test | OPEN — qualification runner active; no PASS evidence yet |
| Autonomous coding E2E | SELECT→CLAIM→EXECUTE→VERIFY→COMMIT→PUSH | OPEN — admissible patch not yet proven |
| Mid-task recovery | kill during EXECUTE and recover fenced task | OPEN |
| DF1/DF2/DF3 distributed E2E | real multi-host ownership/fencing | OPEN |
| Physical cold boot | automatic service/model/Astra recovery | OPEN |
| Provider failure matrix | timeout/429/403/malformed/ambiguous | PARTIAL — contract tests exist; fresh live qualification open |
| Gemini multimodal | text/structured/image/file/document | OPEN |
| OpenRouter coding | real coding execution | OPEN |
| Zhipu/GLM | live credential + marker/coding evidence | NOT QUALIFIED |
| Claude→OmniRoute | context-safe end-to-end coding evidence | NOT QUALIFIED |
| Automatic qualification scheduler | discovery→qualification→register | OPEN |
| Automatic task generation | new tasks from backlog/failure/regression/capability | OPEN |
| 24h soak | continuous useful autonomous progress | RUNNING/OPEN |
| 72h soak | failures + recovery + qualification cycles | RUNNING/OPEN |
| Security sweep | independent security evidence | OPEN |
| Disaster recovery | host/worker/model/CP/SQLite/network/provider/Astra recovery | PARTIAL |
| GOLD release | all mandatory gates fresh and green | NOT QUALIFIED |

## Fresh verification wave — 2026-09-26

- Full DF3 regression: **901 passed, 2 warnings, 27 subtests**.
- Focused lifecycle/model/Control Plane regression: **51 passed**.
- Astra edge/task gateway/lease/worker-loop regression: **21 passed**.
- Native agent launcher after installing Codex CLI 0.157.1: **7 passed**.
- DF3 Ollama exact marker: **PASS**.
- DF3 Qwen2.5-Coder 1.5B coding/patch qualification: **NOT_QUALIFIED**; evidence recorded in `docs/ops/df3-qwen15b-qualification-20260926.md`.
- Autonomous local agent E2E attempt: **IDLE** because the canonical queue is fully encoded and no eligible bounded task exists; this is not an autonomous coding PASS.
