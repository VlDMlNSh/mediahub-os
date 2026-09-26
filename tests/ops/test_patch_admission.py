import json
from pathlib import Path

import pytest

from ops.astra_patch_admission import PatchAdmissionError, StructuredPatch, admit_patch


def test_admit_patch_rejects_absolute_and_parent_paths(tmp_path):
    proposal = StructuredPatch.from_json(json.dumps({"files": [{"path": "/etc/passwd", "operation": "modify", "patch": ""}]}))
    with pytest.raises(PatchAdmissionError):
        admit_patch(proposal, tmp_path, allowed_paths=("tests/**",))


def test_admit_patch_rejects_forbidden_paths(tmp_path):
    proposal = StructuredPatch.from_json(json.dumps({"files": [{"path": "secrets/token.txt", "operation": "modify", "patch": ""}]}))
    with pytest.raises(PatchAdmissionError):
        admit_patch(proposal, tmp_path, allowed_paths=("**",), forbidden_paths=("secrets/**",))


def test_admit_patch_rejects_non_modify_operations(tmp_path):
    proposal = StructuredPatch.from_json(json.dumps({"files": [{"path": "tests/x.py", "operation": "delete", "patch": ""}]}))
    with pytest.raises(PatchAdmissionError):
        admit_patch(proposal, tmp_path, allowed_paths=("tests/**",))


def test_admit_patch_accepts_bounded_unified_diff(tmp_path):
    target = tmp_path / "tests" / "x.py"
    target.parent.mkdir(parents=True)
    target.write_text("VALUE = 1\n", encoding="utf-8")
    patch = """diff --git a/tests/x.py b/tests/x.py\n--- a/tests/x.py\n+++ b/tests/x.py\n@@ -1 +1 @@\n-VALUE = 1\n+VALUE = 2\n"""
    proposal = StructuredPatch.from_json(json.dumps({"files": [{"path": "tests/x.py", "operation": "modify", "patch": patch}]}))
    admitted = admit_patch(proposal, tmp_path, allowed_paths=("tests/**",))
    assert admitted.changed_files == ("tests/x.py",)
    assert target.read_text(encoding="utf-8") == "VALUE = 2\n"

def test_admission_limits_patch_size(tmp_path):
    proposal = StructuredPatch.from_json(json.dumps({"files": [{"path": "tests/x.py", "operation": "modify", "patch": ""}]}))
    pytest.raises(PatchAdmissionError, admit_patch, proposal, tmp_path, allowed_paths=("tests/**",), max_patch_bytes=1)
