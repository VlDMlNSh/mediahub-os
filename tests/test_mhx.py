import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "mhx.py"

def run(tmp, *args, check=True):
    p = subprocess.run([sys.executable, str(CLI), *args], cwd=tmp, text=True, capture_output=True)
    if check:
        assert p.returncode == 0, p.stderr
    return p

def test_execution_loop_and_exact_cache(tmp_path):
    run(tmp_path, "init")
    (tmp_path / "sample.txt").write_text("a\nb\nc\n", encoding="utf-8")
    run(tmp_path, "manifest", ".")
    run(tmp_path, "index")
    run(tmp_path, "chunk", "--lines", "2")
    chunks = json.loads((tmp_path / ".mhx/master/chunk-index.json").read_text())
    assert len(chunks["chunks"]) == 2
    run(tmp_path, "task", "TASK-1", "inspect sample", "--task-class", "T1")
    task = json.loads((tmp_path / ".mhx/tasks/pending/TASK-1.json").read_text())
    run(tmp_path, "task", "claim", "TASK-1", "W-LOCAL")
    raw = tmp_path / "result.json"
    raw.write_text(json.dumps({"task_id":"TASK-1","worker_id":"W-LOCAL","input_revision":"R0","status":"OBSERVED","findings":["ok"]}), encoding="utf-8")
    run(tmp_path, "result", "normalize", str(raw), "RESULT-1")
    result_path = tmp_path / ".mhx/results/normalized/RESULT-1.json"
    run(tmp_path, "cache-store", task["task_hash"], str(result_path))
    p = run(tmp_path, "cache", task["task_hash"])
    assert '"EXACT"' in p.stdout
    run(tmp_path, "review", "RESULT-1", "ACCEPT")
    run(tmp_path, "revision")
    run(tmp_path, "integrate", "RESULT-1")
    state = json.loads((tmp_path / ".mhx/master/state.json").read_text())
    assert state["revision"] == "R1"

def test_governance_firewall(tmp_path):
    run(tmp_path, "init")
    p = run(tmp_path, "task", "TASK-G", "change validation", "--governance", check=False)
    assert p.returncode != 0
    assert "TASK_BLOCKED_GOVERNANCE" in p.stdout
    assert (tmp_path / ".mhx/tasks/failed/TASK-G.json").exists()
    assert not list((tmp_path / ".mhx/tasks/pending").glob("*.json"))

def test_hash_mismatch_rolls_back(tmp_path):
    run(tmp_path, "init")
    target = tmp_path / "sample.txt"
    target.write_text("old\n", encoding="utf-8")
    run(tmp_path, "task", "TASK-2", "change file")
    run(tmp_path, "task", "claim", "TASK-2", "W-CODEX")
    raw = tmp_path / "result.json"
    raw.write_text(json.dumps({"task_id":"TASK-2","worker_id":"W-CODEX","input_revision":"R0","status":"FOUND","changed_artifacts":[{"path":"sample.txt","content":"new\n","content_hash":"0"*64}]}), encoding="utf-8")
    run(tmp_path, "result", "normalize", str(raw), "RESULT-2")
    run(tmp_path, "review", "RESULT-2", "ACCEPT")
    p = run(tmp_path, "integrate", "RESULT-2", check=False)
    assert p.returncode != 0
    assert target.read_text(encoding="utf-8") == "old\n"
