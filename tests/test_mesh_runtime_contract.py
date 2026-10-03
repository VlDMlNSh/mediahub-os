import unittest
from pathlib import Path

ROOT=Path(__file__).parents[1]

class RuntimeContractTests(unittest.TestCase):
    def test_service_is_non_authoritative(self):
        text=(ROOT/"ops/systemd/mediahub-mesh.service").read_text()
        self.assertIn("NoNewPrivileges=yes",text)
        self.assertIn("User=mediahub",text)
    def test_runtime_defaults_fail_closed(self):
        text=(ROOT/"ops/mesh/__main__.py").read_text()
        self.assertIn('MEDIAHUB_MESH_FAIL_CLOSED',text)
        self.assertIn('!= "1"',text)
    def test_node_check_exists(self):
        self.assertTrue((ROOT/"ops/node/mh-dev-02-mesh-check.sh").is_file())

if __name__=="__main__": unittest.main()
