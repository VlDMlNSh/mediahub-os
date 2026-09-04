# Architecture Chat Governance — MH-01…MH-23

Status: GOVERNANCE BASELINE / PROPOSED
Date: 2026-09-04

## 1. Purpose

The MH-01…MH-23 chats are custodians of the reference architecture and architectural decisions for MediaHub. GitHub is the durable repository of record; ChatGPT chats are working custodians and human-readable architectural contexts.

This document defines how architecture chats and the separate development chat interact without mixing architecture with implementation work.

## 2. Separation of responsibilities

### Architecture chats MH-01…MH-23

Allowed:
- architecture analysis and review;
- contracts, invariants, boundaries and acceptance criteria;
- evidence/unknown/contradiction registers;
- architectural decisions and ADR inputs;
- master prompts and reverse master prompts for developer handoff;
- synchronization of the architectural baseline into GitHub.

Forbidden:
- production implementation;
- feature coding;
- prolonged implementation/debugging discussion;
- treating a prototype or code change as architectural truth without review;
- silently changing another MH domain's authority boundary.

### Separate development chat

Responsible for:
- implementation;
- code changes;
- tests and CI execution;
- debugging and refactoring;
- implementation-specific technical choices within approved architectural constraints.

The development chat must not redefine canonical architecture by itself. If implementation reveals an architectural gap or contradiction, it returns an architectural question to the appropriate MH chat and/or records an evidence item for review.

## 3. GitHub is the durable synchronization layer

Do not rely on ChatGPT conversation history as the sole long-term store.

For every MH architecture chat, the durable baseline should be represented in GitHub under `docs/architecture/` with:
- canonical architecture document;
- decision log;
- evidence register;
- contradiction register;
- unknowns/blockers;
- acceptance criteria;
- domain-specific contracts and schemas where applicable;
- chat synchronization record when a major architecture pass is completed.

A chat may contain discussion context, but GitHub contains the durable architectural artifact that the development process can inspect independently.

## 4. Master Prompt contract

A Master Prompt is the developer-facing request generated from an MH architecture chat. It is a constrained implementation handoff, not a license to change architecture.

A Master Prompt must include:
1. MH domain and scope;
2. architectural status;
3. applicable invariants and authority boundaries;
4. required contracts/interfaces;
5. dependencies on P0-03…P0-07 and other MH domains;
6. allowed implementation scope;
7. forbidden shortcuts/bypasses;
8. required tests and evidence;
9. unresolved unknowns/contradictions;
10. acceptance gate;
11. exact GitHub artifacts to consult/update;
12. requirement to report deviations back to the architecture owner.

## 5. Reverse Master Prompt contract

A Reverse Master Prompt is the development-to-architecture return package. It must allow the architecture chat to reconcile implementation reality with the reference architecture.

It should contain:
1. implementation summary;
2. changed files/components;
3. tests and exact results;
4. evidence with versions/platform/configuration;
5. deviations from architecture;
6. new unknowns;
7. contradictions discovered;
8. security/privacy findings;
9. performance/resource findings;
10. compatibility findings;
11. proposed architectural changes, if any;
12. links/paths to durable GitHub artifacts.

Implementation is not considered architectural truth merely because it exists in code. Architecture changes require explicit architectural review and synchronization.

## 6. Conversation hygiene rule

Architecture chats are intentionally short-lived working sessions around architecture passes. Avoid prolonged coding sessions, iterative debugging, implementation chatter or unrelated discussion in MH-01…MH-23.

When an architecture pass is complete:
- synchronize the result to GitHub;
- record status and open gates;
- produce the Master Prompt if development handoff is required;
- stop implementation discussion in the architecture chat;
- continue implementation only in the separate development chat.

## 7. Status semantics

Architecture status values must remain explicit. `PROPOSED`, `OBSERVED`, `VERIFIED`, `BLOCKED`, `CONTRADICTION`, `REQUIRES VERIFICATION`, `ACCEPTED` and `FROZEN` are not interchangeable.

Code existing in a development branch does not by itself make an architecture decision `ACCEPTED` or `FROZEN`.

## 8. Cross-domain authority rule

No MH chat may grant itself authority over another domain. Cross-domain changes require:
Architecture → dependency/impact review → security/privacy review where applicable → evidence → decision → synchronization.

P0 canonical authority boundaries remain higher-order constraints.

## 9. Long-term retrieval rule

Future development sessions should be able to reconstruct the relevant architecture without depending on the original ChatGPT conversation. The primary retrieval path is:

GitHub `docs/architecture/` → relevant MH architecture document → decision/evidence/unknown/contradiction registers → Master Prompt / Reverse Master Prompt.

## 10. MH-18 application

MH-18 follows this governance. Its current architecture remains `PROPOSED / NOT ACCEPTED / NOT FROZEN`; its repository artifacts define contracts and gates, not production authorization.
