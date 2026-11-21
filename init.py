# TEACHING MAP — init.py
# Nuke plug-in search-path/bootstrap entry point. Actual menu registration happens in
# menu.py; publish/shot validation logic lives in portable Python modules.
# See READING_ORDER.md for API connections and Nuke host boundaries.

"""Nuke startup path for Kairo ShotDoctor."""

from pathlib import Path
import sys

_PYTHON = str(Path(__file__).resolve().parent / "python")
if _PYTHON not in sys.path:
    sys.path.insert(0, _PYTHON)
