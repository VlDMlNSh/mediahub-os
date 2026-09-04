# MH-14 — DEVELOPMENT INTERFACE

## Purpose

This document prevents architecture chats from becoming implementation workspaces and provides a durable protocol for a separate development chat.

## Architecture chat rules

Architecture chats MH-1…MH-23 are reference/governance custodians. They may define contracts, invariants, decisions, evidence requirements and acceptance gates. They do not host production implementation, iterative debugging, long feature-development discussions or implementation-specific worklogs.

## Development chat rules

Development consumes architecture through the relevant master prompt and repository artifacts. Development may implement only what is authorized. Implementation findings do not automatically change architecture.

## Forward interface

Architecture -> Development:
- applicable baseline;
- invariants;
- contracts;
- authorized scope;
- forbidden behavior;
- required tests;
- evidence requirements;
- unresolved ADRs/unknowns.

## Reverse interface

Development -> Architecture:
- exact implementation facts;
- reproducible tests;
- observed failures;
- security/privacy findings;
- performance/resource evidence;
- contradictions;
- proposed ADRs;
- requested decision.

Use `MH-14-reverse-master-prompt.md` for the report schema.

## No implicit architecture mutation

The following do not change MH-14 by themselves:
- code exists;
- tests pass;
- a database was selected by a developer;
- a filesystem happens to work;
- a backup file was created;
- a migration succeeded once;
- a cloud service is available;
- an implementation is faster/easier.

A change requires the architecture change protocol and, where applicable, governance approval.

## Long-term source model

Chat = reasoning context.
GitHub = durable external architecture record.
Development repository/code = implementation record.
ADR/governance decision = authority for architecture changes.
