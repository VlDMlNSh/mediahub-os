# MediaHub LLM Gateway — эталонная конфигурация

## Состояние
Кандидатная ветка: `feature/gateway-ethalon`. New API используется как upstream relay/control substrate; MediaHub не копирует AGPL source. Перед production/GOLD image `calciumion/new-api:latest` должен быть заменён на проверенный release tag/digest.

## Ёмкость
| Канал/класс | Лимит/оценка | Токены/день |
|---|---|---:|
| Mistral ×2 | ~1B/account/month | ~66M |
| SiliconFlow ×2 | 1000 RPM, 50K TPM | ~40-60M |
| Novita ×2 | 60 RPM, 5 free models | ~10-20M |
| Z.ai ×2 | ~1000 RPD/account | ~2-4M |
| DeepSeek | 10 RPM, 100K TPM, trial | ~5-10M |
| HF | ~300 RPM, <10B/cold start | ~2-5M |
| Kimi | 3 RPM, 500K TPM, 1.5M TPD | ~1.5M |
| LLM7 | 2 RPS, 40 RPM, 1M TPD | ~1M |
| SambaNova | 20 RPD, 200K TPD | ~200K |
| Aion Labs | 15 RPM, 20K TPD | ~20K |
| Cloudflare ×2 | 10K Neurons/day/account | ~20-30K each (estimate) |
| OpenRouter | 50 RPD, no balance | ~100K |
| NaraRouter | 1 key now; 3 planned | ~3-10M |
| UnoRouter | unpublished | ~3-5M estimate |
| ZeroRouter | unpublished | ~3-5M estimate |
| OrcaRouter | unpublished | ~3-5M estimate |
| Gemini | 10 RPM/20 RPD stated in plan | 0-100K, test-and-skip |
| Groq | 30 RPM/1000 RPD/200K TPD stated in plan | 0-200K, test-and-skip |
| **Current aggregate** | | **~165M realistic** |

Capacity figures are planning estimates supplied for this deployment, not guarantees. Router limits must be measured by fresh qualification.

## Routing
1. Burst: Groq → SambaNova.
2. Main routers: OpenRouter → NaraRouter → UnoRouter → ZeroRouter → OrcaRouter.
3. Stable direct: Mistral ×2 → SiliconFlow ×2 → Z.ai ×2 → Novita ×2.
4. Specific: Cloudflare ×2 → Aion Labs → GigaChat when enabled.
5. Fallback: DeepSeek → HF → Kimi → LLM7.
6. Test-and-skip: Gemini/Groq are never hard dependencies.

Failover is triggered by retryable HTTP 408/409/425/429/5xx, upstream transport errors, quota exhaustion and explicit channel disablement. Priority selects the class; weight distributes within a class.

## Test-and-skip
`gateway-init.py` performs startup checks when `HEALTH_CHECK_ENABLED=true`. Gemini calls the Google models endpoint. Groq calls its models endpoint. 403, authentication failure, network failure or non-200 causes a warning and channel omission; it does not block the remaining gateway.

## Secrets
Only environment variable names are committed. Secret values must come from deployment secret storage/GitHub Actions secrets. Do not paste keys into files, logs, issue comments or PRs. `ZEROUTER_API_KEY` is the canonical name everywhere.

## 30 сентября 2026
1. Add `NARA_KEY_2` and `NARA_KEY_3` to GitHub Secrets.
2. Uncomment/enable the Nara key entries in deployment env; the channel topology already accepts all three.
3. Add `DASHSCOPE_API_KEY`, `NOUS_KEY`, `GIGACHAT_API_PERS`.
4. After BOMB verification, fill `BOMB_BASE_URL`, channel type and model mapping; keep it disabled until verified.
5. Restart: `docker compose down && docker compose up -d`.
6. Run: `bash scripts/init-gateway.sh`.

The JSON manifests cannot contain shell comments, so future sections are represented by disabled `_tomorrow_*` records and explicit `comment`/status metadata.

## Расширение
- OpenRouter: verify the stated $10 top-up effect before relying on it; the supplied plan estimates 50 RPD → 1000 RPD and ~100K → ~2M/day, but this is an external commercial claim and requires fresh account-level confirmation.
- DeepSeek: verify the stated $5 paid-tier transition before purchase; trial exhaustion is a capacity risk.

## Узкие места и риски
1. Mistral: monthly cap dominates sustainable average; do not burn 100M/day blindly.
2. SambaNova: 20 RPD makes it emergency-only.
3. DeepSeek: trial capacity is temporary.
4. OpenRouter: RPD is the immediate constraint without balance.
5. Cloudflare Neurons are compute units, not tokens.
6. GigaChat is single-concurrency and should be queued.
7. DashScope trial is time-limited.
8. Kimi has a hard daily cap.

## Gaps / blueprint
- **GAP-1:** exact New API release is not pinned; runtime validation must establish a digest.
- **GAP-2:** provider limits marked “unknown/estimated” need live qualification.
- **GAP-3:** HF endpoint/model compatibility must be verified; it is not assumed from the token alone.
- **GAP-4:** BOMB provider metadata is intentionally unresolved.
- **GAP-5:** current PR must receive fresh runtime evidence before GOLD.
- Blueprint: manifest → secret injection → compose → API bootstrap → health gate → channel registry → alias/fallback → usage/evidence → ASTRA qualification.
