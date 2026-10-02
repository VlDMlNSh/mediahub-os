import json
import tempfile
import unittest
from pathlib import Path

from ops.qualification.verify_g4_115 import verify as verify_g4
from ops.qualification.verify_integrated_a3 import REQUIRED

ROOT = Path(__file__).parents[1]
CONTRACT = json.loads((ROOT / "control/qualification/g4-115.json").read_text(encoding="utf-8"))


class TestAstraGoldEvidenceContracts(unittest.TestCase):
    def test_g4_contract_is_115_rounds(self):
        self.assertEqual(CONTRACT["total_rounds"], 115)
        self.assertEqual(CONTRACT["rounds_per_path"], 23)
        self.assertEqual(len(CONTRACT["mandatory_paths"]), 5)

    def test_g4_verifier_blocks_missing_rounds(self):
        result = verify_g4({"schema": "mediahub.astra-gold.g4-115-evidence.v1", "status": "PASS", "source_sha": "sha"}, CONTRACT, "sha")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(result["blocked_reasons"])

    def test_a3_requires_g4_g5_g6(self):
        self.assertEqual(set(REQUIRED), {"G4", "G5", "G6"})


if __name__ == "__main__":
    unittest.main()
