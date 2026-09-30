from ops.federation.privacy_data_boundary_poc import run_all


def test_privacy_data_boundary_poc_all_scenarios_pass():
    evidence = run_all()
    assert evidence["schema"] == "mediahub.privacy-data-boundary-poc.v1"
    assert evidence["mode"] == "non-production-deterministic"
    assert evidence["pass"] is True
    assert len(evidence["scenarios"]) == 4
    assert all(item["pass"] for item in evidence["scenarios"])


def test_privacy_data_boundary_poc_enforces_developer_privacy():
    by_name = {item["scenario"]: item for item in run_all()["scenarios"]}
    assert by_name["S1_developer_workload_without_personal_data"]["decision"] == "ALLOW"
    assert by_name["S1_developer_workload_without_personal_data"]["personal_data_requested"] is False
    assert by_name["S2_raw_personal_data_crossing_denied"]["reason"] == "raw_personal_data_would_cross_boundary"
    assert by_name["S3_developer_personnel_access_denied"]["reason"] == "developer_personnel_access_forbidden"
    assert by_name["S4_local_personal_data_retained"]["reason"] == "developer_execution_not_admitted"


def test_privacy_data_boundary_poc_is_deterministic():
    assert run_all() == run_all()
