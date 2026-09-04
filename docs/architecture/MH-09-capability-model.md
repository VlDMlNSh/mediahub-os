# MH-09 — Capability Model

**Status:** PROPOSED / REQUIRES VERIFICATION

UI capabilities are explicit, operation-specific, identity-bound, authorization-bound, auditable, least-privilege and deny-by-default.

Forbidden: wildcard capabilities, self-grant, implicit inheritance, capability escalation, capability inferred from screen visibility, disabled controls as security, cached credentials as authorization, or UI-only authorization.

A presentation surface may request an operation but never mint or widen the capability required for it. Capability verification remains outside the presentation layer.
