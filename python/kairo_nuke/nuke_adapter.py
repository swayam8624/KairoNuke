"""Guarded adapter between Nuke's Python API and ShotDoctor snapshots."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from kairo_pipeline.diagnostics import DiagnosticBag

from .shotdoctor import NodeSnapshot, ScriptProfile, validate_script

try:
    import nuke as _nuke  # type: ignore[import-not-found]
except ImportError:
    _nuke = None


def require_nuke() -> Any:
    if _nuke is None:
        raise RuntimeError("KairoNuke host operations require Nuke's Python runtime")
    return _nuke


def inspect_script(project_root: Path | None = None) -> DiagnosticBag:
    """Capture the open script and run the shared deterministic rules."""

    nuke = require_nuke()
    root_node = nuke.root()
    root = _project_root(nuke, project_root)
    profile = ScriptProfile(
        project_first=int(root_node["first_frame"].value()),
        project_last=int(root_node["last_frame"].value()),
        allowed_read_colorspaces=_configured_colorspaces(),
    )
    nodes = tuple(
        _snapshot_node(node, profile)
        for node in nuke.allNodes(recurseGroups=True)
        if node.Class() in {"Read", "Write", "DeepWrite", "WriteGeo"}
    )
    return validate_script(root, nodes, profile)


def select_node(node_name: str) -> None:
    """Navigate to one node named by a diagnostic location."""

    nuke = require_nuke()
    node = nuke.toNode(node_name)
    if node is None:
        raise ValueError(f"Nuke node no longer exists: {node_name}")
    for current in nuke.selectedNodes():
        current.setSelected(False)
    node.setSelected(True)
    nuke.zoomToFitSelected()


def show_shotdoctor() -> None:
    """Run preflight and show a compact artist-facing report."""

    nuke = require_nuke()
    try:
        diagnostics = inspect_script()
    except Exception as error:
        nuke.message(f"<b>Kairo ShotDoctor could not run</b><br/>{error}")
        return
    items = tuple(diagnostics)
    if not items:
        nuke.message("<b>Kairo ShotDoctor</b><br/>No production issues found.")
        return
    rows = []
    for item in items:
        node = item.location.object_path if item.location else "script"
        rows.append(
            f"<b>{item.severity.value.upper()} · {item.code}</b> [{node}]<br/>"
            f"{item.message}<br/><i>{item.suggestion}</i>"
        )
    state = "BLOCKED" if diagnostics.blocks_publish else "REVIEW"
    nuke.message(f"<b>Kairo ShotDoctor · {state}</b><br/><br/>" + "<br/><br/>".join(rows))


def _project_root(nuke: Any, override: Path | None) -> Path:
    if override is not None:
        return Path(override).resolve(strict=True)
    configured = os.environ.get("KAIRO_PROJECT_ROOT", "").strip()
    if configured:
        return Path(configured).resolve(strict=True)
    script = Path(nuke.root().name())
    if script.name == "Root":
        raise RuntimeError("save the script or set KAIRO_PROJECT_ROOT")
    return script.resolve(strict=True).parent


def _snapshot_node(node: Any, profile: ScriptProfile) -> NodeSnapshot:
    return NodeSnapshot(
        name=node.fullName(),
        class_name=node.Class(),
        file_path=str(_knob_value(node, "file", "")),
        first=int(_knob_value(node, "first", profile.project_first)),
        last=int(_knob_value(node, "last", profile.project_last)),
        colorspace=str(_knob_value(node, "colorspace", "")),
        enabled=not bool(_knob_value(node, "disable", False)),
        connected=(node.input(0) is not None if node.Class() != "Read" else True),
    )


def _knob_value(node: Any, name: str, fallback: Any) -> Any:
    knob = node.knob(name)
    return fallback if knob is None else knob.value()


def _configured_colorspaces() -> tuple[str, ...]:
    raw = os.environ.get("KAIRO_NUKE_READ_COLORSPACES", "").strip()
    return tuple(value.strip() for value in raw.split(",") if value.strip())
