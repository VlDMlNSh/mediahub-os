# Astra transport health gate

Run this gate only against a **fresh** health result from the target live node.

Example:

```bash
python3 ops/qualification/verify_transport_health.py \
  health.json \
  --agent /home/mediahub/astra-work/astra_github_agent.py \
  --worktree /home/mediahub/astra-work
```

The gate requires:

- `transport_version=self-reexec-v1`;
- the reported worktree equals the expected synchronized worktree;
- the reported agent path is exactly the canonical agent in that worktree;
- the reported agent path is inside the worktree;
- `agent_source_sha` equals the SHA-256 of the agent file at that path.

A PASS proves only the transport identity contract. It does not prove runtime,
scheduler, fencing, recovery, multi-node operation, or Gold qualification.
