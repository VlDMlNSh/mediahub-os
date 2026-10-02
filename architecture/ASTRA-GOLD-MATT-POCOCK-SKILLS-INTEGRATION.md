# ASTRA GOLD — Matt Pocock Skills Integration

Status: ADVISORY ENGINEERING INTEGRATION
Source: https://github.com/mattpocock/skills
Upstream author: Matt Pocock
Upstream license: MIT
Evaluation date: 2026-10-02

## Purpose

Matt Pocock's engineering skills are added as an external engineering-methodology reference for MediaHub / ASTRA qualification. They do not become an authority, transport, executor, credential manager, qualification gate, or source of truth.

ASTRA canonical architecture and qualification contracts remain authoritative.

## Selected skills relevant to ASTRA

| Skill | ASTRA use |
| --- | --- |
| `diagnosing-bugs` | Root-cause analysis for qualification/runtime failures before repair |
| `research` | Evidence-oriented investigation of external technical questions |
| `domain-modeling` | Clarifying MediaHub/Astra domain terminology and boundaries |
| `codebase-design` | Architecture/design review without changing canonical authority |
| `code-review` | Independent review of engineering changes |
| `tdd` | Test-first development for bounded fixes where appropriate |
| `to-spec` | Converting an agreed engineering objective into a traceable specification |
| `to-tickets` | Decomposing approved work into bounded GitHub issues |
| `wayfinder` | Decision mapping when a genuine architectural decision exists |
| `improve-codebase-architecture` | Periodic architecture-deepening review; recommendations only until explicitly accepted |
| `grill-with-docs` | Domain clarification when requirements are ambiguous; not a replacement for Human authority |
| `setup-matt-pocock-skills` | Repository setup only if explicitly adopted; it must not silently alter project governance |

## ASTRA boundary rules

1. Human remains final authority.
2. A0 remains MediaHub State Authority and coordination authority.
3. A1/A2/A3 boundaries remain unchanged.
4. Matt Pocock skills are methodology only.
5. They cannot promote a component, executor, provider, model, or node.
6. They cannot create credentials or expand access.
7. They cannot bypass G0-G11 gates.
8. They cannot declare PRE-SOAK, SOAK_24H, LAUNCH_READY, or ASTRA GOLD.
9. Their output is evidence/advice and must be reconciled against canonical ASTRA sources.
10. Installation or updates of external skill files are not themselves qualification evidence.

## Qualification workflow mapping

- DISCOVER / RESEARCH: `research`, `domain-modeling`
- DIAGNOSE: `diagnosing-bugs`
- DESIGN: `codebase-design`, `wayfinder`
- SPECIFICATION: `to-spec`
- IMPLEMENTATION: `tdd`, bounded implementation workflow
- REVIEW: `code-review`
- DECOMPOSITION: `to-tickets`
- RECONCILIATION: ASTRA canonical drift gate remains authoritative
- QUALIFICATION: ASTRA G0-G11 contract remains authoritative
- LAUNCH: Human-only

## Adoption model

The repository records the upstream reference rather than copying the upstream skill catalog into ASTRA's canonical architecture. This avoids creating a second governance layer and avoids treating a third-party methodology bundle as runtime qualification infrastructure.

For Codex/other agents, the upstream repository documents the universal `skills.sh` installation path. For Claude Code, the upstream project documents its managed plugin. Any installation on a runtime node requires a separate explicit component/access decision and is therefore outside this qualification pass.

## Evidence rule

A Matt Pocock skill may improve the method used to produce an engineering artifact, but the artifact is accepted by ASTRA only when the existing canonical evidence contract accepts it.

Reference:
- Upstream repository: https://github.com/mattpocock/skills
- Engineering skill index: https://github.com/mattpocock/skills/blob/main/skills/engineering/README.md
- Plugin metadata: https://github.com/mattpocock/skills/blob/main/.claude-plugin/plugin.json
