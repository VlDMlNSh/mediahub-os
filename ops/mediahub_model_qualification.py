"""Bounded local-model qualification; failures never activate a model."""
from __future__ import annotations
import hashlib, json, os, subprocess, tempfile, time, urllib.request
from pathlib import Path
from typing import Any
from ops.mediahub_model_registry import ModelRecord
MARKER = "MEDIAHUB_MODEL_QUALIFIED_OK"

def _post(url: str, body: dict[str, Any], timeout: float = 180.0) -> tuple[dict[str, Any], float]:
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}, method="POST")
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=timeout) as response:  # nosec B310 - localhost qualification endpoint
        return json.loads(response.read().decode()), (time.monotonic() - started) * 1000

def _chat(url: str, model: str, content: str, *, max_tokens: int) -> tuple[dict[str, Any], float]:
    return _post(url, {"model": model, "messages": [{"role": "user", "content": content}], "stream": False,
                  "options": {"temperature": 0, "num_predict": max_tokens, "seed": 7}})

def qualify_ollama(model: str, *, url: str = "http://127.0.0.1:11434/api/chat") -> dict[str, Any]:
    with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=5) as response:  # nosec B310 - localhost only
        tags = json.loads(response.read().decode())
    models = {row["name"]: row for row in tags.get("models", [])}
    if model not in models:
        return {"status": "NOT_QUALIFIED", "reason": "model-not-loaded"}
    started = time.monotonic()
    marker_payload, marker_ms = _chat(url, model, f"Return exactly {MARKER}", max_tokens=8)
    health_ms = (time.monotonic() - started) * 1000
    marker_text = marker_payload.get("message", {}).get("content", "").strip()
    digest = models[model].get("digest", "")
    if marker_text != MARKER:
        return {"status": "NOT_QUALIFIED", "reason": "marker-mismatch", "latency_ms": marker_ms, "digest": digest}
    prompt = ("Produce only this unified diff. File qualification_target.py currently contains VALUE = 1. "
              "Change it to VALUE = 2. No prose and no code fences.")
    coding_payload, coding_ms = _chat(url, model, prompt, max_tokens=96)
    diff = coding_payload.get("message", {}).get("content", "").strip()
    coding_ok = "+++ b/qualification_target.py" in diff and "-VALUE = 1" in diff and "+VALUE = 2" in diff
    patch_ok = test_ok = False
    if coding_ok:
        with tempfile.TemporaryDirectory(prefix="mediahub-model-qualification-") as tmp:
            root = Path(tmp); target = root / "qualification_target.py"; target.write_text("VALUE = 1\n", encoding="utf-8")
            patch = root / "change.diff"; patch.write_text(diff + "\n", encoding="utf-8")
            applied = subprocess.run(["patch", "-p1", "--forward", str(patch)], cwd=root, text=True, capture_output=True, check=False)  # nosec B603
            patch_ok = applied.returncode == 0 and target.read_text(encoding="utf-8") == "VALUE = 2\n"
            if patch_ok:
                test = subprocess.run(["python3", "-m", "py_compile", str(target)], cwd=root, text=True, capture_output=True, check=False)  # nosec B603
                test_ok = test.returncode == 0
    qualified = coding_ok and patch_ok and test_ok
    record = ModelRecord(provider="ollama", model=model, digest=digest,
                         capabilities=("coding-small", "test-generation", "qualification"),
                         context=models[model].get("details", {}).get("context_length"),
                         qualification_status="QUALIFIED" if qualified else "NOT_QUALIFIED",
                         latency_ms=marker_ms + coding_ms, task_classes=("coding", "qualification"))
    return {"status": record.qualification_status, "marker": marker_text, "health_ms": health_ms,
            "marker_ms": marker_ms, "coding_ms": coding_ms, "digest": digest,
            "digest_sha256": hashlib.sha256(digest.encode()).hexdigest(), "coding_ok": coding_ok,
            "patch_ok": patch_ok, "test_ok": test_ok, "record": record}

def main() -> int:
    result = qualify_ollama(os.environ.get("MEDIAHUB_OLLAMA_MODEL", "qwen2.5-coder:1.5b"))
    serializable = dict(result)
    if isinstance(serializable.get("record"), ModelRecord): serializable["record"] = serializable["record"].__dict__
    print(json.dumps(serializable, sort_keys=True, default=str))
    return 0 if result.get("status") == "QUALIFIED" else 2

if __name__ == "__main__": raise SystemExit(main())
