# Astra fresh qualification contract

This contract defines the evidence order after the canonical transport launcher has been installed on a node. Qualification consumes evidence; it does not migrate a process manager.

## Single-node sequence

1. Transport identity — fresh health result passes verify_transport_health.py.
2. Runtime E2E — a bounded coding operation executes through the transport and returns successful evidence.
3. Scheduler E2E — two consecutive cycles prove the generated task targets the new remote SHA rather than a stale lease SHA.
4. Fencing — stale or duplicate ownership is rejected and a valid lease can complete.
5. Recovery — restart or lease-expiry recovery is demonstrated with fresh evidence.
6. Backup/restore — current control-plane state is backed up and restored with integrity evidence.
7. Provider/model — the configured local model/provider path completes a bounded task and records model identity and artifact evidence.

Only after all seven produce fresh status=PASS evidence may the PRE-SOAK bundle gate pass.

## Three-node sequence

Repeat transport identity and runtime evidence for mh-dev-01, mh-dev-02, and Voktors-Mini.Dlink. Then demonstrate multi-node fencing against the same task identity. A result from one node must not be accepted as proof for another node.

## Evidence freshness

Each evidence record must identify at minimum: node_id, execution/task identity, target SHA, completion timestamp, status, relevant commit/remote SHA where applicable, and artifact/test evidence where applicable.

Historical CI runs are useful regression evidence but do not substitute for fresh live deployment evidence.

## Hard stop

If transport identity is stale, any downstream result is non-qualifying. Do not start the 24-hour soak.

## Current deployment boundary

The repository contains the canonical launcher and qualification gates, but the actual process-manager migration on the three live nodes remains an external deployment action. This contract does not bypass that boundary.
