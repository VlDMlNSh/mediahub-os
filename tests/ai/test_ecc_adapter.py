import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "oss/adapters/ecc/README.md"


class ECCAdapterContractTests(unittest.TestCase):
    def setUp(self):
        self.text = ADAPTER.read_text(encoding="utf-8")

    def test_adapter_is_documentation_only_and_target_gated(self):
        self.assertIn("target-gated", self.text)
        self.assertIn("documentation-only", self.text)
        self.assertIn("not an ECC runtime", self.text)

    def test_mediahub_owns_authority(self):
        self.assertIn("MediaHub remains authoritative", self.text)
        self.assertIn("no direct State Authority mutation", self.text)
        self.assertIn("explicit, reviewable MediaHub-controlled GitHub change", self.text)

    def test_execution_boundaries_fail_closed(self):
        for needle in (
            "no credentials, API keys, tokens, or private keys",
            "no hidden persistence",
            "no hidden network egress",
            "no unbounded subprocesses",
            "no bypass of authorization, security, qualification, or release gates",
            "fail-closed behavior",
        ):
            self.assertIn(needle, self.text)

    def test_ecc_activation_is_not_implied(self):
        self.assertIn("hooks and command shims are not enabled by default", self.text)
        self.assertIn("Arbitrary upstream source import is prohibited", self.text)
        self.assertIn("production use are separate qualification-gated decisions", self.text)


if __name__ == "__main__":
    unittest.main()
