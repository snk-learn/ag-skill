#!/usr/bin/env python3
"""Heuristic token audit for prompt/instruction files in a repository.

Stdlib-only by design: this script is copied into arbitrary consumer repos
via `ag-skill install`, which may not have any third-party tokenizer installed.
It uses a chars-per-token heuristic (~4 chars/token for English text), which
is accurate enough to rank files and flag oversized ones -- it is not a
substitute for a real tokenizer when exact counts matter.

Usage:
    python token_audit.py [path] [--top N] [--threshold TOKENS]
"""

from __future__ import annotations

import argparse
from pathlib import Path

CHARS_PER_TOKEN = 4

# Filenames/patterns treated as "prompt-like" -- instructions, agent
# definitions, and skill docs that get loaded into an LLM's context.
PROMPT_GLOBS = [
    "**/*.instructions.md",
    "**/*.prompt.md",
    "**/*.agent.md",
    "**/SKILL.md",
    "**/AGENTS.md",
    "**/CLAUDE.md",
    "**/copilot-instructions.md",
]

DEFAULT_TOP_N = 10
DEFAULT_THRESHOLD = 2000

# Directories to skip regardless of matches (build artifacts, deps, VCS).
SKIP_DIR_NAMES = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 characters per token for English text."""
    return max(1, len(text) // CHARS_PER_TOKEN)


def find_prompt_files(root: Path) -> list[Path]:
    seen: set[Path] = set()
    files: list[Path] = []
    for pattern in PROMPT_GLOBS:
        for path in root.glob(pattern):
            if not path.is_file() or path in seen:
                continue
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            seen.add(path)
            files.append(path)
    return files


def audit(root: Path, top_n: int, threshold: int) -> int:
    files = find_prompt_files(root)
    if not files:
        print(f"No prompt/instruction files found under {root}")
        return 0

    results = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            print(f"skip {path}: {e}")
            continue
        results.append((path, estimate_tokens(text)))

    results.sort(key=lambda r: r[1], reverse=True)

    print(f"Scanned {len(results)} prompt-like file(s) under {root}\n")
    print(f"Top {min(top_n, len(results))} by estimated tokens:")
    for path, tokens in results[:top_n]:
        flag = " ÃƒÂ¢Ã…Â¡Ã‚Â  over threshold" if tokens > threshold else ""
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
        print(f"  {tokens:>7,} tokens  {rel}{flag}")

    over_threshold = [r for r in results if r[1] > threshold]
    if over_threshold:
        print(
            f"\n{len(over_threshold)} file(s) exceed the {threshold:,}-token "
            "threshold. Consider moving detail into references/ files loaded "
            "on demand (progressive disclosure) instead of keeping it inline."
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Repo root to scan (default: cwd)")
    parser.add_argument("--top", type=int, default=DEFAULT_TOP_N, help="Show top N files by size")
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help="Flag files above this estimated token count",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        parser.error(f"path does not exist: {root}")

    return audit(root, args.top, args.threshold)


if __name__ == "__main__":
    raise SystemExit(main())
