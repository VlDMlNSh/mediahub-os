# MH-12 Secrets

Lifecycle: Generate → Store → Use → Rotate → Revoke → Destroy.

Secrets include credentials, API keys, tokens, private keys, certificates and signing material. They are least-privilege, bounded and explicitly auditable.

Secrets must not enter source, Git history, logs, telemetry, AI prompts, diagnostic snapshots or implicit exports. Exact secret store is non-canonical until evidence and ADR.
