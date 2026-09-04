# MH-21 External Compute Contract

Status: PROPOSED.

An ExternalWorkload is a bounded computation request, never an authority grant.

Required fields: workload_id, requester_identity, workload_type, purpose, destination, provider_id, model_id, model_version, data_classification, data_scope, capability_scope, timeout, resource_budget, cost_budget, privacy_constraints, security_constraints, retention, response_limits, provenance, correlation_id, audit_context, cancellation and failure semantics.

Lifecycle: REQUESTED → CLASSIFIED → POLICY_EVALUATED → AUTHORIZED → PLACED → DISPATCHED → RUNNING → COMPLETED | FAILED | TIMEOUT | CANCELLED | REJECTED.

COMPLETED means computation completed; it does not authorize mutation. Every result is untrusted DATA until local validation/provenance/policy/authorization succeeds.
