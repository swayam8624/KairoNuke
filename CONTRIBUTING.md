# Contributing

Keep changes focused and run:

```bash
PYTHONPATH=../KairoPipelineCore/src:python \
  python3 -m unittest discover -s tests -v
python3 -m compileall -q python init.py menu.py tests
```

Changes to `nuke_adapter.py`, `init.py`, or `menu.py` require a native smoke
inside Nuke. Include the Nuke version and license tier in the pull request.
