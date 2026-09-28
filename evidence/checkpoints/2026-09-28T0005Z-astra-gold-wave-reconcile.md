# Astra GOLD wave reconcile — 2026-09-28

Timestamp: 2026-09-28T00:05:00Z

## HEAD
- main: eb8deaf41ca969d2c4dbbc2e54c8a7e33805bd32
- previous checkpoint: 2026-09-27T2248Z-cloud-hybrid-gold-queue.md

## Active canonical runs
- FreeLLMAPI Live Qualification: 36356066463 — PENDING; head 7bdd382e5cceb1b380f4985ce9b36c351161407f; jobs=0.
- Astra GOLD 24h real soak: 36356066470 — PENDING; head 7bdd382e5cceb1b380f4985ce9b36c351161407f; jobs=0.
- Astra Verify: 36356526187 — SUCCESS on current HEAD eb8deaf41ca969d2c4dbbc2e54c8a7e33805bd32.
- Cloud Provider Qualification: 36356066509 — SUCCESS; evidence artifact present and unexpired.

## Evidence inventory
Current evidence tree contains provider-model.json and transport-health-current.json plus checkpoints. The required pre-soak bundle is incomplete: transport-health.json, runtime-e2e.json, scheduler-e2e.json, fencing.json, recovery.json, and backup-restore.json are not present as fresh bundle files. verify_pre_soak_bundle.py therefore cannot legitimately pass without fresh runtime evidence.

## GOLD workflow contract
astra-gold-24h-soak.yml checks canonical runner hostname/user, clean git, worker presence, and astra_github_agent.py blob SHA 3b4767c33caf4d5a633893e11001426d4a2ecc8b. Current main tree confirms that exact blob SHA, so the historical SHA gate is NOT currently a mismatch.

## Cloud qualification policy
Only fresh model paths with catalog + required live inference evidence may enter GOLD cloud routing. Current provider evidence remains partial/blocked for several providers. No provider is promoted merely because credential or catalog is present.

## Execution result
No duplicate FreeLLMAPI or GOLD run was created. GitHub Transport exposed no safe workflow-dispatch/cancel operation for the two zero-job PENDING runs. Therefore no fabricated launch, PASS, or 24h result is recorded.

## Next wave
1. Resolve the two canonical zero-job PENDING runs through an available GitHub Actions control path.
2. Fresh live cloud qualification on current HEAD.
3. Build all seven pre-soak evidence files from real runtime.
4. Run verify_pre_soak_bundle.py without --allow-missing.
5. 3-node/recovery/fencing/backup-restore gates.
6. Start one canonical 24h Astra GOLD soak using only freshly qualified cloud paths plus local-first routing.
7. Independent verification and final manifest/runbook.

Secrets: SUPPRESSED.
