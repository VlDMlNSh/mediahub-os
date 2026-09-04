# MH-17 — Command Lifecycle

**Status:** CANDIDATE

`Requested → Authorized → Accepted → Dispatched → Sent → Acknowledged → Applied → Confirmed`

Exception states: `Failed`, `Timed Out`, `Cancelled`, `Unknown`.

Every transition is explicit and auditable. `Sent` means transport dispatch evidence only. `Acknowledged` means protocol-level acknowledgement only. `Applied` requires device evidence where available. `Confirmed` requires acceptable reverse telemetry/verification. If physical outcome cannot be established, state remains `Unknown`; it must not be guessed from timeout or acknowledgement.

Canonical runtime mutation remains a State Authority concern; command outcome is evidence, not an authority bypass.