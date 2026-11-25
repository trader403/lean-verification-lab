import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from verify_manifest import verify_manifest


class VerifyManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "a.txt").write_bytes(b"alpha")
        self.manifest = self.root / "MANIFEST.sha256.json"

    def tearDown(self):
        self.tmp.cleanup()

    def write_manifest(self, entries):
        import hashlib
        data = {
            "schema_version": "1.0.0",
            "algorithm": "sha256",
            "scope": ".",
            "self_exclusion": "MANIFEST.sha256.json",
            "files": entries,
        }
        self.manifest.write_text(json.dumps(data), encoding="utf-8")

    def entry(self, path="a.txt", payload=b"alpha"):
        import hashlib
        return {"path": path, "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload)}

    def test_valid_manifest(self):
        self.write_manifest([self.entry()])
        result = verify_manifest(self.root, self.manifest)
        self.assertTrue(result["ok"])
        self.assertEqual(result["checked_files"], 1)

    def test_detects_modified_file(self):
        self.write_manifest([self.entry()])
        (self.root / "a.txt").write_bytes(b"changed")
        result = verify_manifest(self.root, self.manifest)
        self.assertFalse(result["ok"])
        self.assertTrue(any("mismatch" in e for e in result["errors"]))

    def test_detects_missing_file(self):
        self.write_manifest([self.entry("missing.txt")])
        result = verify_manifest(self.root, self.manifest)
        self.assertFalse(result["ok"])

    def test_rejects_path_traversal(self):
        self.write_manifest([self.entry("../outside.txt")])
        result = verify_manifest(self.root, self.manifest)
        self.assertFalse(result["ok"])
        self.assertTrue(any("unsafe" in e for e in result["errors"]))

    def test_rejects_duplicate_paths(self):
        self.write_manifest([self.entry(), self.entry()])
        result = verify_manifest(self.root, self.manifest)
        self.assertFalse(result["ok"])
        self.assertTrue(any("duplicate" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
