# MediaHub hybrid cloud + Astra GOLD queue

Timestamp: 2026-09-27T22:48:00Z
HEAD observed before checkpoint: c8b7308a7362ae5f89a23929befbdbdd9d4cdcaf
Previous checkpoint: evidence/checkpoints/2026-09-27T2145Z-mediahub-master-continuation.md

## Active runs
- FreeLLMAPI: 36356066463 — PENDING, zero jobs, head 7bdd382e5cceb1b380f4985ce9b36c351161407f
- Astra GOLD 24h: 36356066470 — PENDING, zero jobs, head 7bdd382e5cceb1b380f4985ce9b36c351161407f
- Cloud Provider Qualification: 36356066509 — SUCCESS
- Astra Verify: 36356211639 — SUCCESS

## Queue
1. Resolve the two pre-existing PENDING runs without duplication.
2. Fresh live qualification of cloud provider/model paths.
3. Fresh ZeroRouter independent qualification.
4. Gemini runtime qualification.
5. Cross-provider failover.
6. Refresh all seven pre-soak evidence files with real runtime evidence.
7. Run pre-soak verifier without --allow-missing.
8. Verify 3-node transport and Astra state.
9. Verify recovery/restart/crash/fencing and backup/restore.
10. Run Astra 24h soak using local-first routing plus only freshly QUALIFIED cloud paths.
11. Independent verification.
12. Final manifest and operational runbook.

## Cloud usage rule
Only provider/model paths with fresh catalog + required live inference evidence may enter GOLD routing. BLOCKED, PARTIAL, CREDENTIAL_MISSING, RATE_LIMIT, BILLING and stale paths remain excluded.

## Execution constraint
GitHub Transport available in this session has no workflow dispatch/cancel action. Existing PENDING runs therefore remain canonical and are not duplicated. This checkpoint records the queue rather than fabricating a launch.

## Secrets
No secret values recorded.
