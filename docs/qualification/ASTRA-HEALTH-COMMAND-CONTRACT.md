# Astra health command contract

The health probe is the first live qualification action. It is intentionally bounded and read-only.

Command file: `control/commands/<node_id>.json`

Example shape:

```json
{
  "schema": 1,
  "command_id": "health-<node>-<timestamp>",
  "node_id": "mh-dev-01",
  "operation": "health",
  "title": "Astra transport health",
  "description": "Fresh canonical transport identity probe"
}
```

The node must publish a result under `control/results/<node_id>.json` on its node branch. The result must contain the command_id, returncode, completion timestamp, and health payload.

The payload is accepted only if `ops/qualification/verify_transport_health.py` passes against the current canonical worktree.

Do not reuse an old command ID or an old result as fresh evidence. Do not treat branch existence as proof that the live process consumed the command.
