# Worker Secret Scan and Project Skill — Implementation Plan

> For agentic workers: Follow repository agent instructions and the project-local mediahub-next skill. Use test-first changes for executable behavior.

**Goal:** Repair the distributed worker's secret-assignment detector, add executable regression coverage, and make MediaHub's /next retrieval and evidence protocol durable for repository agents.

**Architecture:** Keep the existing security_gate API and fail-closed finding format. Add unittest-discoverable tests that exercise the public gate against temporary files. Add a thin root AGENTS.md that routes agents to canonical project documents and a focused .agents/skills/mediahub-next/SKILL.md; do not duplicate the large architecture map.

**Tech Stack:** Python 3.12-compatible code, unittest, Markdown, GitHub Actions.

**Spec:** docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md on docs/mediahub-chat-tree-map-20261012; GEMINI.md on main; Issue #301.

## Global Constraints

- Baseline 2.0 remains the canonical functional reference.
- Product State Authority remains the only canonical product-state mutation authority.
- Preserve historical IDs and accepted authority/capability boundaries.
- No direct merge, deployment, provider dispatch, secret access, or Contour A qualification claim.
- Do not alter unrelated worker publishing behavior in this pass.

## Review Focus

- Secret-assignment detector must match ordinary KEY=value and bearer: "..." patterns without literal-backslash false negatives.
- PEM private-key marker detection must remain active.
- Ordinary documentation must not trigger the detector.
- Tests must be discovered by python -m unittest discover -s tests -p 'test_*.py'.
- Agent instructions must distinguish source inspection, test execution, verification, qualification, deployment and acceptance.

---

### Task 1: Secret scanner regression

- Add tests/test_worker_security_gate.py using unittest.TestCase.
- Confirm the API-key and bearer-token tests fail on the existing implementation.
- Fix only the regex escaping in ops/qualification/run_distributed_local_worker.py.
- Run focused tests and the repository test command; report unrelated baseline failures separately.

### Task 2: Durable repository skill

- Add root AGENTS.md as a concise routing layer, preserving GEMINI.md and its current agent-specific rules.
- Add .agents/skills/mediahub-next/SKILL.md for live-ref checks, source-of-truth retrieval, bounded implementation, evidence, read-back, and reporting.
- Keep the skill advisory; it does not grant capabilities or bypass governance.

### Task 3: Verification and provenance

- Review exact diff and status.
- Run compile and full unittest discovery where environment permits.
- Verify the skill files and test are present and ensure no secrets are present in the diff.
- Record current base/head SHA and leave integration to a separately reviewed PR.
