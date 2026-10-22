# MediaHub OS Agentic Development Operating System

Status: PROPOSED FOR REVIEW
Date: 2026-09-07

## Purpose

This document defines the autonomous development operating model for MediaHub OS 11.x LTS / MediaHub iOS. It increases parallel engineering throughput while preserving architectural authority, qualification independence, and immutable evidence.

## Non-negotiable boundaries

1. The immutable forensic target is never rewritten or force-pushed.
2. Canonical state has exactly one State Authority.
3. ConsumerBoundary never owns canonical state, persistence, events, or authorization.
4. Every mutation follows INPUT -> CONSUMER BOUNDARY -> AUTHORIZATION/POLICY -> COMMAND -> STATE AUTHORITY -> CANONICAL STATE -> EVENT -> OBSERVATION -> EVIDENCE.
5. Agents may propose, implement, test, audit, document, and prepare PRs; agents may not self-certify independent qualification.
6. No agent may silently broaden scope, change frozen semantics, or introduce persistence/HA/recovery authority without explicit governance authorization.
7. Unknowns and contradictions are recorded, never guessed away.

## Agent organization

### Architecture Office
Owns contracts, invariants, dependency direction, ADRs, and architectural drift detection.

### Core Runtime Engineering
Implements governed runtime behavior on isolated branches/worktrees.

### Security Engineering
Runs adversarial analysis, negative testing, authority/bypass inventory, and fail-closed verification.

### Qualification Office
Maintains qualification ledgers, evidence manifests, reproducibility references, and gate status. It does not manufacture independence.

### Verification Engineering
Maintains deterministic regression, static checks, contract checks, and system-wide negative verification tooling.

### Release Office
Controls release readiness, branch promotion, evidence completeness, and production authorization.

### Operations / Developer Experience
Maintains the server toolchain, CI runner, remote development access, reproducible environments, and agent execution infrastructure.

## Delegation protocol

Every agent task must have: objective, scope, base SHA, allowed paths, forbidden paths, acceptance criteria, commands, evidence output, and stop conditions.

Agents work in isolated branches/worktrees. Integration happens only after deterministic checks and review. Qualification evidence is never treated as equivalent to author/CI evidence.

## Parallel execution model

- Track A: architecture/contracts
- Track B: runtime implementation
- Track C: security/negative verification
- Track D: tests/tooling
- Track E: qualification/evidence
- Track F: developer infrastructure

Tracks may run concurrently when they do not modify the same semantic surface. Shared-state conflicts are resolved by the Architecture Office before integration.

## Automation policy

Automate discovery, formatting, static analysis, tests, evidence collection, branch hygiene, and status reporting. Keep semantic integration and release authorization gated. Background automation must fail closed on ambiguity, dirty protected branches, unexpected diffs, failing tests, missing evidence, or scope expansion.

## Server policy

The development server is a tool host, not an authority host. AI agents operate with least privilege and isolated worktrees. Local models are optional and must not be installed merely for appearance. On an 8 GiB machine, prefer lightweight/remote inference and existing Codex infrastructure over large local models.

## Independent review boundary

No local agent, including a second model or replay agent, is automatically an independent qualification reviewer. Independence requires a separately identified reviewer/executor and independently produced execution evidence at the governed revision.

## Default completion rule

An agent is done only when code/docs are committed to an appropriate branch, deterministic checks pass, evidence is retained, scope is explicit, and the next handoff is machine-readable.
