import pytest

from ops.mediahub_egress_controller import EgressController, EgressDenied, EgressPolicy


def test_egress_is_fail_closed():
    controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
    with pytest.raises(EgressDenied):
        controller.admit("https://api.example.com")


def test_allowlisted_destination_is_admitted():
    controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
    controller.authorize()
    controller.admit("https://api.example.com")


def test_unknown_destination_and_http_are_denied():
    controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
    controller.authorize()
    for destination in ("https://other.example.com", "http://api.example.com"):
        with pytest.raises(EgressDenied):
            controller.admit(destination)


def test_policy_destination_cannot_contain_credentials_or_url_data():
    for destination in (
        "https://user:pass@example.com",
        "https://example.com/?token=secret",
        "https://example.com/#fragment",
    ):
        controller = EgressController(EgressPolicy(frozenset({destination})))
        with pytest.raises(EgressDenied):
            controller.authorize()


def test_policy_size_is_bounded():
    destinations = frozenset(f"https://{i}.example.com" for i in range(17))
    controller = EgressController(EgressPolicy(destinations))
    with pytest.raises(EgressDenied):
        controller.authorize()


def test_revocation_is_terminal():
    controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
    controller.revoke()
    with pytest.raises(EgressDenied):
        controller.authorize()
