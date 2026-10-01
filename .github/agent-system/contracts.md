# Agent Contracts

Every worker receives:
- task_id
- role
- mission
- context
- boundary
- owned_paths
- exclusive_actions
- dependencies
- constraints
- acceptance_criteria
- verification_criteria
- rollback_plan

Every worker returns:
- result
- changes
- tests
- risks
- open_questions
- verification_status
- evidence_refs

Lifecycle:
CREATED -> ASSIGNED -> ACTIVE -> READY_FOR_VERIFY -> VERIFIED -> INTEGRATED -> CLOSED

ACTIVE may enter BLOCKED and return to ACTIVE.
Verification failure may return to ACTIVE after bounded re-plan or become REJECTED.
Failure classes: timeout, blocked, dependency_failed, verification_failed, scope_exceeded, collision, environment_failure.
