# TEACHING MAP — menu.py
# Nuke UI menu creation and operator binding. User actions call nuke_adapter and ShotDoctor
# APIs; menus should not silently modify the current Nuke script on import.
# See READING_ORDER.md for API connections and Nuke host boundaries.

"""Nuke menu registration for Kairo ShotDoctor."""

import nuke

from kairo_nuke.nuke_adapter import show_shotdoctor

_menu = nuke.menu("Nuke").addMenu("Kairo")
_menu.addCommand("Run ShotDoctor", show_shotdoctor, "ctrl+shift+k")
