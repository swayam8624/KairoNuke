# SOURCE STUDY NOTE:
# Public Nuke Python package exports for host adapter, ShotDoctor rules and published-manifest ingest.
# Read docs/SOURCE_READING_ORDER.md for Nuke → snapshots → diagnostics.

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
