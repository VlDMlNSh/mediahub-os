# MH-03 Error Handling

Principles:
- ambiguity → fail closed;
- malformed input → reject;
- missing authorization → deny;
- stale transaction → reject;
- unknown dependency/device/identity → deny or quarantine according to contract;
- critical foundation failure → not ready or controlled stop;
- optional external failure → degraded operation where safe.

Errors must be stable, bounded and sanitized. They must not expose credentials, secrets, private material or unnecessary internal paths.

Partial lifecycle transitions are forbidden. Failure of a runtime service must not corrupt canonical state.
