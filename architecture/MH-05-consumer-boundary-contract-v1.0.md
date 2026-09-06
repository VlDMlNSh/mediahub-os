# MH-05 — Consumer Boundary Contract v1.0

**Status:** ACCEPTED FOR AUTHORIZED IMPLEMENTATION / QUALIFICATION OPEN  
**Owner:** `consumer_boundary`  
**Dependency:** MH-04 State Authority / CTR-001

## Purpose

Provide the single governed ingress for state-changing consumers before requests reach the canonical State Authority.

## Required path

`INPUT → CONSUMER BOUNDARY → AUTHORIZATION/POLICY → COMMAND → CONSUMER CONTRACT → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE`

The boundary MUST reject malformed, unidentified, unauthenticated, unauthorized, incompatible, quarantined, or policy-invalid requests before State Authority mutation.

## Consumer identity

Every request MUST carry an attributable consumer/source identity and correlation identity. Presence, discovery, network reachability, health, readiness, or physical connection MUST NOT establish authorization.

## Single authority rule

The Consumer Boundary MUST NOT own canonical state, persistence authority, event authority, or authorization authority. It validates and routes governed requests to the single State Authority.

## Source classes

UI, local API, device integration, plugin, automation, telemetry/event reaction, AI, cloud, and recovery are consumers/producers of governed requests or observations; none may mutate canonical state directly.

## Event re-entry

An event may trigger a proposal for mutation, but any resulting mutation MUST re-enter this boundary as a governed command. Event delivery itself is observational.

## Failure semantics

Boundary rejection MUST be non-mutating. Boundary uncertainty MUST fail closed. The boundary MUST NOT silently elevate privileges or convert readiness/health into authorization.

## Verification requirements

Implementation qualification MUST include positive path tests plus negative tests for direct mutation bypass, forged consumer identity, missing authorization, remote privilege escalation, event bypass, UI/AI/plugin/device/cloud direct mutation, persistence shadow writes, and recovery shadow authority.

## Scope

Product Owner explicitly authorized MH-05 implementation on 2026-09-06. This contract authorizes MH-05 only. It does not authorize persistence, HA, production release, recovery implementation, or unrelated capabilities.
