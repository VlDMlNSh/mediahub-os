import ast
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "mediahub_runtime"
AUTHORITY_FILE = RUNTIME / "state_authority.py"
ALLOWED_CONSTRUCTOR_FILE = RUNTIME / "composition_root.py"
FORBIDDEN_AUTHORITY_STORAGE = {
    "_state", "_events", "_processed", "_generation", "_version",
    "_sequence", "_available", "_policy", "_token", "_observers",
}


class TestMH05SystemwideReachability(unittest.TestCase):
    def test_only_composition_root_constructs_state_authority(self):
        offenders = []
        for path in RUNTIME.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "StateAuthority":
                    if path != ALLOWED_CONSTRUCTOR_FILE:
                        offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_canonical_authority_storage_is_confined_to_authority_module(self):
        offenders = []
        for path in RUNTIME.rglob("*.py"):
            if path == AUTHORITY_FILE:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store) and node.attr in FORBIDDEN_AUTHORITY_STORAGE:
                    offenders.append(f"{path.relative_to(ROOT)}:{node.attr}")
        self.assertEqual(offenders, [])

    def test_restore_call_is_confined_to_authority_module(self):
        offenders = []
        for path in RUNTIME.rglob("*.py"):
            if path == AUTHORITY_FILE:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "restore":
                    offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_consumer_boundary_has_no_direct_private_authority_mutation(self):
        path = RUNTIME / "consumer_boundary.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assignments = {
            node.attr for node in ast.walk(tree)
            if isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store)
        }
        self.assertTrue(assignments.isdisjoint(FORBIDDEN_AUTHORITY_STORAGE))


if __name__ == "__main__":
    unittest.main()
