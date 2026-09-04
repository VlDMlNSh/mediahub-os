# MH-09 — Session Model

**Status:** PROPOSED / REQUIRES VERIFICATION

A UI session is presentation context, not authority. Authentication context and authorization context are distinct and must not be conflated with navigation or cached credentials.

Session concerns include identity reference, authorization context reference, correlation/request identifiers, lifecycle, expiration, cancellation and reconnect handling. Session loss must fail closed for privileged actions. Reconnect must re-establish required authentication/authorization context rather than silently reusing presentation state.
