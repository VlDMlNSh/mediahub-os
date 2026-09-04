# MH-17 — Command Model

**Status:** CANDIDATE

A device command is an authorized request to an adapter, never a raw protocol packet.

Minimum semantic fields:
- command_id;
- correlation_id / causation context;
- device_id;
- capability + operation + target;
- validated payload and data bounds;
- caller/service identity;
- authorization and policy context;
- timeout/deadline;
- idempotency class/key;
- cancellation semantics;
- expected state/version where required;
- safety class and audit requirements.

Flow:
`Requested → Authorized → Accepted → Dispatched → Sent → Acknowledged → Applied → Confirmed`
with terminal/exception states `Failed, Timed Out, Cancelled, Unknown`.

`Sent ≠ Applied`, `Acknowledged ≠ Canonical State`. Only State Authority can commit canonical runtime state.

Adapters cannot add authority by changing protocol payloads or retries. Any retry policy must preserve the command's declared idempotency semantics.