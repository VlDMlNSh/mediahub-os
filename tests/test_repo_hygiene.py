"""Repository-hygiene regression gate.

The whole-project audit found defects that no test caught: a workflow with
invalid YAML (heredoc bodies at column 0), a malformed recovery YAML, and
Python that did not compile on the sandbox interpreter. This gate makes those
classes of defect impossible to merge silently.

Deliberately dependency-light: only stdlib plus PyYAML (declared in
requirements-dev.txt).
"""
import json
import os
import unittest
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "build", "dist", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def _iter_files(suffixes):
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(suffixes):
                yield Path(root) / name


class RepoHygieneTests(unittest.TestCase):
    def test_every_python_file_compiles(self):
        failures = []
        for path in _iter_files((".py",)):
            source = path.read_text(encoding="utf-8")
            try:
                compile(source, str(path), "exec")
            except SyntaxError as exc:
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
        self.assertEqual(failures, [], "Python files that fail to compile:\n" + "\n".join(failures))

    def test_every_yaml_file_parses(self):
        failures = []
        for path in _iter_files((".yml", ".yaml")):
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001 - report every parser failure
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
        self.assertEqual(failures, [], "YAML files that fail to parse:\n" + "\n".join(failures))

    def test_every_json_file_parses(self):
        failures = []
        for path in _iter_files((".json",)):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
        self.assertEqual(failures, [], "JSON files that fail to parse:\n" + "\n".join(failures))

    def test_every_workflow_is_named_and_has_jobs(self):
        failures = []
        for path in sorted((ROOT / ".github" / "workflows").glob("*.y*ml")):
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                failures.append(f"{path.name}: not a mapping")
                continue
            if not document.get("name"):
                failures.append(f"{path.name}: missing top-level name")
            if not document.get("jobs"):
                failures.append(f"{path.name}: missing jobs")
        self.assertEqual(failures, [], "Invalid workflow definitions:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
