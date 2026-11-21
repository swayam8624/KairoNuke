# KairoNuke — teaching source reading order

Start with the [README](../README.md), then follow this **workflow-oriented** path. These repositories integrate with [KairoPipelineCore](https://github.com/swayam8624/KairoPipelineCore), the host-neutral Python contracts. The order below describes how a user action reaches validated, publishable data—not the import/build order.

1. [init.py](../init.py) — read API inputs, output contracts, errors and downstream caller.
2. [menu.py](../menu.py) — read API inputs, output contracts, errors and downstream caller.
3. [python/kairo_nuke/__init__.py](../python/kairo_nuke/__init__.py) — read API inputs, output contracts, errors and downstream caller.
4. [python/kairo_nuke/nuke_adapter.py](../python/kairo_nuke/nuke_adapter.py) — read API inputs, output contracts, errors and downstream caller.
5. [python/kairo_nuke/shotdoctor.py](../python/kairo_nuke/shotdoctor.py) — read API inputs, output contracts, errors and downstream caller.
6. [python/kairo_nuke/publish_ingest.py](../python/kairo_nuke/publish_ingest.py) — read API inputs, output contracts, errors and downstream caller.
7. [tests/test_shotdoctor.py](../tests/test_shotdoctor.py) — read API inputs, output contracts, errors and downstream caller.
8. [tests/test_nuke_adapter.py](../tests/test_nuke_adapter.py) — read API inputs, output contracts, errors and downstream caller.
9. [tests/test_publish_ingest.py](../tests/test_publish_ingest.py) — read API inputs, output contracts, errors and downstream caller.

## Data flow

Nuke menu/host adapter → recursive Read/Write node snapshots and per-shot profile → host-neutral ShotDoctor validation using portable paths and SequenceScan → diagnostics linked to Nuke node names → (separate) ingest of Houdini/render publish manifest with hash verification. No frames should be rewritten by inspection.

## Boundary of the tests

Host-neutral tests use snapshots; native Nuke script nodes, menus, group traversal, and licensed integration require separate verification. A validated external manifest is not itself a successful render.

## Teaching exercises

1. Trace one host action or command into a pure validation function and its structured diagnostic.
2. Identify where filesystem paths are normalized and hashed before publishing.
3. Feed malformed/missing files to the host-neutral path and locate the specific failure/diagnostic.
4. Run the portable tests; then read the native verification checklist before claiming host support.
5. Explain why a dry-run plan, a completed atomic publish, and a native host import are three different events.

## Licensing

Preserve the repository's existing [LICENSE](../LICENSE). The original source and documentation permit learning and development according to that file; external DCC SDKs, plugins, images and example assets retain their own terms.
