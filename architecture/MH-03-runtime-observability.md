# MH-03 Runtime Observability

**Status:** PROPOSED

Observability covers logs, metrics, health, diagnostics and traces as available. Observability is an observer and must not become a mutation path.

Diagnostics may produce observation, alert or recommendation. Any requested mutation must re-enter the governed command → policy/authorization → Consumer Contract → State Authority path.

Runtime observability must make lifecycle transitions, dependency failures, degraded state, recovery attempts and authority-path failures diagnosable without exposing unrestricted credentials or bypassing trust boundaries.
