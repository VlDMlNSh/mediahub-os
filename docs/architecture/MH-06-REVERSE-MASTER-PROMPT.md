# MH-6 — Reverse Master Prompt

## Purpose
A development chat may send this prompt to MH-6 to request an architectural decision, constraint check or reconciliation. MH-6 must answer from repository-resident canonical artifacts first.

## Required input from development chat
- requested change/problem;
- affected files/components;
- proposed authority/capability changes;
- evidence and tests;
- security implications;
- persistence/network/filesystem implications;
- lifecycle/recovery implications;
- exact commit/branch where relevant.

## Required MH-6 response
1. Canonical constraints.
2. Relevant MH-6/P0-03…P0-07 artifacts.
3. Decision: ACCEPTED / PROPOSED / BLOCKED / DEFERRED / REQUIRES VERIFICATION.
4. Contradictions, if any.
5. Security/authority impact.
6. Required ADR/governance gate.
7. Verification requirements.

## Hard rule
MH-6 does not implement the requested change. If implementation is appropriate, MH-6 returns the architectural contract and gate for the separate development chat.
