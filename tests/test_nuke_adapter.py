import os
import unittest
from unittest.mock import patch

from kairo_nuke.nuke_adapter import _snapshot_node, require_nuke
from kairo_nuke.shotdoctor import ScriptProfile


class _Knob:
    def __init__(self, value):
        self._value = value

    def value(self):
        return self._value


class _Node:
    def __init__(self):
        self.knobs = {
            "file": _Knob("renders/comp.####.exr"),
            "first": _Knob(1001),
            "last": _Knob(1010),
            "disable": _Knob(False),
        }

    def fullName(self): return "Group1.Write1"
    def Class(self): return "Write"
    def knob(self, name): return self.knobs.get(name)
    def input(self, index): return object()


class NukeAdapterTests(unittest.TestCase):
    def test_snapshot_uses_real_knob_shape_and_fallbacks(self):
        snapshot = _snapshot_node(_Node(), ScriptProfile(1001, 1010))
        self.assertEqual(snapshot.name, "Group1.Write1")
        self.assertEqual(snapshot.colorspace, "")
        self.assertTrue(snapshot.connected)

    def test_host_operation_fails_explicitly_without_nuke(self):
        with self.assertRaisesRegex(RuntimeError, "require Nuke"):
            require_nuke()
