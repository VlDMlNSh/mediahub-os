import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class G4GoldRunnerAdmissionContractTests(unittest.TestCase):
    def test_g4_admission_uses_registered_control_runner(self):
        doc = yaml.safe_load((ROOT / '.github/workflows/astra-g4-115-qualification.yml').read_text())
        self.assertEqual(doc['jobs']['admission']['runs-on'], ['self-hosted', 'linux', 'x64', 'mediahub-control'])

    def test_gold_admission_uses_registered_control_runner(self):
        doc = yaml.safe_load((ROOT / '.github/workflows/astra-gold-unified-qualification.yml').read_text())
        self.assertEqual(doc['jobs']['g4-admission']['runs-on'], ['self-hosted', 'linux', 'x64', 'mediahub-control'])

    def test_gold_finds_g4_evidence_by_exact_sha_across_dispatch_refs(self):
        text = (ROOT / '.github/workflows/astra-gold-unified-qualification.yml').read_text()
        self.assertIn('actions/workflows/astra-g4-115-qualification.yml/runs?per_page=100', text)
        self.assertIn('select(.head_sha == env.GITHUB_SHA and .status == "completed" and .conclusion == "success")', text)
        self.assertNotIn('runs?branch=main&per_page=', text)


if __name__ == '__main__':
    unittest.main()
