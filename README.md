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


## Source learning pathway

Follow [the linked reading order](docs/SOURCE_READING_ORDER.md) to trace module ownership, public interfaces, implementation, tests and cross-repository interaction. This path is designed for learners who want to understand both the algorithms and the API boundaries rather than just execute a sample.

## Open-source learning and extension

Original contributions may be learned from, modified and further developed under the applicable [LICENSE](LICENSE). Preserve required notices; external libraries, application-host SDKs, source adaptations, datasets and media retain their own terms. Check [STATUS.md](STATUS.md) and native-host evidence before treating a feature as verified.
