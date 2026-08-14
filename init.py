"""Nuke startup path for Kairo ShotDoctor."""

from pathlib import Path
import sys

_PYTHON = str(Path(__file__).resolve().parent / "python")
if _PYTHON not in sys.path:
    sys.path.insert(0, _PYTHON)
