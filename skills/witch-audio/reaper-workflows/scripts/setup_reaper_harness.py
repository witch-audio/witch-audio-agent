#!/usr/bin/env python3
"""Create a simple REAPER validation harness folder structure.

Usage:
  python setup_reaper_harness.py /path/to/harness-root
"""

from __future__ import annotations

import sys
from pathlib import Path

SUBDIRS = [
    'projects',
    'renders',
    'notes',
    'screenshots',
    'source-audio',
]

README = """# REAPER Validation Harness

Suggested projects:
- plugin-load-test.rpp
- automation-torture-test.rpp
- recall-reopen-test.rpp
- render-null-test.rpp

Put source loops in source-audio/
Put rendered artifacts in renders/
Keep notes in notes/
"""


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: python setup_reaper_harness.py /path/to/harness-root')
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    for subdir in SUBDIRS:
        (root / subdir).mkdir(parents=True, exist_ok=True)

    readme = root / 'README.md'
    if not readme.exists():
        readme.write_text(README)

    print(root)
    for subdir in SUBDIRS:
        print(root / subdir)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
