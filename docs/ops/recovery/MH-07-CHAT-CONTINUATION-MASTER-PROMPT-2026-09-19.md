# MEDIAHUB OS / MEDIAHUB iOS — MH-07 CONTINUATION
Продолжай существующую историю MediaHub, не начинай проект заново. Lane: mh-7. Worktree: /home/mediahub/dev/parallel-lanes/mh-7. Branch: engineering/mh07-ai-registry-20260919. HEAD: 3990504c61dfef6dd746526995b44dafb5225c2d. R4: 471f709f5633feab7aeb62dd3ea52effad6d2bc4; ancestry PASS.

Сначала прочитай STATUS.md, docs/MASTER-CONTINUATION-PROMPT-2026-09-09.md, все docs/checkpoints/W04C-*.md, recovery/mh-07-reconciliation-2026-09-05.md, recovery/mh-07-reverse-master-prompt-2026-09-05.md, specification/*registry.yaml и существующие AI/provider tests. Это repository evidence. Недоступный буквальный transcript чата не реконструируй как факт.

Сохраняй: State Authority единственный platform authority; Home Assistant Core authority только Smart Home; AI/cloud/mobile/plugins/adapters non-authoritative; fail-closed; R4 immutable; lease/worktree isolation; no secrets; no bypass VPN/sudo/provider restrictions; human-only merge/release/production.

MH-07 frontier: P1.3 AI model/provider/capability registry verification, затем P1.4 provider selector/fallback including offline/degraded behavior. FCM только discovery/benchmark; OpenRouter не runtime authority. Внешние модели остаются CANDIDATE до native adapter + credential + policy + egress + protocol + live evidence.

Loop: OBSERVE → RECONCILE → SELECT → CLAIM → ISOLATE → IMPLEMENT → VERIFY → RECORD → COMMIT → REPLAN → CONTINUE.

Каждый цикл: targeted tests, regression, ruff, diff-check, security, provenance, R4 ancestry, clean worktree. Формат: STATUS/LANE/CHECKPOINT/TASK/LEASE/ACTION/FILES/TESTS/SECURITY/RESULT/EVIDENCE/BLOCKER/NEXT. Не выдумывай CI, cloud auth или credentials.
