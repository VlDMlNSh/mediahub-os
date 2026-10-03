import json
import tempfile
import unittest
from pathlib import Path

from ops.mesh.inventory import capability_from_inventory


FIXTURE = Path(__file__).parent / "fixtures" / "mesh_capability_inventory.json"


class MeshCapabilityInventoryContractTests(unittest.TestCase):
    def test_required_auxiliary_capabilities_have_neutral_inventory_contracts(self):
        entries = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(
            {entry["provider"] for entry in entries},
            {"FreeLLMAPI", "OpenFlux", "ECC"},
        )

        with tempfile.TemporaryDirectory() as tmp:
            for entry in entries:
                executable = Path(tmp) / entry["executable"]
                executable.write_bytes((entry["provider"] + "\n").encode("utf-8"))
                component = {
                    "executable": str(executable),
                    "version": "fixture-1",
                    "qualification_state": entry["qualification_state"],
                }
                capability = capability_from_inventory(
                    component,
                    provider=entry["provider"],
                    capability_id=entry["capability_id"],
                    authority=entry["authority"],
                )
                self.assertEqual(capability["provider"], entry["provider"])
                self.assertEqual(capability["capability_id"], entry["capability_id"])
                self.assertEqual(capability["authority"], "NONE")
                self.assertEqual(capability["qualification_state"], "DISCOVERED")
                self.assertEqual(len(capability["identity_sha256"]), 64)

    def test_fixture_availability_keys_are_explicit_and_unique(self):
        entries = json.loads(FIXTURE.read_text(encoding="utf-8"))
        keys = [entry["availability_key"] for entry in entries]
        self.assertEqual(keys, ["freellmapi", "openflux", "ecc"])
        self.assertEqual(len(keys), len(set(keys)))


if __name__ == "__main__":
    unittest.main()
