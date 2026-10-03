import hashlib
import tempfile
import unittest
from pathlib import Path
from ops.mesh.inventory import capability_from_inventory, executable_identity_sha256
from ops.mesh.validators import validate_capability

class MeshInventoryAdapterTests(unittest.TestCase):
    def test_identity_is_sha256_of_executable_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tool"; path.write_bytes(b"mediahub-test-executable")
            self.assertEqual(executable_identity_sha256(path), hashlib.sha256(b"mediahub-test-executable").hexdigest())
    def test_missing_executable_is_rejected(self):
        with self.assertRaises(ValueError): executable_identity_sha256("/does/not/exist")
    def test_adapter_preserves_discovered_state_and_none_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tool"; path.write_bytes(b"tool-v1")
            c=capability_from_inventory({"executable":str(path),"version":"1.2.3","qualification_state":"DISCOVERED"},provider="test-provider",capability_id="test-provider")
            self.assertEqual(c["authority"],"NONE"); self.assertEqual(c["qualification_state"],"DISCOVERED"); self.assertTrue(validate_capability(c).valid)
    def test_adapter_does_not_promote_without_explicit_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tool"; path.write_bytes(b"tool-v1")
            c=capability_from_inventory({"executable":str(path),"version":"1.2.3"},provider="test-provider",capability_id="test-provider")
            self.assertEqual(c["qualification_state"],"DISCOVERED")
    def test_explicit_qualification_state_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tool"; path.write_bytes(b"qualified-tool")
            c=capability_from_inventory({"executable":str(path),"version":"1.2.3","qualification_state":"QUALIFIED"},provider="test-provider",capability_id="test-provider")
            self.assertEqual(c["qualification_state"],"QUALIFIED")
    def test_authority_is_not_derived_from_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"tool"; path.write_bytes(b"tool")
            c=capability_from_inventory({"executable":str(path),"version":"1.0"},provider="control-looking-provider",capability_id="control-looking-provider")
            self.assertEqual(c["authority"],"NONE")
if __name__=="__main__": unittest.main()
