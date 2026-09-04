# MH-17 — Architecture Chat Governance

Status: PROPOSED / NOT ACCEPTED / NOT FROZEN

## Purpose

This document defines the operating boundary for the MH-17 architecture chat and its relationship to GitHub and the separate development chat.

## Canonical roles

- MH-17 chat: architecture authority for Device / Protocol / Integration decisions, evidence classification, contradictions, unknowns, ADR direction, acceptance criteria, and governance state.
- GitHub: durable repository record of architecture artifacts, evidence registers, decision logs, contradiction registers, unknowns, and accepted/frozen revisions.
- Development chat: implementation workspace. It may consume MH-17 Master Prompt / Reverse Master Prompt, but it does not redefine MH-17 architecture authority.
- Production implementation: prohibited from being authorized by discussion in MH-17 alone; it requires the stated governance gates.

## Non-goals of MH-17 chat

The MH-17 chat must not become a general development workspace. Avoid prolonged implementation debugging, routine coding, speculative integration work, or unrelated design discussion here.

## Evidence discipline

Use:

Evidence → Canonical State → Decision → Architecture → Implementation → Verification → Governance Acceptance → Freeze

No VERIFIED, PASS, ACCEPTED, FROZEN, QUALIFIED, or PRODUCTION READY status without evidence.

Unknown facts remain UNKNOWN / REQUIRES VERIFICATION.
Proposals remain PROPOSED / CANDIDATE until justified.

## GitHub synchronization

Architecture artifacts should be committed to the repository so the project does not depend on ChatGPT conversation persistence. Architecture branches/PRs may be used as staging and review mechanisms. Main must not be treated as proof of acceptance unless governance evidence explicitly establishes acceptance.

## Development boundary

The following are not authorized merely by MH-17 architecture discussion:

- production device connections;
- production commands;
- firewall/network changes;
- opening ports;
- broker installation;
- pairing/enrollment;
- credential provisioning;
- firmware updates;
- production automation.

Required gate:

Architecture → Security Review → Evidence → ADR → Governance Authorization

## Master Prompt / Reverse Master Prompt

The architecture chat may publish a compact Master Prompt for development consumption and receive a Reverse Master Prompt containing implementation findings, evidence, contradictions, and requested architectural decisions. The reverse prompt is evidence input; it does not automatically mutate canonical architecture.

## Current MH-17 state

NOT ACCEPTED / NOT FROZEN.
No production device authority is granted by this document.
