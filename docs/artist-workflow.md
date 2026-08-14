# Artist workflow

1. Add this repository to `NUKE_PATH` and set `KAIRO_PROJECT_ROOT` to the shot
   root when the script is not stored there.
2. Optionally set `KAIRO_NUKE_READ_COLORSPACES` to a comma-separated show
   allowlist.
3. Open **Kairo > Run ShotDoctor** before render submission.
4. Resolve blocking Read/Write path, range, colorspace, connectivity, and
   missing-frame diagnostics.
5. Review overwrite warnings and publish a new render version where required.
6. Validate Houdini cache or render manifests before ingest. ShotDoctor checks
   strict schema, allowed publish kind, file presence, byte count, and SHA-256.

## Native release gate

- `init.py` adds the package path without duplicate entries;
- the Kairo menu appears once and its shortcut opens ShotDoctor;
- grouped Read/Write nodes are discovered;
- selecting a diagnostic navigates to the corresponding node;
- the report distinguishes blocking errors from review warnings.
