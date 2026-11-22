# TEACHING MODULE: This is a *consumer-side* trust boundary.
# It reads a KairoPipelineCore publish manifest, requires a supported
# cache/render kind, normalizes every path beneath the project root
# and rehashes declared output/dependency files. A producer-side
# "publish succeeded" message is not proof of unchanged consumer bytes.
#
# The result is typed diagnostic evidence for a Nuke ingest command;
# it does not create Nuke Read nodes, convert colorspaces or authorize
# redistribution of third-party source images.
"""Validate cross-DCC publish manifests before Nuke ingest."""

from __future__ import annotations

from pathlib import Path

from kairo_pipeline.diagnostics import (
    Diagnostic,
    DiagnosticBag,
    DiagnosticLocation,
    Severity,
)
from kairo_pipeline.fingerprint import fingerprint_file
from kairo_pipeline.manifest import PublishKind, PublishManifest, load_manifest
from kairo_pipeline.paths import resolve_project_path


# Load a strict manifest and revalidate every declared file on the
# *consumer's* filesystem. Catch missing/modified outputs before Nuke
# scripts use them; the native adapter decides how to surface errors.
def inspect_publish(project_root: Path, manifest_path: Path) -> tuple[PublishManifest, DiagnosticBag]:
    """Load a strict manifest and verify every declared output fingerprint."""

    root = Path(project_root).resolve(strict=True)
    manifest = load_manifest(manifest_path)
    bag = DiagnosticBag()
    location = DiagnosticLocation(host="nuke", resource=str(manifest_path))
    if manifest.kind not in {PublishKind.CACHE, PublishKind.RENDER}:
        bag.add(Diagnostic(
            code="NUKE_PUBLISH_KIND_UNSUPPORTED", severity=Severity.ERROR,
            message=f"Nuke ingest does not support {manifest.kind.value} publishes.",
            location=location, suggestion="Choose a cache or render publish manifest."
        ))
    for output in manifest.outputs:
        try:
            source = resolve_project_path(root, output.path)
            actual = fingerprint_file(source)
        except (FileNotFoundError, ValueError):
            bag.add(Diagnostic(
                code="NUKE_PUBLISH_OUTPUT_MISSING", severity=Severity.ERROR,
                message=f"Published output is unavailable: {output.path}",
                location=location, suggestion="Restore or republish the declared output."
            ))
            continue
        if actual != output.fingerprint:
            bag.add(Diagnostic(
                code="NUKE_PUBLISH_HASH_MISMATCH", severity=Severity.ERROR,
                message=f"Published output changed after publication: {output.path}",
                location=location, suggestion="Do not ingest it; create a new immutable version."
            ))
    return manifest, bag
