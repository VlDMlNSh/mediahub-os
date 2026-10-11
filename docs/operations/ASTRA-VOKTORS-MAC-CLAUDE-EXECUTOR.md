# ASTRA-VOKTORS-MAC-CLAUDE-EXECUTOR.md

## Purpose
This document outlines an execution plan and requirements for the fast permanent local executor lane on Voktors-Mac-mini.local utilizing the node-local qwen2.5-coder:1.5b backend. The executor is bound to the exact target-SHA and run in an isolated branch. Promotion is fail-closed, and the worker does not write directly to main. Credential management is disabled, ensuring no access to any production infrastructure, user data, or unrelated paths. The worker will produce a real execution result and a real independent verifier verdict; synthetic or prefilled evidence is invalid.

## Node Identity
- Target Node: Voktors-Mac-mini.local

## Executor Identity
- Exec Driver: claude
- Executor Model: qwen2.5-coder:1.5b
- Executor Process: Running as an independent verifier process

## Authority Boundary
- Executor-Only Authority

## Target-SHA Binding
- The worker will be bound to the exact target-SHA: 26f77703f8149f957bcb8a9b4d12199da8a15385

## Isolated Branch Execution
- Execution will be run in a separate and isolated branch

## Promotion Fail-Closed
- Promotion will be fail-closed, requiring explicit approval

## No Direct Writes to Main
- The worker will not write directly to main. All writes will be directed to a specific branch or a staging area

## No Credentials or Secrets
- The worker will run without any access to production infrastructure, user data, or credentials.
- No secrets or credentials will be included in the document

## Exec Executor Boundary
- The worker will adhere to the executor-only authority boundary set in the environment settings

## Test Execution
- Exec Executor Behavior: The worker will exhibit identical behavior when executed elsewhere, ensuring no variations in performance, output, or internal processes

## Conclusion
This document outlines the execution plan and requirements for the fast and permanent local executor lane on Voktors-Mac-mini.local utilizing the node-local qwen2.5-coder:1.5b backend, ensuring a high level of quality and reliability with strict execution boundaries and adherence to the executor-only authority.
