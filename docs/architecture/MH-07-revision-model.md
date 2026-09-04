# MH-7 — Revision Model

Status: CANDIDATE

Authoritative configuration/policy publication requiring concurrency control binds to the lower State Authority generation/state version.

Stale candidates fail closed. MH-7 introduces no second transaction authority and no hidden merge, rebase, retry or last-write-wins behavior. Cross-document atomicity is not authorized.

Canonical publication:
Candidate → validate → authorize → controlled ingress → verify expected lower-layer generation/version → atomic commit.
