from ops.federation.federation_admission_poc import run_all


def test_federation_admission_poc_all_scenarios_pass():
    evidence = run_all()
    assert evidence["schema"] == "mediahub.federation-admission-poc.v1"
    assert evidence["mode"] == "non-production-deterministic"
    assert evidence["pass"] is True
    assert len(evidence["scenarios"]) == 8
    assert all(item["pass"] for item in evidence["scenarios"])
