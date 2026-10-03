import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from ops.mesh.artifacts import verify_artifact, validate_artifact_manifest, admit_verified_artifact

class ArtifactEdgeTests(unittest.TestCase):
    def test_hash_mismatch_never_admitted(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"x"; p.write_bytes(b"good")
            vr=verify_artifact(p,"0"*64)
            self.assertFalse(vr.verified)
    def test_malformed_manifest_rejected(self):
        self.assertFalse(validate_artifact_manifest({"schema_version":"mediahub.mesh.artifact.v1"}))
    def test_size_mismatch_never_admitted(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"x"; p.write_bytes(b"good")
            import hashlib
            h=hashlib.sha256(b"good").hexdigest()
            vr=verify_artifact(p,h)
            m={"schema_version":"mediahub.mesh.artifact.v1","artifact_id":"x","sha256":h,"size":99,"type":"test","origin":"unit","transport":["cid"],"replicas":[],"verification_state":"VERIFIED"}
            self.assertFalse(admit_verified_artifact(m,vr))

if __name__=="__main__": unittest.main()
