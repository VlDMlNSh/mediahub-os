# MH-07 — Observability

Status: CANDIDATE.

Auditable decisions should carry correlation identifier, decision result, source, policy revision, configuration revision, caller context, reason/category and timestamp.

Observability is read-only and cannot grant authority or mutate state. Secrets/credentials are never logged. Audit evidence distinguishes proposal, validation, policy decision, authorization, publication and observed runtime outcome.
