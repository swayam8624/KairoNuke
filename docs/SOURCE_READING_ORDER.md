# Teaching source map — KairoNuke

Nuke compositing/render-output preflight tools.

Read these source links in order, identify the caller and callee for each public API, then check the error/ownership contract and its tests.

## Reading order

1. [`README.md`](../README.md)
2. [`init.py`](../init.py)
3. [`menu.py`](../menu.py)
4. [`pyproject.toml`](../pyproject.toml)
5. [`python`](../python)
6. [`tests`](../tests)
7. [`docs`](../docs)

## Repository integration and API contracts

Nuke startup hooks expose tools; validation inspects Read/Write paths and provenance, and KairoPipelineCore verifies published data. Preserve Nuke-native license and host boundaries.

## Teaching standards

- Comments explain invariants, decision reasons, lifetime, prerequisites and cross-file effects; they do not narrate obvious statements.
- Follow upstream interfaces before implementation details; distinguish implemented, host-verified and planned features.
- Run available tests at a pinned commit and consult [STATUS.md](../STATUS.md) / [STATUS.yaml](../STATUS.yaml) before declaring completion.
- Reuse original contributions under [LICENSE](../LICENSE), subject to third-party code and asset terms.


## Complete source-file inventory

After the curated teaching path, follow this deterministic inventory of first-party source, scripts, shaders, and tests. Grouping is a suggested learning order, not an indication that every function is already annotated. Vendored dependencies, ROMs, binaries, data, media, and generated evidence are excluded.

### Implementation and other source (6)

1. [`init.py`](../init.py)
2. [`menu.py`](../menu.py)
3. [`python/kairo_nuke/__init__.py`](../python/kairo_nuke/__init__.py)
4. [`python/kairo_nuke/nuke_adapter.py`](../python/kairo_nuke/nuke_adapter.py)
5. [`python/kairo_nuke/publish_ingest.py`](../python/kairo_nuke/publish_ingest.py)
6. [`python/kairo_nuke/shotdoctor.py`](../python/kairo_nuke/shotdoctor.py)

### Verification and tests (3)

1. [`tests/test_nuke_adapter.py`](../tests/test_nuke_adapter.py)
2. [`tests/test_publish_ingest.py`](../tests/test_publish_ingest.py)
3. [`tests/test_shotdoctor.py`](../tests/test_shotdoctor.py)

Snapshot totals: 9 first-party source/build/test files, 21 tracked files overall. Re-audit when files are renamed or added.
