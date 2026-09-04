# MH-5 — Proposal Model

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

## Definition

A **Proposal** is inert data suggesting a possible operation, change, recommendation, or interpretation. It has no execution or mutation authority.

Typical producers include AI, automation, plugins, analytics, optimization, diagnostics, and external services.

## Canonical lifecycle

```text
Producer
 → Proposal
 → bounded validation
 → policy evaluation
 → explicit authorization
 → Command conversion
 → P0-05 Consumer Boundary
 → P0-04 State Authority
```

Proposal generation MUST NOT publish canonical state. A proposal may be rejected, retained transiently, transformed, or converted into a command only after the required policy and authorization decisions.

## AI-specific rule

AI output is untrusted proposal data. Prompt output, tool output, retrieved documents, model-generated JSON, or agent recommendations never become executable authority merely because they are syntactically valid or originate from an authenticated AI service.

## Plugin/automation rule

Plugin and automation output remains inert data until the same validation, capability, policy, authorization, and command conversion gates are satisfied. A producer cannot self-grant capabilities through proposal contents.

## Prohibitions

Proposals MUST NOT contain hidden executable callbacks, arbitrary code, shell instructions treated as execution authority, unrestricted credential references, persistence directives, or direct State Authority handles.
