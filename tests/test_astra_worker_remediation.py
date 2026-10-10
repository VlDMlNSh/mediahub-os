from __future__ import annotations

import json
import subprocess
from pathlib import Path

from ops.qualification import run_distributed_local_worker as worker


def test_verifier_diff_includes_tracked_edits_and_untracked_files(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args: str) -> str:
        result = subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)
        return result.stdout.strip()

    git("init", "-q")
    git("config", "user.name", "Astra Regression")
    git("config", "user.email", "astra-regression@example.invalid")
    (repo / "tracked.txt").write_text("base" + chr(10), encoding="utf-8")
    git("add", "tracked.txt")
    git("commit", "-qm", "base")
    target_sha = git("rev-parse", "HEAD")
    (repo / "tracked.txt").write_text("base" + chr(10) + "changed" + chr(10), encoding="utf-8")
    (repo / "new artifact.txt").write_text("new file contents" + chr(10), encoding="utf-8")
    monkeypatch.setattr(worker, "ROOT", repo)
    diff = worker.verifier_diff(target_sha)
    assert "tracked.txt" in diff
    assert "new artifact.txt" in diff
    assert "+changed" in diff
    assert "+new file contents" in diff


def test_artifact_contract_requires_changed_file_exact_sha_and_terms(tmp_path: Path, monkeypatch):
    target_sha = "a" * 40
    path = "docs/operations/ASTRA-DISTRIBUTED-LOCAL-DEVELOPMENT-TOPOLOGY.md"
    artifact = tmp_path / path
    artifact.parent.mkdir(parents=True)
    required = [
        "mh-dev-01 as controller/authority", "mh-dev-02 as primary local pool",
        "Voktors-Mac-mini.local as fast pool", "G-5 = 3", "target-SHA binding",
        "isolated branches", "GitHub evidence transport", "fail-closed promotion",
        "no worker writes directly to main", "no credentials or secrets",
    ]
    contract = {"path": path, "target_sha_required": True, "required_terms": required,
                "forbidden_terms": ["Stopped for maintenance"]}
    task = {"boundary": [path], "artifact_contract": contract}
    artifact.write_text(chr(10).join(required + ["Stopped for maintenance"]) + chr(10), encoding="utf-8")
    monkeypatch.setattr(worker, "ROOT", tmp_path)
    findings = worker.artifact_contract_findings(task, target_sha, {path})
    assert "artifact_contract_target_sha_missing" in findings
    assert "artifact_contract_forbidden_term:Stopped for maintenance" in findings
    assert "artifact_contract_requires_changed_file" in worker.artifact_contract_findings(task, target_sha, set())
    artifact.write_text(chr(10).join(required + [target_sha]) + chr(10), encoding="utf-8")
    assert worker.artifact_contract_findings(task, target_sha, {path}) == []



def test_artifact_contract_rejects_invented_configuration_and_placeholders(tmp_path: Path, monkeypatch):
    artifact = tmp_path / "topology.md"
    artifact.write_text("Safe topology prose\n", encoding="utf-8")
    monkeypatch.setattr(worker, "ROOT", tmp_path)
    patterns = [
        r"(?im)^\s*(?:api[_ -]?token|access[_ -]?token|github[_ -]?token)\s*:",
        r"(?im)^\s*(?:ip|port|cpu|memory)\s*:",
        r"(?im)^\s*(?:LocalPoolAuthority|FastPoolAuthority|FailClosedPromotion|NoDirectMainWrites)\s*:",
        r"(?i)\b(?:fail-closed-promotion-url|your[_ -]?(?:api[_ -]?)?key|placeholder|changeme|example\.com)\b",
    ]
    task = {
        "boundary": ["topology.md"],
        "artifact_contract": {
            "path": "topology.md",
            "required_terms": [],
            "forbidden_terms": [],
            "forbidden_patterns": patterns,
        },
    }
    assert worker.artifact_contract_findings(task, "a" * 40, {"topology.md"}) == []
    for bad_line in (
        "api_token: [REDACTED]",
        "port: 5002",
        "FailClosedPromotion: http://fail-closed-promotion-url",
        "Use placeholder values",
    ):
        artifact.write_text("Safe topology prose\n" + bad_line + "\n", encoding="utf-8")
        assert any(
            finding.startswith("artifact_contract_forbidden_pattern:")
            for finding in worker.artifact_contract_findings(task, "a" * 40, {"topology.md"})
        ), bad_line


def test_document_fallback_prompt_forbids_unsupported_operational_details():
    source = Path(worker.__file__).read_text(encoding="utf-8")
    assert "unsupported runtime claims" in source
    assert "Do not add URLs, configuration examples, credentials, placeholders" in source


def test_marked_document_fallback_extracts_only_the_exact_envelope():
    output = (
        "model preamble that must not be materialized\n"
        "ASTRA_ARTIFACT_BEGIN\n"
        "# mh-dev-02 executor\n"
        "target-SHA binding and fail-closed promotion; no direct writes to main.\n"
        "ASTRA_ARTIFACT_END\n"
        "model trailing text that must not be materialized\n"
    )
    assert worker.extract_marked_artifact(output) == (
        "# mh-dev-02 executor\n"
        "target-SHA binding and fail-closed promotion; no direct writes to main."
    )


def test_marked_document_fallback_rejects_missing_or_empty_envelopes():
    assert worker.extract_marked_artifact("plain text without markers") is None
    assert worker.extract_marked_artifact("ASTRA_ARTIFACT_BEGIN\n\nASTRA_ARTIFACT_END") is None


