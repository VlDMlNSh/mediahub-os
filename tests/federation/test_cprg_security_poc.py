from ops.federation.cprg_security_poc import run_all


REQUIRED_FIELDS = {
    "scenario",
    "pass",
    "request_id",
    "node_id",
    "operation",
    "destination",
    "lease_until",
    "active",
    "closed",
    "audit",
    "final_state",
}


def test_cprg_security_poc_all_scenarios_pass():
    evidence = run_all()
    assert evidence["schema"] == "mediahub.cprg-security-poc.v1"
    assert evidence["mode"] == "non-production-deterministic"
    assert evidence["pass"] is True
    assert len(evidence["scenarios"]) == 8
    assert all(item["pass"] for item in evidence["scenarios"])
    assert all(REQUIRED_FIELDS <= item.keys() for item in evidence["scenarios"])


def test_cprg_security_poc_is_byte_deterministic():
    assert run_all() == run_all()


def test_cprg_security_poc_never_leaves_denied_scenarios_active():
    evidence = run_all()
    for item in evidence["scenarios"]:
        if item["scenario"] != "S2_exact_registration_allowed":
            assert item["active"] is False
            assert item["closed"] is True
            assert item["final_state"] == "CLOSED"


def test_cprg_security_poc_only_allows_exact_registration_scope():
    evidence = run_all()
    allowed = next(item for item in evidence["scenarios"] if item["scenario"] == "S2_exact_registration_allowed")
    assert allowed["operation"] == "api_key_registration"
    assert allowed["destination"] == "provider-registration"
    assert allowed["active"] is False
    assert allowed["closed"] is True
    assert [x["state"] for x in allowed["audit"]][-1] == "CLOSED"
