# SOURCE STUDY NOTE:
# Nuke UI menu actions for ShotDoctor; nuke_adapter reads native nodes while shotdoctor.py performs
# host-independent validation.
# Read docs/SOURCE_READING_ORDER.md for Nuke → snapshots → diagnostics.

"""Nuke menu registration for Kairo ShotDoctor."""

import nuke

from kairo_nuke.nuke_adapter import show_shotdoctor

_menu = nuke.menu("Nuke").addMenu("Kairo")
_menu.addCommand("Run ShotDoctor", show_shotdoctor, "ctrl+shift+k")
