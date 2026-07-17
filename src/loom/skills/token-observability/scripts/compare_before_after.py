#!/usr/bin/env python3
"""Compare estimated tokens between two files or two folders."""

import argparse
from pathlib import Path


TEXT_EXTS = {".md", ".mdx", ".txt", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def count_tokens(path: Path) -> int:
    if path.is_file():
        return approx_tokens(path.read_text(encoding="utf-8", errors="ignore"))

    if path.is_dir():
        total = 0
        for file in path.rglob("*"):
            if file.is_file() and file.suffix.lower() in TEXT_EXTS:
                total += approx_tokens(file.read_text(encoding="utf-8", errors="ignore"))
        return total

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare token estimates.")
    parser.add_argument("before", help="Path to the 'before' file or folder")
    parser.add_argument("after", help="Path to the 'after' file or folder")
    args = parser.parse_args()

    before_path = Path(args.before)
    after_path = Path(args.after)

    before_tokens = count_tokens(before_path)
    after_tokens = count_tokens(after_path)
    delta = before_tokens - after_tokens
    percent = (delta / before_tokens * 100) if before_tokens else 0.0

    print("# Before / After Token Comparison\n")
    print(f"- Before: `{before_path}` → **{before_tokens}** est. tokens")
    print(f"- After:  `{after_path}` → **{after_tokens}** est. tokens")
    print(f"- Difference: **{delta}** tokens")
    print(f"- Change: **{percent:.1f}%**")

    if delta > 0:
        print("\nResult: Reduction detected.")
    elif delta < 0:
        print("\nResult: Increase detected.")
    else:
        print("\nResult: No change.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())