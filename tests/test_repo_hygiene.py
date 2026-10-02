"""Repository-hygiene regression gate.

The whole-project audit found defects that no test caught: a workflow with
invalid YAML (heredoc bodies at column 0), a malformed recovery YAML, Python
that did not compile on the sandbox interpreter, and dispatch-only "phantom"
workflows that reference runtime modules and tests that do not exist in this
repository (defect D1).

This gate makes those classes of defect impossible to merge silently. The
phantom-workflow guard is non-destructive: those workflows are planned
verification procedures for architecture stages that are not implemented yet,
so they are kept but pinned as explicitly dormant rather than deleted (the
build-or-remove decision belongs to A1/Human — see
docs/qualification/ASTRA-GOLD-PROJECT-AUDIT-2026-10-02.md).

Deliberately dependency-light: only stdlib plus PyYAML (declared in
requirements-dev.txt).
"""
import json
import os
import re
import unittest
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "build", "dist", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
WORKFLOW_DIR = ROOT / ".github" / "workflows"

# Dispatch-only verification procedures whose dependencies (P0-07/P0-08
# subsystems and their tests) are not implemented in this repository yet. They
# cannot run in CI. They are kept pending an A1/Human build-or-remove decision,
# so this register must be updated deliberately when that changes.
DORMANT_WORKFLOWS = {
    "mediahub-p0-07-verification.yml",
    "mediahub-p0-08-verification.yml",
    "mediahub-bridge.yml",
    "mediahub-live-provider-qualification.yml",
}

AUTO_TRIGGERS = {"push", "pull_request", "pull_request_target"}

# Deterministic source references (not runtime output paths such as
# control/results/... that are produced on other branches).
SOURCE_REFERENCE = re.compile(
    r"(?:tests|runtime/mediahub_runtime)/[A-Za-z0-9_./-]+\.py"
)


def _iter_files(suffixes):
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith(suffixes):
                yield Path(root) / name


def _trigger(document):
    if not isinstance(document, dict):
        return None
    # PyYAML resolves the bare ``on:`` key to boolean True.
    return document.get("on", document.get(True))


def _is_auto_running(trigger):
    if trigger is None:
        return False
    if trigger is True:
        # A bare ``on:`` defaults to push.
        return True
    if isinstance(trigger, str):
        return trigger in AUTO_TRIGGERS
    if isinstance(trigger, list):
        return any(_is_auto_running(item) for item in trigger)
    if isinstance(trigger, dict):
        return any(key in AUTO_TRIGGERS for key in trigger)
    return False


