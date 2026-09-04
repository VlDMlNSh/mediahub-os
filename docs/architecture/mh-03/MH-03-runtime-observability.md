# MH-03 Runtime Observability

Observability is an observer plane and is non-mutating.

Sources may include lifecycle facts, bounded health signals, metrics, logs and diagnostics. Collection and output must be bounded and sanitized.

Observability may produce:
- observation;
- alert;
- recommendation.

It cannot directly mutate canonical state. Any operational response must re-enter the governed path: observation → authorized request/command → policy → authorization → P0-05 → State Authority.

Observability must not expose credentials, secrets, private material or unnecessary personal data.
