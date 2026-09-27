# MediaHub OS / Astra — master continuation checkpoint
- checkpoint_time_utc: 2026-09-27T21:45:00Z
- canonical_repository: VlDMlNSh/mediahub-os
- immutable_baseline: 471f709f5633feab7aeb62dd3ea52effad6d2bc4
- latest_evidence_commit: 211e8587d6d7f20947f0b0afd0426f12df8c38ce
- latest_provider_qualification_run: 36352594082
- latest_astra_verify_run: 36352732142
- gold_24h_soak_run: 36349663466
- gold_24h_soak_status_at_checkpoint: in_progress
- canonical_worker_content_sha: 3b4767c33caf4d5a633893e11001426d4a2ecc8b

## Current cloud qualification
- unified workflow: .github/workflows/mediahub-cloud-provider-qualification.yml
- qualification contract: catalog + two model inferences + nonempty marker; secrets suppressed
- OpenRouter: PARTIAL; catalog PASS; at least one live model PASS; another model lane BLOCKED_BILLING
- OpenAI: BLOCKED_RATE_LIMIT in latest live qualification
- Gemini: catalog PASS; live inference/runtime not yet qualified
- UnoRouter: catalog PASS; inference BLOCKED (auth/runtime)
- ZeroRouter: BLOCKED_AUTH / billing evidence from prior runs
- DeepSeek: credential_missing
- Kimi: credential_missing
- Perplexity: credential_missing
- Claude/OmniRoute: credential_missing / live runtime unverified
- FreeLLMAPI: local self-hosted qualification pending

## Runtime/code state
- CloudFirstOrchestrator supports bounded provider/model/credential failover.
- OpenAI native Responses adapter exists.
- Gemini native generateContent adapter exists.
- OpenAI-compatible adapters exist for OpenRouter, Perplexity, Kimi, DeepSeek.
- UnoRouter native adapter exists.
- OmniRoute Claude native Anthropic adapter exists.
- HTTP classification includes 401/403 auth, 402 billing, 429 rate limit, 5xx runtime.
- indexed credential/model failover is supported.
- do not claim any provider QUALIFIED without fresh two-model evidence.

## Node/control-plane state
- nodes: mh-dev-01, mh-dev-02, Voktors-Mini.Dlink
- transport: GitHub commands/results on node branches
- Desktop Commander/SentinelX: prohibited by project contract
- historical worker hardening commit: b8502ed4e399e76ce42db38abe7f74cf28eb0f12
- repair dispatch: 83a3924b8b70016993f6532a4189aea57fa19b8a
- parameterized systemd service: 1ac3924e3d47690b5f00cb981b24e0cdf33a1c68
- latest known node health: all three PASS with canonical worker SHA cd7a83c6b6b8d6065a157274e79e315e2aa5012c0f8ee9466de92980570b9e1a
- node branch heads at last known checkpoint: mh-dev-01 9b4765de8cf208af4930c83e8ffb37039255a9c9; mh-dev-02 9e30e4d716e526abbf66aca60872785f33a9de0a; Voktors-Mini.Dlink 63cd187303d55d1aa6d89c035af5194b38b302d5

## Required next gates
1. refresh FreeLLMAPI self-hosted live qualification and record sanitized evidence
2. diagnose/fix Gemini runtime qualification without weakening secret handling
3. perform live cross-provider failover drill and record success/failure path
4. obtain fresh pre-soak bundle: transport-health, runtime-e2e, scheduler-e2e, fencing, recovery, backup-restore, provider-model
5. run verification of bundle
6. only then advance GOLD gates
7. wait for/verify 24h soak run; do not call it GOLD until all independent gates pass
8. final evidence manifest and recovery/runbook only after fresh evidence

## Historical context to preserve
- prior project chats covered Astra autonomous loop, Control Plane, 3-node qualification, 24h soak, cloud registration, UnoRouter/Zerouter/OmniRoute, SoL-Pi, OpenOPC, OpenFlux, GLM/local-model exploration, VNC/Mac setup, Ubuntu storage.
- SoL-Pi and OpenOPC were evaluated as experimental external layers; not production replacements for Astra Control Plane.
- OpenFlux work must continue only through approved GitHub transport.
- never expose secrets; never bypass auth/billing/quota; never simulate deployment/restart/inference.