def test_claude_output_budget_is_applied_and_document_fallback_avoids_json_schema():
    source = Path(worker.__file__).read_text(encoding="utf-8")
    assert 'env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(max(1, min(int(max_tokens), 4096)))' in source
    assert "artifact_schema = {" not in source
    assert "max_tokens=1024," in source
    assert "WRITE THE DOCUMENT NOW." in source
    assert 'builder_timeout = min(max(60, int(task.get("timeout_seconds", 1800))), 1200)' in source
    assert 'builder_attempts = max(1, min(int(task.get("builder_attempts", 2)), 2))' in source
    assert 'max_turns=3,' in source
    assert "Reproduce the following Markdown template exactly" in source
    assert "[complete Markdown document]" not in source
    assert "system_prompt: str | None = None" in source
    assert 'command.extend(["--system-prompt", system_prompt, "--no-session-persistence"])' in source
    assert "strict literal document-template renderer" in source
    assert "f\"- Model: {cfg['model']}\\n\"" in source
    assert "f\"- Verifier: {task['verifier']}\\n\"" in source
    assert "extract_marked_artifact(output)" in source
    assert "exec_claude(prompt, model, 720, env_file, 128, max_turns=2)" in source


def test_verifier_requires_one_exact_pass_verdict():
    assert worker.verifier_passed("ASTRA_VERDICT: PASS" + chr(10))
    assert not worker.verifier_passed("The prior run said ASTRA_VERDICT: PASS" + chr(10))
    assert not worker.verifier_passed("ASTRA_VERDICT: PASS (probably)" + chr(10))
    assert not worker.verifier_passed("ASTRA_VERDICT: PASS" + chr(10) + "ASTRA_VERDICT: BLOCKED" + chr(10))


def test_security_gate_detects_common_secret_assignments(tmp_path: Path, monkeypatch):
    sample = tmp_path / "config.py"
    sample.write_text("api" + "_key = " + chr(34) + ("abc" * 8) + chr(34) + chr(10), encoding="utf-8")
    monkeypatch.setattr(worker, "ROOT", tmp_path)
    assert "possible_secret:config.py" in worker.security_gate({"config.py"}, {})
    sample.write_text("Authorization = " + chr(34) + "Bearer " + ("abc" * 12) + chr(34) + chr(10), encoding="utf-8")
    assert "possible_secret:config.py" in worker.security_gate({"config.py"}, {})


def test_canonical_queue_task_disallows_no_change_pass_and_requires_sha_contract():
    task = json.loads(Path("ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text(encoding="utf-8"))
    assert task["status"] == "READY"
    assert task["allow_no_changes"] is False
    assert task["artifact_contract"]["target_sha_required"] is True
    assert task["artifact_contract"]["path"] == task["deliverable"]


def test_document_fallback_prompt_is_pinned_to_target_sha():
    source = Path(worker.__file__).read_text(encoding="utf-8")
    assert 'f"\\n## Target SHA\\n{target_sha}\\n"' in source
    assert 'artifact_contract_target_sha_missing' in source




def test_publication_workflow_uses_available_self_hosted_runner():
    workflow = Path(".github/workflows/astra-node-result-publication.yml").read_text(encoding="utf-8")
    assert "runs-on: [self-hosted, Linux, X64, mediahub-control]" in workflow
    assert "runs-on: ubuntu-latest" not in workflow
    assert "workflow_run" in workflow

def test_topology_document_records_verified_controller_worker_runner_contention():
    document = Path("docs/operations/ASTRA-DISTRIBUTED-LOCAL-DEVELOPMENT-TOPOLOGY.md").read_text(encoding="utf-8")
    assert "Observed runner-capacity blocker" in document
    assert "38034436196" in document
    assert "38034576170" in document
    assert "not three currently available concurrent runner slots" in document
    assert "Increasing remote wait time alone cannot resolve this self-dispatch dependency" in document

def test_queue_002_document_satisfies_its_literal_artifact_contract():
    task = json.loads(Path("ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text(encoding="utf-8"))
    contract = task["artifact_contract"]
    document = Path(contract["path"]).read_text(encoding="utf-8").casefold()
    assert all(term.casefold() in document for term in contract["required_terms"])
    assert all(term.casefold() not in document for term in contract["forbidden_terms"])
    target_sha = "3e3c4daa62095d3049c8dcf121a614250ec5ebfc"
    assert target_sha in document


def test_raw_markdown_fallback_requires_sha_and_all_contract_terms():
    target_sha = "a" * 40
    terms = ["mh-dev-01 as controller/authority", "fail-closed promotion"]
    raw = (
        "Astra Operations Contract\n"
        "mh-dev-01 as controller/authority\n"
        "fail-closed promotion\n"
        f"Target SHA: {target_sha}\n"
    )
    artifact = worker.extract_validated_artifact(raw, target_sha, terms)
    assert artifact is not None
    assert artifact.startswith("# Astra Operations Contract")
    assert target_sha in artifact
    assert worker.extract_validated_artifact(raw.replace(target_sha, "b" * 40), target_sha, terms) is None
    assert worker.extract_validated_artifact(raw, target_sha, terms + ["missing phrase"]) is None


def test_raw_markdown_fallback_rejects_forbidden_terms_urls_and_bad_markers():
    target_sha = "c" * 40
    terms = ["required topology term"]
    raw = f"Topology\nrequired topology term\nTarget SHA: {target_sha}"
    assert worker.extract_validated_artifact(raw, target_sha, terms, ["Topology"]) is None
    assert worker.extract_validated_artifact(raw + "\nhttps://example.invalid", target_sha, terms) is None
    assert worker.extract_validated_artifact("ASTRA_ARTIFACT_BEGIN\n" + raw, target_sha, terms) is None
