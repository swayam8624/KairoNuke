from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from kairo_nuke.shotdoctor import NodeSnapshot, ScriptProfile, validate_script


class ShotDoctorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "plates").mkdir()
        (self.root / "renders").mkdir()
        self.profile = ScriptProfile(1001, 1003, ("ACES - ACEScg",))

    def tearDown(self):
        self.temporary.cleanup()

    def codes(self, *nodes):
        return {item.code for item in validate_script(self.root, nodes, self.profile)}

    def test_complete_read_passes(self):
        for frame in range(1001, 1004):
            (self.root / "plates" / f"main.{frame:04d}.exr").write_bytes(b"exr")
        node = NodeSnapshot("Read1", "Read", "plates/main.####.exr", 1001, 1003,
                            "ACES - ACEScg")
        self.assertEqual(self.codes(node), set())

    def test_read_reports_missing_range_and_colorspace(self):
        (self.root / "plates" / "main.1001.exr").write_bytes(b"exr")
        node = NodeSnapshot("Read1", "Read", "plates/main.####.exr", 1001, 1003,
                            "default")
        self.assertEqual(self.codes(node), {"NUKE_READ_FRAMES_MISSING", "NUKE_READ_COLORSPACE"})

    def test_write_reports_range_connection_and_overwrite(self):
        (self.root / "renders" / "comp.1001.exr").write_bytes(b"old")
        node = NodeSnapshot("Write1", "Write", "renders/comp.####.exr", 1001, 1002,
                            connected=False)
        self.assertEqual(self.codes(node), {
            "NUKE_WRITE_RANGE_MISMATCH", "NUKE_WRITE_DISCONNECTED", "NUKE_WRITE_OVERWRITE"
        })

    def test_external_absolute_path_is_blocked(self):
        node = NodeSnapshot("Read1", "Read", "/tmp/main.####.exr", 1001, 1003,
                            "ACES - ACEScg")
        self.assertEqual(self.codes(node), {"NUKE_PATH_OUTSIDE_PROJECT"})

    def test_invalid_pattern_is_blocked(self):
        node = NodeSnapshot("Write1", "Write", "renders/final.exr", 1001, 1003)
        self.assertEqual(self.codes(node), {"NUKE_SEQUENCE_PATTERN_INVALID"})
