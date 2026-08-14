"""Nuke menu registration for Kairo ShotDoctor."""

import nuke

from kairo_nuke.nuke_adapter import show_shotdoctor

_menu = nuke.menu("Nuke").addMenu("Kairo")
_menu.addCommand("Run ShotDoctor", show_shotdoctor, "ctrl+shift+k")
