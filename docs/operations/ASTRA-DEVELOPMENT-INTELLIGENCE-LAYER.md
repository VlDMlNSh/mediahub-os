# Astra Development Intelligence Layer

Status: CANONICAL DESIGN / IMPLEMENTED PRIMITIVES
Date: 2026-10-08

## Purpose

This layer converts lessons from completed projects into deterministic, reusable development controls. It strengthens Astra without creating a second control plane.

Astra remains authoritative for mission and command identity, claims and leases, G-5 concurrency, executor binding, target SHA, evidence acceptance, A3 verification, promotion and qualification.

Development Intelligence provides planning, classification, checkpoint and knowledge primitives only.

## Pipeline

```text
USER SPECIFICATION
        |
        v
PROJECT CLASSIFIER
        |
        v
ROADMAP COMPILER
        |
        +--> MD BLOCKS --> UNIT GRAPH
        |
        +--> SELECTIVE KNOWLEDGE
                |
                v
        UNIVERSAL FIRST_ACTION
                |
                v
        BOUNDED ASTRA EXECUTION
                |
                v
        VALIDATION / CHECKPOINT
                |
          +-----+-----+
          |           |
        PASS         FAIL
          |           |
          v           v
   CONFIRMED       FAILURE CLASSIFICATION
   KNOWLEDGE             |
                         v
                    RECOVERY PATH
                         |
                         v
                       RESUME
```

## Checkpoint hierarchy

Every future compiler/executor integration should support UNIT CHECKPOINT, FILE CHECKPOINT and PROJECT CHECKPOINT. A checkpoint is evidence of state, not an authority grant.

## Universal FIRST_ACTION

Before executing a unit:

1. read authoritative state;
2. resolve the latest confirmed checkpoint;
3. verify prerequisites and dependency state;
4. load only applicable confirmed failure knowledge;
5. verify target SHA and claim boundaries;
6. execute the bounded unit;
7. validate before checkpointing.

## Failure knowledge

Knowledge follows the strict chain: Failure -> Diagnosis -> Hypothesis -> Fix -> Targeted Validation -> Regression Validation -> Confirmed -> Knowledge Base.

Unconfirmed hypotheses are never promoted into automatic rules. Every record should distinguish CATEGORY (Universal / Platform / Framework/Tooling / Project-specific), CONFIDENCE (Confirmed / Strong / Project-only), symptom vs root cause, wrong approaches, confirmed fix, validation, applicability and recovery point.

## Capability Contract

A task may declare required_capabilities, preferred_roles, verification, qualification.evidence_required and qualification.commit_binding. These fields describe what expertise is useful. They do not select an executor outside the canonical Astra capability matrix.

The permanent production execution topology remains exactly three Claude lanes with G-5 = 3.

## Roadmap compiler boundary

The initial compiler is deliberately conservative and deterministic. It uses explicit Markdown headings/list boundaries and does not invent hidden requirements. Future semantic decomposition must still pass validation before execution.

## Non-authority rule

ECC roles, knowledge records, checkpoints, classifiers and roadmap blocks cannot create claims, alter G-5, change target SHA, promote execution schemes, write directly to canonical main, certify their own work, replace A3 or become the source of truth.

## Regression use

The calculator project should become the first retrospective benchmark: reconstruct the original specification -> MD blocks -> units path; compare compiler output; replay known failures; measure repeated work and checkpoint loss; and verify selective injection of confirmed knowledge.

A second multi-layer project should then be used as an independent benchmark before this layer is considered qualification evidence.
