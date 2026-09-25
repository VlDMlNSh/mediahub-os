from urllib.error import HTTPError
from urllib.request import Request

from ops.local_autonomous_agent import LOCAL_AI_URL, NoRedirectHandler


def test_local_ai_endpoint_is_loopback_only() -> None:
    assert LOCAL_AI_URL == "http://127.0.0.1:8081/v1/chat/completions"


def test_local_ai_redirects_are_denied() -> None:
    handler = NoRedirectHandler()
    request = Request(LOCAL_AI_URL)
    try:
        handler.redirect_request(request, None, 302, "Found", {}, "http://example.invalid/")
    except HTTPError as exc:
        assert exc.code == 302
        assert "redirect denied" in str(exc.reason)
    else:
        raise AssertionError("redirect must be denied")


def test_omniroute_is_local_optional_transport() -> None:
    from ops.local_autonomous_agent import OMNIROUTE_URL
    assert OMNIROUTE_URL == "http://127.0.0.1:20128/v1/chat/completions"
