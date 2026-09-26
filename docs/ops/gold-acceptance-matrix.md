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
