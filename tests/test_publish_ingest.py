from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from kairo_nuke.publish_ingest import inspect_publish
from kairo_pipeline.fingerprint import fingerprint_file
from kairo_pipeline.manifest import (
    PublishFile, PublishKind, PublishManifest, serialize_manifest,
)


class PublishIngestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "scene.nk").write_bytes(b"script")
        (self.root / "cache").mkdir()
        self.output = self.root / "cache" / "smoke.1001.vdb"
        self.output.write_bytes(b"vdb")
        self.manifest = PublishManifest(
            kind=PublishKind.CACHE, project="Demo", name="smoke", version=1,
            source_host="houdini", source_path="scene.nk",
            source_fingerprint=fingerprint_file(self.root / "scene.nk"),
            outputs=(PublishFile("cache/smoke.1001.vdb", "cache-frame",
                                 fingerprint_file(self.output)),),
        )
        self.path = self.root / "manifest.json"
        self.path.write_bytes(serialize_manifest(self.manifest))

    def tearDown(self):
        self.temporary.cleanup()

    def test_valid_cross_dcc_publish_passes(self):
        loaded, diagnostics = inspect_publish(self.root, self.path)
        self.assertEqual(loaded.source_host, "houdini")
        self.assertFalse(diagnostics.blocks_publish)

    def test_mutated_publish_is_blocked(self):
        self.output.write_bytes(b"changed")
        _, diagnostics = inspect_publish(self.root, self.path)
        self.assertEqual({item.code for item in diagnostics},
                         {"NUKE_PUBLISH_HASH_MISMATCH"})

    def test_missing_publish_is_blocked(self):
        self.output.unlink()
        _, diagnostics = inspect_publish(self.root, self.path)
        self.assertEqual({item.code for item in diagnostics},
                         {"NUKE_PUBLISH_OUTPUT_MISSING"})
