# KairoNuke: linked source-reading order

Learn Nuke's plugin init/menu registration, then portable shot diagnostics and publication ingest, then host-native adapter and test suite. Nuke Read/Write nodes and publish bundle hashes are distinct contracts.

## APIs and boundaries

ShotDoctor checks source plates/output settings; publish_ingest verifies manifest and source fingerprints; nuke_adapter binds to Nuke node APIs. Do not claim a desktop-host connection merely because headless/fixture Python tests pass.

## Read these files (9)

1. [`init.py`](init.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
2. [`menu.py`](menu.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
3. [`python/kairo_nuke/shotdoctor.py`](python/kairo_nuke/shotdoctor.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
4. [`python/kairo_nuke/publish_ingest.py`](python/kairo_nuke/publish_ingest.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
5. [`python/kairo_nuke/nuke_adapter.py`](python/kairo_nuke/nuke_adapter.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
6. [`tests/test_shotdoctor.py`](tests/test_shotdoctor.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
7. [`tests/test_publish_ingest.py`](tests/test_publish_ingest.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
8. [`tests/test_nuke_adapter.py`](tests/test_nuke_adapter.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.
9. [`python/kairo_nuke/__init__.py`](python/kairo_nuke/__init__.py) — inspect the host API dependencies, validation, returned evidence and failure handling; compare its callers to corresponding tests.

## License and verification

This repository preserves its existing [LICENSE](LICENSE) for original work; external artist tools, SDKs, output media and third-party assets keep their own terms. Educational reuse and further development are encouraged within those licenses. Use [README](README.md) for actual host configuration. A source guide or passing pure-Python unit tests do not imply a successful native-host integration run.
