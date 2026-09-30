from ops.federation.cluster_trust_poc import run_all


def test_cluster_trust_poc_all_scenarios_pass():
    evidence = run_all()
    assert evidence["schema"] == "mediahub.cluster-trust-poc.v1"
    assert evidence["mode"] == "non-production-deterministic"
    assert evidence["pass"] is True
    assert len(evidence["scenarios"]) == 4
    assert all(item["pass"] for item in evidence["scenarios"])


def test_cluster_trust_poc_enforces_identity_and_capability_boundaries():
    by_name = {item["scenario"]: item for item in run_all()["scenarios"]}
    assert by_name["S1_trusted_identity"]["decision"] == "ALLOW"
    assert by_name["S2_untrusted_anchor_denial"]["decision"] == "DENY"
    assert by_name["S3_identity_integrity_denial"]["reason"] == "source_identity_integrity_failure"
    assert by_name["S4_unadvertised_capability_denial"]["reason"] == "source_capability_not_advertised"


def test_cluster_trust_poc_is_deterministic():
    assert run_all() == run_all()
