import pathlib
import tempfile
import unittest
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("mhx_host", ROOT / "tools/mhx_host.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class MHXHostSecurityTests(unittest.TestCase):
    def test_sensitive_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / ".env").write_text("TOKEN=do-not-package", encoding="utf-8")
            violations = MODULE.validate_source(root)
            self.assertTrue(any(v["path"] == ".env" for v in violations))

    def test_private_key_name_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "id_ed25519").write_text("private-key-placeholder", encoding="utf-8")
            violations = MODULE.validate_source(root)
            self.assertTrue(any(v["reason"] == "sensitive_path" for v in violations))

    def test_normal_source_has_no_violation(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "README.md").write_text("MediaHub OS", encoding="utf-8")
            self.assertEqual(MODULE.validate_source(root), [])

if __name__ == "__main__":
    unittest.main()
