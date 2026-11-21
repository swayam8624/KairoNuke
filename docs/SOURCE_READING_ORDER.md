# Teaching source map — KairoNuke

Nuke compositing/render-output preflight tools.

Read these source links in order, identify the caller and callee for each public API, then check the error/ownership contract and its tests.

## Reading order

1. [`README.md`](README.md)
2. [`init.py`](init.py)
3. [`menu.py`](menu.py)
4. [`pyproject.toml`](pyproject.toml)
5. [`python`](python)
6. [`tests`](tests)
7. [`docs`](docs)

## Repository integration and API contracts

Nuke startup hooks expose tools; validation inspects Read/Write paths and provenance, and KairoPipelineCore verifies published data. Preserve Nuke-native license and host boundaries.

## Teaching standards

- Comments explain invariants, decision reasons, lifetime, prerequisites and cross-file effects; they do not narrate obvious statements.
- Follow upstream interfaces before implementation details; distinguish implemented, host-verified and planned features.
- Run available tests at a pinned commit and consult [STATUS.md](STATUS.md) / [STATUS.yaml](STATUS.yaml) before declaring completion.
- Reuse original contributions under [LICENSE](LICENSE), subject to third-party code and asset terms.
