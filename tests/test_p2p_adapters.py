import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from ops.p2p.torrent import publish_torrent, verify_download
from ops.p2p.ipfs import ipfs_available, TransportUnavailable, resolve_cid

class P2PAdapterTests(unittest.TestCase):
    def test_ipfs_probe_is_explicit(self):
        if not ipfs_available():
            with self.assertRaises(TransportUnavailable):
                resolve_cid("bafytest")
    def test_torrent_publish_and_verify(self):
        with TemporaryDirectory() as d:
            root=Path(d); artifact=root/"artifact"; artifact.write_bytes(b"MEDIAHUB-P2P-V1")
            torrent=root/"artifact.torrent"
            publish_torrent(artifact,torrent)
            self.assertTrue(torrent.is_file())
            import hashlib
            self.assertTrue(verify_download(artifact,hashlib.sha256(b"MEDIAHUB-P2P-V1").hexdigest()).verified)

if __name__=="__main__": unittest.main()
