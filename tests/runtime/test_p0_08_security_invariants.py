"""Static guard tests for P0-08 plugin extension runtime.

The guard scans executable Python imports/calls and selected AST names rather
than searching contract documentation strings for forbidden words.
"""

import ast
from pathlib import Path


ROOT = Path(__file__).parents[2]
P0_08_FILES = (
    ROOT / "runtime/mediahub_runtime/plugin_manifest.py",
    ROOT / "runtime/mediahub_runtime/plugin_capabilities.py",
    ROOT / "runtime/mediahub_runtime/plugin_boundary.py",
    ROOT / "runtime/mediahub_runtime/plugin_authorization.py",
    ROOT / "runtime/mediahub_runtime/plugin_lifecycle.py",
    ROOT / "runtime/mediahub_runtime/plugin_resources.py",
    ROOT / "runtime/mediahub_runtime/plugin_proposals.py",
)


def _tree():
    return [ast.parse(path.read_text(encoding="utf-8"), filename=str(path)) for path in P0_08_FILES]


def test_p0_08_has_no_forbidden_runtime_imports_or_calls():
    forbidden_modules = {"subprocess", "socket", "requests", "sqlite3", "http", "urllib", "os", "shutil"}
    forbidden_calls = {"system", "popen", "exec", "eval", "compile", "open"}
    for tree in _tree():
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert not any(alias.name.split(".")[0] in forbidden_modules for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                assert (node.module or "").split(".")[0] not in forbidden_modules
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in forbidden_calls
                elif isinstance(node.func, ast.Attribute):
                    assert node.func.attr not in forbidden_calls


def test_p0_08_contains_no_authority_or_persistence_bindings():
    forbidden_names = {
        "StateAuthority",
        "CanonicalStore",
        "PersistenceHandle",
        "MutableState",
        "Transaction",
        "Checkpoint",
    }
    for tree in _tree():
        names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
        assert not names.intersection(forbidden_names)
