# TEACHING MAP — python/kairo_nuke/__init__.py
# Package boundary for Nuke-compatible diagnostics and publication ingestion. Native Nuke
# nodes remain in the host adapter.
# See READING_ORDER.md for API connections and Nuke host boundaries.

"""Kairo Nuke ShotDoctor public API."""

from .shotdoctor import NodeSnapshot, ScriptProfile, validate_script
from .nuke_adapter import inspect_script, select_node, show_shotdoctor
from .publish_ingest import inspect_publish

__version__ = "0.1.0"

__all__ = [
    "NodeSnapshot",
    "ScriptProfile",
    "inspect_script",
    "inspect_publish",
    "select_node",
    "show_shotdoctor",
    "validate_script",
    "__version__",
]
