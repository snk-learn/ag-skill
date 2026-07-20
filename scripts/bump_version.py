#!/usr/bin/env python3
"""Bump the project version in pyproject.toml.

Usage:
    python scripts/bump_version.py major|minor|patch [--commit] [--tag]
    python scripts/bump_version.py --set 1.2.3 [--commit] [--tag]

Examples:
    python scripts/bump_version.py patch
    python scripts/bump_version.py minor --commit --tag
    python scripts/bump_version.py --set 2.0.0 --commit --tag
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = ROOT / "pyproject.toml"
VERSION_RE = re.compile(r'^version\s*=\s*"(?P<version>[^"]+)"', re.MULTILINE)


def read_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        raise SystemExit(f"Could not find a version field in {PYPROJECT}")
    return match.group("version")


def write_version(new_version: str) -> None:
    text = PYPROJECT.read_text(encoding="utf-8")
    new_text, count = VERSION_RE.subn(f'version = "{new_version}"', text, count=1)
    if count != 1:
        raise SystemExit(f"Failed to update version in {PYPROJECT}")
    PYPROJECT.write_text(new_text, encoding="utf-8")


def bump(version: str, part: str) -> str:
    try:
        major, minor, patch = (int(p) for p in version.split("."))
    except ValueError as exc:
        raise SystemExit(
            f"Current version '{version}' is not in MAJOR.MINOR.PATCH format"
        ) from exc

    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    elif part == "patch":
        patch += 1
    else:
        raise SystemExit(f"Unknown version part: {part}")

    return f"{major}.{minor}.{patch}"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump the ag-skill version.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "part",
        nargs="?",
        choices=["major", "minor", "patch"],
        help="Part of the semantic version to increment.",
    )
    group.add_argument(
        "--set",
        dest="explicit_version",
        metavar="X.Y.Z",
        help="Set an explicit version instead of bumping.",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Create a git commit for the version bump.",
    )
    parser.add_argument(
        "--tag",
        action="store_true",
        help="Create a git tag (vX.Y.Z) for the new version. Implies --commit.",
    )
    args = parser.parse_args()

    current_version = read_version()

    if args.explicit_version:
        new_version = args.explicit_version
        if not re.fullmatch(r"\d+\.\d+\.\d+", new_version):
            raise SystemExit(f"'{new_version}' is not in MAJOR.MINOR.PATCH format")
    else:
        new_version = bump(current_version, args.part)

    if new_version == current_version:
        raise SystemExit(f"Version is already {current_version}; nothing to do.")

    write_version(new_version)
    print(f"Bumped version: {current_version} -> {new_version}")

    if args.tag:
        args.commit = True

    if args.commit:
        run(["git", "add", str(PYPROJECT)])
        run(["git", "commit", "-m", f"chore: bump version to {new_version}"])
        print(f"Committed version bump for {new_version}")

    if args.tag:
        tag_name = f"v{new_version}"
        run(["git", "tag", tag_name])
        print(f"Created tag {tag_name}. Push it with: git push origin {tag_name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
