#!/usr/bin/env python3
"""Single source of truth for the CLI version string.

Canonical version lives in the repo-root ``package.json``; this module reads it
so there is exactly one place to bump. ``resolve()`` follows the skill symlink
(``~/.claude/skills/...`` → real repo), so the lookup works when installed.
The fallback is a sentinel — it is not a second version to maintain; if you see
it, ``package.json`` was unreachable.
"""
import json
import pathlib

_FALLBACK = "0.0.0+unknown"


def _read_version() -> str:
    # scripts/_version.py → parents[3] == repo root (holds package.json)
    package_json = pathlib.Path(__file__).resolve().parents[3] / "package.json"
    try:
        return json.loads(package_json.read_text(encoding="utf-8"))["version"]
    except (OSError, ValueError, KeyError):
        return _FALLBACK


__version__ = _read_version()
