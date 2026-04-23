#!/usr/bin/env python3
"""Scaffold and open repeatable REAPER sessions on macOS.

Examples:
  python reaper_session_helper.py scaffold ~/Music/witch-audio-reaper --name plugin-load-test
  python reaper_session_helper.py scaffold ~/Music/witch-audio-reaper --name bounce-null-test --template ~/Templates/reaper/base-harness.rpp
  python reaper_session_helper.py open ~/Music/witch-audio-reaper/plugin-load-test/plugin-load-test.rpp
  python reaper_session_helper.py activate
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

SESSION_SUBDIRS = [
    "audio",
    "renders",
    "exports",
    "notes",
    "media",
]

README_TEMPLATE = """# {name}

REAPER session scaffold for witch.audio.

Created assets:
- audio/
- renders/
- exports/
- notes/
- media/
- planned project path: {project_file}

Suggested next steps:
1. Open REAPER.
2. Save a new session to {project_file} if this scaffold started without a template.
3. Put source material in audio/ or media/.
4. Render outputs into renders/ or exports/.
5. Keep session notes in notes/.
"""


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def _activate_reaper() -> None:
    _run(["osascript", "-e", 'tell application id "com.cockos.reaper" to activate'])


def cmd_activate(_: argparse.Namespace) -> int:
    _activate_reaper()
    print("REAPER activated")
    return 0


def cmd_open(args: argparse.Namespace) -> int:
    project = Path(args.project).expanduser().resolve()
    if not project.exists():
        print(f"error: project not found: {project}", file=sys.stderr)
        return 1
    _run(["open", "-a", "REAPER", str(project)])
    _activate_reaper()
    print(project)
    return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    session_dir = root / args.name
    project_file = session_dir / f"{args.name}.rpp"

    session_dir.mkdir(parents=True, exist_ok=True)
    for subdir in SESSION_SUBDIRS:
        (session_dir / subdir).mkdir(parents=True, exist_ok=True)

    if args.template:
        template = Path(args.template).expanduser().resolve()
        if not template.exists():
            print(f"error: template not found: {template}", file=sys.stderr)
            return 1
        shutil.copy2(template, project_file)
    else:
        readme = session_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                README_TEMPLATE.format(name=args.name, project_file=project_file.name),
                encoding="utf-8",
            )

    print(session_dir)
    if project_file.exists():
        print(project_file)
    else:
        print(f"planned project path: {project_file}")
        print("note: no .rpp created yet; save a new REAPER project there or pass --template")
    for subdir in SESSION_SUBDIRS:
        print(session_dir / subdir)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scaffold and open REAPER sessions on macOS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold = subparsers.add_parser("scaffold", help="Create a repeatable REAPER session folder")
    scaffold.add_argument("root", help="Parent directory for session folders")
    scaffold.add_argument("--name", required=True, help="Session name, used for folder and .rpp filename")
    scaffold.add_argument("--template", help="Optional .rpp template to copy into the new session")
    scaffold.set_defaults(func=cmd_scaffold)

    open_cmd = subparsers.add_parser("open", help="Open an existing .rpp project in REAPER")
    open_cmd.add_argument("project", help="Path to a .rpp project file")
    open_cmd.set_defaults(func=cmd_open)

    activate = subparsers.add_parser("activate", help="Bring REAPER to the foreground")
    activate.set_defaults(func=cmd_activate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
