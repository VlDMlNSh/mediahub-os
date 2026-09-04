# MH-22 — Master Prompt / Reverse Master Prompt Interface

## Purpose

This document defines the durable interface between the canonical MH-22 architecture record and the separate development chat.

## Master Prompt: architecture → development

Provide: accepted constraints, invariants, required artifact, decision ID, scope, forbidden authority changes, evidence required, verification gate, and explicit statement that implementation is authorized only within that scope.

## Reverse Master Prompt: development → architecture

Return only: implementation revision, tests/evidence, artifacts, observed deviations, unresolved unknowns, security impact, operational impact, proposed decision, and rollback/recovery evidence. Do not return a long implementation discussion as architecture truth.

## Boundary

The MH-22 chat is a canonical architecture/governance store. It is not the development workspace. Long-running implementation, debugging, refactoring and exploratory coding belong in the separate development chat.

## Durable record

GitHub is the external durable record. ChatGPT architecture chats are not the sole source of truth.
