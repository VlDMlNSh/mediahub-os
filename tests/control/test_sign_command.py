import hashlib, hmac, json, os, tempfile, time, unittest, importlib.util
from pathlib import Path
SPEC=importlib.util.spec_from_file_location("sign_command",Path(__file__).parents[1]/"control"/"sign_command.py")
MODULE=importlib.util.module_from_spec(SPEC); assert SPEC.loader is not None; SPEC.loader.exec_module(MODULE)

class CommandSignerTests(unittest.TestCase):
    def command(self):
        return {"schema_version":1,"command_id":"cmd-001","node_id":"mh-dev-01","operation":"health","target_sha":"bbc8475c43b2aeabc86906ebf31bb4a7afa2959a","workflow_only":True,"owned_paths":["control/commands/mh-dev-01.json"],"title":"health","description":"bounded health check","exclusive_actions":["execute"],"issued_at":int(time.time())}
    def test_signature_uses_hmac_sha256(self):
        command=self.command(); signed=MODULE.sign_command(command,"test-secret")
        expected=hmac.new(b"test-secret",MODULE.canonical_command_body(command),hashlib.sha256).hexdigest()
        self.assertEqual(signed["signature"],expected)
    def test_tampering_changes_signature(self):
        signed=MODULE.sign_command(self.command(),"test-secret"); tampered=dict(signed); tampered["operation"]="autonomous_gold_mission"
        expected=hmac.new(b"test-secret",MODULE.canonical_command_body(tampered),hashlib.sha256).hexdigest()
        self.assertNotEqual(signed["signature"],expected)
    def test_missing_required_field_fails_closed(self):
        command=self.command(); del command["node_id"]
        with self.assertRaises(ValueError): MODULE.sign_command(command,"test-secret")
    def test_stale_command_fails_closed(self):
        command=self.command(); command["issued_at"]-=MODULE.MAX_AGE_SECONDS+1
        with self.assertRaises(ValueError): MODULE.sign_command(command,"test-secret")
    def test_file_signer_adds_fresh_issued_at_without_exposing_secret(self):
        command=self.command(); command.pop("issued_at")
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"command.json"; path.write_text(json.dumps(command),encoding="utf-8")
            old=os.environ.get("ASTRA_COMMAND_HMAC_KEY"); os.environ["ASTRA_COMMAND_HMAC_KEY"]="test-secret"
            try: MODULE.sign_file(path)
            finally:
                if old is None: os.environ.pop("ASTRA_COMMAND_HMAC_KEY",None)
                else: os.environ["ASTRA_COMMAND_HMAC_KEY"]=old
            content=path.read_text(encoding="utf-8"); signed=json.loads(content)
            self.assertIn("issued_at",signed); self.assertIn("signature",signed); self.assertNotIn("test-secret",content)

if __name__=="__main__": unittest.main()
