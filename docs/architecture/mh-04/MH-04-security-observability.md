# MH-04 Security Observability

Security observability is non-mutating.

Minimum audit context: principal, operation/capability, resource/context, timestamp/order metadata, authorization decision, policy basis and correlation context where applicable.

Logs/metrics/traces/alerts must be bounded, integrity-conscious and sanitized. Credentials, secrets and unnecessary private data are excluded.

Operational response must re-enter the governed path: observation -> authorized request/command -> policy -> Consumer Contract -> State Authority.