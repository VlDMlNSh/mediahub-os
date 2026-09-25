# Astra node command bus

Commands are JSON, bounded to the node worker's fixed vocabulary. Payloads never become shell.
Required fields: `schema:1`, `command_id`, `target`, `action`, `expires_at` (UTC).
Allowed actions: `STATUS`, `SYNC`, `PREPARE`, `STOP`, `RESUME`.
Expired, malformed, or mis-targeted commands are ignored.
Runtime status is written under `.autonomous/node_bus/<node>/` and is not the authoritative Control Plane state.
