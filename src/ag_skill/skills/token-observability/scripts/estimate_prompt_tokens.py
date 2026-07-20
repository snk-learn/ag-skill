#!/usr/bin/env python3
"""Estimate tokens for a single file or a piped string."""

import argparse
import sys
from pathlib import Path


def approx_tokens(text: str, chars_per_token: int = 4) -> int:
    if not text:
        return 0
    return max(1, len(text) // chars_per_token)


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate tokens for a file or stdin.")
    parser.add_argument("path", nargs="?", help="File path to estimate. Omit to read stdin.")
    parser.add_argument("--chars-per-token", type=int, default=4)
    args = parser.parse_args()

    if args.path:
        path = Path(args.path)
        if not path.is_file():
            print(f"File not found: {path}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        label = str(path)
    else:
        text = sys.stdin.read()
        label = "<stdin>"

    tokens = approx_tokens(text, args.chars_per_token)
    print("# Prompt Token Estimate\n")
    print(f"- Source: `{label}`")
    print(f"- Characters: {len(text)}")
    print(f"- Lines: {len(text.splitlines())}")
    print(f"- Estimated tokens: **{tokens}**")
    print(f"- Estimation ratio: {args.chars_per_token} characters per token")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())