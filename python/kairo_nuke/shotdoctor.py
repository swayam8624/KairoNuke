"""Host-neutral Nuke script validation rules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from kairo_pipeline.diagnostics import (
    Diagnostic,
    DiagnosticBag,
    DiagnosticLocation,
    Severity,
)
from kairo_pipeline.paths import normalize_project_path, resolve_project_path
from kairo_pipeline.sequences import FramePattern, scan_sequence


@dataclass(frozen=True, slots=True)
class NodeSnapshot:
    name: str
    class_name: str
    file_path: str = ""
    first: int = 1
    last: int = 1
    colorspace: str = ""
    enabled: bool = True
    connected: bool = True


@dataclass(frozen=True, slots=True)
class ScriptProfile:
    project_first: int
    project_last: int
    allowed_read_colorspaces: tuple[str, ...] = ()
    require_connected_writes: bool = True

    def __post_init__(self) -> None:
        if self.project_first > self.project_last:
            raise ValueError("project first frame must not exceed last frame")


def validate_script(
    project_root: Path,
    nodes: Iterable[NodeSnapshot],
    profile: ScriptProfile,
) -> DiagnosticBag:
    """Validate deterministic Read/Write snapshots against one shot profile."""

    root = Path(project_root).resolve(strict=True)
    bag = DiagnosticBag()
    for node in nodes:
        if node.class_name == "Read":
            _validate_read(root, node, profile, bag)
        elif node.class_name in {"Write", "DeepWrite", "WriteGeo"}:
            _validate_write(root, node, profile, bag)
    return bag


def _location(node: NodeSnapshot, property_name: str = "") -> DiagnosticLocation:
    return DiagnosticLocation(
        host="nuke", object_path=node.name, property_name=property_name
    )


def _add(
    bag: DiagnosticBag,
    node: NodeSnapshot,
    code: str,
    severity: Severity,
    message: str,
    suggestion: str,
    property_name: str = "",
) -> None:
    bag.add(
        Diagnostic(
            code=code,
            severity=severity,
            message=message,
            location=_location(node, property_name),
            suggestion=suggestion,
        )
    )


def _validate_read(
    root: Path, node: NodeSnapshot, profile: ScriptProfile, bag: DiagnosticBag
) -> None:
    if not node.file_path:
        _add(bag, node, "NUKE_READ_PATH_EMPTY", Severity.ERROR,
             "Read node has no source path.", "Choose a published plate.", "file")
        return
    pattern = _portable_pattern(root, node, bag)
    if pattern is None:
        return
    scan = scan_sequence(root, pattern, node.first, node.last)
    if scan.missing:
        ranges = _frame_ranges(scan.missing)
        _add(bag, node, "NUKE_READ_FRAMES_MISSING", Severity.ERROR,
             f"Read source is missing frames {ranges}.",
             "Restore or republish the listed frames.", "file")
    if node.first > profile.project_first or node.last < profile.project_last:
        _add(bag, node, "NUKE_READ_RANGE_SHORT", Severity.WARNING,
             "Read range does not cover the project frame range.",
             "Confirm handles or extend the Read range.", "first")
    if profile.allowed_read_colorspaces and node.colorspace not in profile.allowed_read_colorspaces:
        _add(bag, node, "NUKE_READ_COLORSPACE", Severity.ERROR,
             f"Read colorspace '{node.colorspace}' is not approved.",
             "Select a colorspace from the shot profile.", "colorspace")
    if not node.enabled:
        _add(bag, node, "NUKE_READ_DISABLED", Severity.INFO,
             "Read node is disabled.", "Enable it or remove it if obsolete.", "disable")


def _validate_write(
    root: Path, node: NodeSnapshot, profile: ScriptProfile, bag: DiagnosticBag
) -> None:
    if not node.file_path:
        _add(bag, node, "NUKE_WRITE_PATH_EMPTY", Severity.ERROR,
             "Write node has no output path.", "Choose a project-relative output.", "file")
        return
    pattern = _portable_pattern(root, node, bag)
    if pattern is None:
        return
    if node.first != profile.project_first or node.last != profile.project_last:
        _add(bag, node, "NUKE_WRITE_RANGE_MISMATCH", Severity.ERROR,
             "Write range does not match the project frame range.",
             "Use the shot profile range before rendering.", "first")
    if profile.require_connected_writes and not node.connected:
        _add(bag, node, "NUKE_WRITE_DISCONNECTED", Severity.ERROR,
             "Write node has no connected input.", "Connect the intended output branch.")
    if not node.enabled:
        _add(bag, node, "NUKE_WRITE_DISABLED", Severity.WARNING,
             "Write node is disabled.", "Enable it before submitting the render.", "disable")
    scan = scan_sequence(root, pattern, node.first, node.last)
    if scan.existing:
        _add(bag, node, "NUKE_WRITE_OVERWRITE", Severity.WARNING,
             f"Write would overwrite {len(scan.existing)} existing frame(s).",
             "Publish a new version or explicitly approve replacement.", "file")


def _portable_pattern(
    root: Path, node: NodeSnapshot, bag: DiagnosticBag
) -> FramePattern | None:
    raw = node.file_path.replace("\\", "/")
    if Path(raw).is_absolute():
        try:
            relative = Path(raw).resolve(strict=False).relative_to(root).as_posix()
        except ValueError:
            _add(bag, node, "NUKE_PATH_OUTSIDE_PROJECT", Severity.ERROR,
                 "Path resolves outside the project root.",
                 "Use a project-relative published path.", "file")
            return None
        _add(bag, node, "NUKE_PATH_MACHINE_SPECIFIC", Severity.WARNING,
             "Path is absolute and machine-specific.",
             f"Replace it with {relative} or a project token.", "file")
        raw = relative
    try:
        relative = normalize_project_path(raw)
        resolve_project_path(root, relative)
        return FramePattern.parse(relative)
    except (TypeError, ValueError):
        _add(bag, node, "NUKE_SEQUENCE_PATTERN_INVALID", Severity.ERROR,
             "Path must contain exactly one supported frame token.",
             "Use #### or %04d style frame notation.", "file")
        return None


def _frame_ranges(frames: tuple[int, ...]) -> str:
    groups: list[str] = []
    start = previous = frames[0]
    for frame in frames[1:]:
        if frame == previous + 1:
            previous = frame
            continue
        groups.append(str(start) if start == previous else f"{start}-{previous}")
        start = previous = frame
    groups.append(str(start) if start == previous else f"{start}-{previous}")
    return ", ".join(groups)
