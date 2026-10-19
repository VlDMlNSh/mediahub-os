---
name: mediahub-next
description: Run a bounded, evidence-driven MediaHub OS /next engineering pass, using the canonical project map and contracts, live GitHub state, scoped implementation, CI evidence, and verified handoff.
---

# MediaHub OS /next Engineering Skill

Use for any /next, Contour A, repository audit, CI/PR, architecture-gap, or project-synchronization task.

## Required retrieval sequence

1. Refresh the live GitHub refs and HEAD for main and docs/mediahub-chat-tree-map-20261012. Record SHA and ahead/behind/merge-base when available.
2. Read these files from the current canonical documentation branch:
   - docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
   - docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
   - docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
   - docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
3. Read docs/checkpoints/mediahub-functional-baseline-2.0.md from main and the primary contracts relevant to the task.
4. Refresh Issue #301, relevant open PR metadata, exact-head CI runs and job steps. A PR title or a test file's existence is not evidence that a test executed.
5. If an API returns empty content for a large file, fetch the exact blob by its returned SHA. Do not infer the file is empty.

## Scope and execution

- Select the next unfinished dependency from the Master Roadmap; do not repeat a closed deliverable unless new evidence invalidates it.
- Preserve historical IDs and Baseline 2.0. Do not silently revive Baseline 1.0 requirements.
- Reuse stable components before custom implementation; pin sources and record license/security/interface evidence.
- Use a fresh branch/worktree from the verified current base. Inspect status and diff before and after editing.
- For behavior changes, write a focused failing regression test first, verify the expected failure, then implement the smallest coherent fix.
- Parallelize only independent tasks. Give each agent a distinct scope and expected evidence; use isolated branches. Treat agent output as an untrusted proposal until source, diff, tests, and provenance are checked.
- Use agent-browser only for browser-visible workflows; it supplements, not replaces, API/source inspection and CI evidence.
- Never assume manual Gemini dispatch, persistent scheduling, or background execution is active without run IDs and current status.
- Do not read secret values, bypass issuer/capability, weaken repository protection, or merge/deploy without the required gates.
- Product State Authority alone owns canonical product-state mutation. Jarvis and ASTRA A0 do not acquire that authority.
- Contour B remains gated until Contour A has evidence of deployment and independent acceptance.

## Evidence and closeout

- Separate observed facts, inference, proposed design, implementation, test execution, verification, qualification, release, deployment, and acceptance.
- Record exact branch/ref, commit SHA, changed paths, blob SHA where available, test commands/results, CI run/job/step IDs, blockers and next action.
- Re-read every changed file after writing and verify exact contents and SHA.
- If a documentation change affects project navigation, update the canonical map and continuation checkpoint on the documentation branch, then read them back by blob SHA.
- Do not report success without direct evidence. If a check cannot run, state why and leave the status unqualified.
