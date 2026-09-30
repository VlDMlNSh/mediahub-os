# MediaHub OS — GitHub Component Registry

Дата фиксации: 2026-09-30

## Назначение

Единый реестр GitHub-компонентов проекта. Реестр описывает фактически присутствующие workflow и их операционную роль; наличие workflow не означает прохождение соответствующей runtime-квалификации.

## CORE_CONTROL

| Компонент | Workflow | Назначение | Состояние |
|---|---|---|---|
| Astra Autonomous Supervisor | astra-autonomous-supervisor.yml | автономный supervisor узла mh-dev-01, команды, worker lifecycle | READY |
| Astra Queue Recovery | astra-queue-recovery.yml | восстановление очереди/команд | READY |
| Astra Verify | astra-verify.yml | базовая проверка репозитория и control-path | READY |
| MediaHub Bridge | mediahub-bridge.yml | bridge/control integration | PRESENT |
| Astra Cloud | astra-cloud.yml | cloud orchestration surface | PRESENT |

## QUALIFICATION

| Компонент | Workflow | Назначение | Состояние |
|---|---|---|---|
| Execution Backend Qualification | astra-node-provider-backend-qualification.yml | qualification execution backends | READY |
| Cloud Provider Qualification | mediahub-cloud-provider-qualification.yml | cloud provider qualification | PRESENT |
| Live Provider Qualification | mediahub-live-provider-qualification.yml | live provider probes | PRESENT |
| FreeLLMAPI Qualification | freellmapi-qualification.yml | FreeLLMAPI qualification | PRESENT |
| UnoRouter Qualification | unorouter-qualification.yml | catalog/API/inference qualification | PRESENT; inference not qualified by latest evidence |
| ZeroRouter Qualification | zerouter-qualification.yml | catalog/API/inference qualification | PRESENT; inference blocked by latest evidence |
| Provider Cross-Key Auth Audit | provider-cross-key-auth-audit.yml | cross-key authentication audit | PRESENT |
| SiliconFlow live probes | siliconflow-key2-live-probe*.yml | targeted SiliconFlow probes | PRESENT |

## VERIFICATION

| Компонент | Workflow | Назначение | Состояние |
|---|---|---|---|
| Federation Admission PoC | federation-admission-poc.yml | deterministic admission contract validation | IMPLEMENTED; fresh runtime evidence must be retained |
| P0-07 Verification | mediahub-p0-07-verification.yml | P0-07 verification | PRESENT |
| P0-08 Verification | mediahub-p0-08-verification.yml | P0-08 verification | PRESENT |
| Runner Migration Smoke | mediahub-runner-migration-smoke.yml | runner migration smoke checks | PRESENT |
| Claude Worker | mediahub-claude-worker.yml | Claude worker execution surface | PRESENT |

## GOLD / RELEASE GATE

| Компонент | Workflow | Назначение | Состояние |
|---|---|---|---|
| Astra GOLD 24h real soak | astra-gold-24h-soak.yml | 24h GOLD soak | ACTIVE RUN #176; do not disturb |
| GOLD admission protection | astra-gold-24h-soak.yml trigger/concurrency policy | ordinary commits must not launch new GOLD soak | PROTECTED on current workflow; historical run #177 predates protection |

## ARCHITECTURE CHECKPOINTS

Канонические документы покрывают:
- local MediaHub Cluster vs Cloud Development Cluster;
- Media Data Plane / Federation Control Plane / Protected Registration Plane;
- Media Fabric storage/transport/data locality/compute/scheduler/job contract;
- Federation Admission PoC;
- Central Protected Registration Gateway (CPRG).

CPRG правило: VPN используется исключительно для API-key registration. Остальные узлы VPN-free; media/data/storage/compute/ordinary Internet не проходят через CPRG.

## IMPORTANT QUALIFICATION RULES

1. API key presence или /models catalog access не является inference qualification.
2. Provider failure classifications должны отражать фактическую свежую evidence.
3. OpenAI direct исключён из текущего qualification scope по решению проекта; UnoRouter и ZeroRouter остаются в scope.
4. Секреты не должны покидать GitHub Secrets/approved secret boundary.
5. GOLD #176 остаётся нетронутым до завершения его текущего 24h цикла.
6. Исторический GOLD #177 не использовать как qualification evidence.
7. Production deployment для Federation Admission PoC/CPRG не считать выполненным только по наличию контрактов или deterministic harness.

## Следующие gates

1. Свежий runtime evidence Federation Admission PoC.
2. Mesh PoC для local MediaHub Cluster.
3. Media Data Plane PoC.
4. Compute Fabric PoC.
5. Scheduler runtime.
6. CPRG protected-registration PoC.
7. Security/recovery/fencing verification.
8. Distributed qualification.
9. Только после всех gates — новый явный GOLD admission/run.
