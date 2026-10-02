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


def test_privacy_data_boundary_poc_never_records_exposure_on_a_denied_attempt():
    """A blocked attempt is an attempt, not an exposure.

    ``raw_personal_data_exposed`` is a post-decision fact. The workflow gate
    asserts it is False for every scenario, which is only meaningful if the
    DENY path does not set it. The pre-decision condition is reported
    separately as ``raw_personal_data_would_cross`` so the blocked attempt
    stays visible in the evidence.
    """
    by_name = {item["scenario"]: item for item in run_all()["scenarios"]}

    denied = by_name["S2_raw_personal_data_crossing_denied"]
    assert denied["decision"] == "DENY"
    assert denied["raw_personal_data_would_cross"] is True
    assert denied["raw_personal_data_exposed"] is False

    assert all(
        item["raw_personal_data_exposed"] is False
        for item in run_all()["scenarios"]
    )


def test_privacy_data_boundary_poc_is_deterministic():
    assert run_all() == run_all()
