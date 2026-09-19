# MH-07 — Validation Model

Status: CANDIDATE.

Validation layers are separate: syntax → schema → semantic → policy → authorization → runtime compatibility.

Syntax validates representation. Schema validates fields/types/bounds. Semantic validation checks domain meaning. Policy evaluates declared rules. Authorization checks the principal's concrete capability. Runtime validation checks safe applicability.

Failure at any required layer means NO APPLY. Validation is deterministic, bounded and side-effect free. Candidates and reads are immutable.

Existing implementation evidence covers bounded structure, immutable nested values, finite numbers and secret-key rejection. Complete semantic/runtime validation is not yet evidenced.
