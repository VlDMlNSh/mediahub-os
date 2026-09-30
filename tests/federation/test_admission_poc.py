from ops.federation.federation_admission_poc import run_all


REQUIRED_SCENARIO_FIELDS = {
    "scenario",
    "pass",
    "job_id",
    "source_cluster",
    "destination_domain",
    "workload_class",
    "admission_decision",
    "state_transitions",
    "payload_bytes",
    "result_bytes",
    "capability_scope",
    "lease_until",
    "lease_active",
    "execution_result",
    "failure_retry",
    "final_authorization_state",
    "evidence_timestamp",
}


def test_federation_admission_poc_all_scenarios_pass():
    evidence = run_all()
    assert evidence["schema"] == "mediahub.federation-admission-poc.v2"
    assert evidence["mode"] == "non-production-deterministic"
    assert evidence["pass"] is True
    assert len(evidence["scenarios"]) == 8
    assert all(item["pass"] for item in evidence["scenarios"])
    assert all(REQUIRED_SCENARIO_FIELDS <= item.keys() for item in evidence["scenarios"])


def test_federation_admission_poc_is_byte_deterministic():
    assert run_all() == run_all()


def test_federation_admission_poc_has_expected_state_boundaries():
    evidence = run_all()
    by_id = {item["job_id"]: item for item in evidence["scenarios"]}
    assert [x["state"] for x in by_id["s3"]["state_transitions"]] == [
        "ADMITTED", "RUNNING", "RESULT_READY", "CLOSED"
    ]
    assert [x["state"] for x in by_id["s5"]["state_transitions"]][-3:] == [
        "LEASE_EXPIRED", "TERMINATED", "CLOSED"
    ]
    assert [x["state"] for x in by_id["s7"]["state_transitions"]] == [
        "ADMITTED", "DENIED", "CLOSED"
    ]
    assert by_id["s7"]["final_authorization_state"] == "CLOSED"
    assert by_id["s8"]["admission_decision"] == "DENY"
