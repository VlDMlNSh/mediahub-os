from ops.federation.compute_contribution_poc import run_all


def test_compute_contribution_poc_all_scenarios_pass():
    evidence = run_all()
    assert evidence["schema"] == "mediahub.compute-contribution-poc.v1"
    assert evidence["mode"] == "non-production-deterministic"
    assert evidence["pass"] is True
    assert len(evidence["scenarios"]) == 4
    assert all(item["pass"] for item in evidence["scenarios"])


def test_compute_contribution_poc_enforces_resource_and_workload_boundaries():
    by_name = {item["scenario"]: item for item in run_all()["scenarios"]}
    assert by_name["S1_bounded_developer_compute_admission"]["decision"] == "ALLOW"
    assert by_name["S2_user_workload_separation"]["reason"] == "non_developer_workload"
    assert by_name["S3_lease_bound_enforcement"]["reason"] == "lease_exceeds_capability_limit"
    assert by_name["S4_capability_integrity_denial"]["reason"] == "capability_integrity_failure"


def test_compute_contribution_poc_is_deterministic():
    assert run_all() == run_all()
