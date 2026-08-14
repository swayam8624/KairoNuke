# Kairo Nuke ShotDoctor

ShotDoctor is an artist-facing Nuke preflight tool for Read/Write nodes. It
finds missing plates, unsafe machine-specific paths, range mismatches,
disconnected nodes, colorspace omissions, and accidental output overwrites.

The validation engine is host-neutral and tested without Nuke. The adapter
uses the real `nuke` module when loaded in a licensed host; native verification
is a separate release gate and is never inferred from mocks.

```bash
PYTHONPATH=../KairoPipelineCore/src:python \
  python3 -m unittest discover -s tests -v
```

## Production behavior

- recursively inspects Read, Write, DeepWrite, and WriteGeo nodes;
- scans actual on-disk frame sequences and compresses missing-frame ranges;
- keeps all navigation locations tied to real Nuke node names and knobs;
- validates Houdini cache and render manifests before cross-DCC ingest;
- never deletes frames or silently overwrites an existing version.

See [the artist workflow](docs/artist-workflow.md) for setup and the native
release checklist.