def _missing_source_references(text):
    return sorted(
        {match for match in SOURCE_REFERENCE.findall(text) if not (ROOT / match).exists()}
    )


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
        for path in sorted(WORKFLOW_DIR.glob("*.y*ml")):
            document = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                failures.append(f"{path.name}: not a mapping")
                continue
            if not document.get("name"):
                failures.append(f"{path.name}: missing top-level name")
            if not document.get("jobs"):
                failures.append(f"{path.name}: missing jobs")
        self.assertEqual(failures, [], "Invalid workflow definitions:\n" + "\n".join(failures))

    def test_auto_running_workflows_reference_existing_sources(self):
        """An auto-running workflow must not reference a source file that is absent.

        A missing reference in a push/pull_request workflow is a guaranteed CI
        failure; a missing reference in a dispatch-only workflow is the tracked
        D1 deferral handled by the dormant-workflow tests below.
        """
        failures = []
        for path in sorted(WORKFLOW_DIR.glob("*.y*ml")):
            text = path.read_text(encoding="utf-8")
            document = yaml.safe_load(text)
            if not _is_auto_running(_trigger(document)):
                continue
            for reference in _missing_source_references(text):
                failures.append(f"{path.name}: auto-run references missing {reference}")
        self.assertEqual(failures, [], "Auto-running workflows with missing sources:\n" + "\n".join(failures))

    def test_dormant_workflows_are_registered_and_dispatch_only(self):
        """Every workflow with missing sources must be a registered dormant one.

        This is what turns D1 from a silent phantom reference into a tracked,
        guarded deferral: adding a new broken auto- or manual workflow fails here.
        """
        failures = []
        for path in sorted(WORKFLOW_DIR.glob("*.y*ml")):
            text = path.read_text(encoding="utf-8")
            if not _missing_source_references(text):
                continue
            if path.name not in DORMANT_WORKFLOWS:
                failures.append(
                    f"{path.name}: references missing sources but is not in the dormant register"
                )
                continue
            document = yaml.safe_load(text)
            if _is_auto_running(_trigger(document)):
                failures.append(
                    f"{path.name}: registered as dormant but runs automatically"
                )
        self.assertEqual(failures, [], "Untracked or auto-running phantom workflows:\n" + "\n".join(failures))

    def test_registered_dormant_workflows_still_exist(self):
        failures = []
        for name in sorted(DORMANT_WORKFLOWS):
            if not (WORKFLOW_DIR / name).is_file():
                failures.append(f"{name}: registered dormant workflow is missing")
        self.assertEqual(failures, [], "Registered dormant workflows that no longer exist:\n" + "\n".join(failures))

    def test_dormant_workflows_are_still_actually_blocked(self):
        """Fails when a dormant stage is implemented, forcing the register to be revisited.

        If P0-07/P0-08 (or the bridge/live-provider tests) are built, their
        workflow no longer has missing sources and must be reconciled here.
        """
        failures = []
        for name in sorted(DORMANT_WORKFLOWS):
            path = WORKFLOW_DIR / name
            if not path.is_file():
                continue
            if not _missing_source_references(path.read_text(encoding="utf-8")):
                failures.append(
                    f"{name}: no longer blocked; remove it from the dormant register and wire it up"
                )
        self.assertEqual(failures, [], "Dormant workflows that appear implemented:\n" + "\n".join(failures))


class TestDiscoveryHygieneTests(unittest.TestCase):
    """Guards the test suite itself against silent loss of coverage.

    Two defects found while landing the qualification contracts are covered
    here:

    1. A test directory without ``__init__.py`` is skipped entirely by
       ``python -m unittest discover -s tests``, which is the command CI runs.
       ``tests/qualification/`` and ``tests/federation/`` were both invisible
       to CI that way, so 25 unittest-style tests never executed.
    2. A test module importing a sibling test module that does not exist
       fails only when something actually collects that directory. In CI
       nothing did, so a broken import shipped green.
    """

    TESTS_DIR = ROOT / "tests"

    def _test_subdirectories(self):
        for path in sorted(self.TESTS_DIR.iterdir()):
            if not path.is_dir() or path.name.startswith("."):
                continue
            if path.name in SKIP_DIRS:
                continue
            yield path

    def test_every_test_subdirectory_is_a_package(self):
        """A missing __init__.py makes unittest discover skip the whole directory."""
        missing = [
            f"tests/{p.name}/__init__.py"
            for p in self._test_subdirectories()
            if not (p / "__init__.py").is_file()
        ]
        self.assertEqual(
            missing,
            [],
            "Test directories without __init__.py are silently skipped by "
            "'python -m unittest discover -s tests' in CI:\n" + "\n".join(missing),
        )

    def test_test_modules_import_only_existing_modules(self):
        """Guards against a test importing a sibling test module that was removed."""
        failures = []
        pattern = re.compile(r"^\s*from\s+(tests[\w.]*)\s+import\s", re.MULTILINE)
        for path in sorted(self.TESTS_DIR.rglob("test_*.py")):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            for module in set(pattern.findall(path.read_text(encoding="utf-8"))):
                rel = Path(*module.split("."))
                if (self.TESTS_DIR.parent / rel).with_suffix(".py").is_file():
                    continue
                if (self.TESTS_DIR.parent / rel / "__init__.py").is_file():
                    continue
                failures.append(
                    f"{path.relative_to(ROOT)}: imports missing module '{module}'"
                )
        self.assertEqual(failures, [], "Broken test imports:\n" + "\n".join(failures))


if __name__ == "__main__":
    unittest.main()
