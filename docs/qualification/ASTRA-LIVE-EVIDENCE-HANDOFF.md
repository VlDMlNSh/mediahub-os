# Astra live-evidence handoff

This document is the exact handoff between repository qualification and the live deployment boundary.

## 1. Install the canonical launcher

On each node, install the matching process-manager manifest from `ops/systemd/mediahub-astra-github-bootstrap.template.service` (Linux) or `ops/launchd/com.mediahub.astra.github-agent.plist` (macOS). Set the exact node identity.

Do not run both the legacy Astra worker and the canonical GitHub Transport worker for the same node.

## 2. Restart through the process manager

Use the node's normal service manager to replace the old worker with the canonical launcher. This is the only step that cannot be performed by repository commits alone.

## 3. Prove identity before any coding task

Submit a `health` command through `control/commands/<node_id>.json`, wait for the node result on its `astra-node/<node_id>` branch, and preserve the returned JSON as fresh evidence.

Validate it with:

```bash
python3 ops/qualification/verify_transport_health.py health.json --agent /home/mediahub/astra-work/astra_github_agent.py --worktree /home/mediahub/astra-work
```

For macOS, substitute the canonical `/Users/voktor/astra-work/...` paths.

## 4. Qualification order

After identity PASS, collect runtime E2E, scheduler E2E, fencing, recovery, backup/restore, and provider/model evidence. Then run `verify_pre_soak_bundle.py`.

A failed identity gate invalidates all downstream live evidence for that node.

## 5. Stop conditions

Stop if the health result reports the legacy transport version, an unexpected agent path, a mismatched worktree, or a source SHA mismatch. Do not start PRE-SOAK.

## 6. Evidence retention

Record command ID, node ID, target SHA, timestamps, returned result, commit SHA, and remote SHA where applicable. Evidence must be attributable to the current deployment, not copied from historical runs.
