# ASTRA GOLD — Candidate vs mandatory path governance mapping

Status: INTERNAL GUIDANCE / NOT A GATE
Date: 2026-10-02
Purpose: clarify how mandatory and candidate execution paths are treated and
how concurrency/concurrency guards interact with candidate expansion.

This document is guidance only. It is not part of the canonical gate contract
and does not promote any gate.

## Mandatory paths

The mandatory path set is fixed to:

- CODEX_FCC
- CLAUDE_FCC
- CODEX_OMNIROUTE
- CLAUDE_OMNIROUTE
- CLAUDE_CODE_DIRECT

The mandatory set is unchanged until independently qualified proof exists for
a given alternative. That requirement is stated in the governance contract
(`executor_classes.extension_policy`).

## Candidate paths

Candidate cloud executors are enumerated in
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`. They include:

- GEMINI_DIRECT
- PERPLEXITY_DIRECT
- KIMI_DIRECT
- DEEPSEEK_DIRECT
- OPENAI_DIRECT
- ANTHROPIC_DIRECT
- GIGACHAT_DIRECT
- OPENROUTER_GATEWAY

and in the unified model
`architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml`
(`cloud_executor_fabric.candidate_paths`).

## Expansion rules

- Candidate paths do not replace mandatory paths until they are independently
  qualified.
- Any expanded path still requires its own admission ladder:
  credential present, auth success, model discovery, non-mutating probe, task
  execution, result validation, and independent A3.
- Any expanded path still requires its own fresh rounds. The governance
  contract states `promotion_requires_rounds: 23`.
- Gateway success is not native-provider qualification.
- Provider identity is preserved in evidence.

## Concurrency guard notes

When expanding or adding candidate paths, the following concurrency-related
notes apply as guidance:

- The mandatory concurrency guard remains `max_parallel_autonomous_claims: 2`
  and requires disjoint claims and serialized shared surfaces.
- Expanded candidate usage may interact with concurrency in practice, so any
  operational deployment must account for distribution/overlap behavior
  explicitly before treating the expanded matrix as ready.
- Gateway-mediated candidate usage is especially relevant for overlap handling:
  if a candidate is reached only through a gateway, the deployment must still
  preserve provider identity and avoid treating gateway success as native
  provider qualification.

## How this fits the strengthening plan

This mapping supports the reinforcement priorities document by making explicit:

- which paths are mandatory now;
- which paths are candidates;
- what an expansion would need to preserve (identity, rounds, admission,
  concurrency behavior, gateway/native separation);
- that any change to mandatory or candidate scope is itself a governance
  decision and should be auditable.

No gate is promoted by this document.
