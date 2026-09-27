import json
from io import BytesIO

import ops.local_autonomous_agent as agent


class Response:
    status = 200

    def __init__(self, body):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, _size=-1):
        return self.body


class Opener:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.urls = []

    def open(self, request, timeout=0):
        self.urls.append(request.full_url)
        return next(self.responses)


def test_gemini_is_preferred_when_authorized(monkeypatch):
    body = {"candidates":[{"content":{"parts":[{"text":"diff --git a/a b/a"}]}}]}
    opener = Opener([Response(json.dumps(body).encode())])
    monkeypatch.setattr(agent, "LOCAL_AI_OPENER", opener)
    monkeypatch.setattr(agent, "GEMINI_API_KEY", "present")
    monkeypatch.setattr(agent, "OPENROUTER_API_KEY", "")
    rc, content, status = agent.generate("task")
    assert rc == 0
    assert content.startswith("diff --git")
    assert status == "GEMINI_AI_SUCCESS"
    assert opener.urls[0].endswith("/models/gemini-3.5-flash-lite:generateContent")


def test_openrouter_is_second_cloud_fallback(monkeypatch):
    import urllib.error
    opener = Opener([])
    def open_request(request, timeout=0):
        opener.urls.append(request.full_url)
        if "generativelanguage.googleapis.com" in request.full_url:
            raise urllib.error.HTTPError(request.full_url, 429, "rate", {}, BytesIO(b"{}"))
        return Response(b'{"choices":[{"message":{"content":"diff --git a/a b/a"}}]}')
    opener.open = open_request
    monkeypatch.setattr(agent, "LOCAL_AI_OPENER", opener)
    monkeypatch.setattr(agent, "GEMINI_API_KEY", "present")
    monkeypatch.setattr(agent, "OPENROUTER_API_KEY", "present")
    rc, content, status = agent.generate("task")
    assert rc == 0
    assert content.startswith("diff --git")
    assert status == "OPENROUTER_AI_SUCCESS"
    assert opener.urls[1] == "https://openrouter.ai/api/v1/chat/completions"
