#!/usr/bin/env python3
"""Estimate cost per typical session based on always-on context size."""

import argparse
import os
from pathlib import Path


ALWAYS_ON = [
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".claude/CLAUDE.md",
]

ALWAYS_ON_DIR = ".github/instructions"


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def always_on_tokens(root: Path) -> int:
    total = 0
    for name in ALWAYS_ON:
        file = root / name
        if file.is_file():
            total += approx_tokens(file.read_text(encoding="utf-8", errors="ignore"))

    directory = root / ALWAYS_ON_DIR
    if directory.is_dir():
        for file in directory.rglob("*.instructions.md"):
            if file.is_file():
                total += approx_tokens(file.read_text(encoding="utf-8", errors="ignore"))

    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimate session cost.")
    parser.add_argument("--turns", type=int, default=20)
    parser.add_argument("--output-tokens-per-turn", type=int, default=500)
    parser.add_argument("--retrieved-tokens-per-turn", type=int, default=1000)
    parser.add_argument("--input-rate-per-m", type=float,
                        default=float(os.getenv("TOKEN_INPUT_RATE_PER_M", "3.0")))
    parser.add_argument("--output-rate-per-m", type=float,
                        default=float(os.getenv("TOKEN_OUTPUT_RATE_PER_M", "15.0")))
    args = parser.parse_args()

    root = Path.cwd()
    baseline = always_on_tokens(root)

    input_per_turn = baseline + args.retrieved_tokens_per_turn
    total_input = input_per_turn * args.turns
    total_output = args.output_tokens_per_turn * args.turns

    input_cost = total_input / 1_000_000 * args.input_rate_per_m
    output_cost = total_output / 1_000_000 * args.output_rate_per_m
    total_cost = input_cost + output_cost

    print("# Session Cost Estimate\n")
    print(f"- Always-on baseline: **{baseline}** est. tokens")
    print(f"- Retrieved per turn: {args.retrieved_tokens_per_turn}")
    print(f"- Output per turn: {args.output_tokens_per_turn}")
    print(f"- Turns per session: {args.turns}")
    print(f"- Total input tokens: **{total_input}**")
    print(f"- Total output tokens: **{total_output}**\n")

    print("| Item | Rate per 1M | Cost |")
    print("|---|---:|---:|")
    print(f"| Input | {args.input_rate_per_m:.2f} | {input_cost:.4f} |")
    print(f"| Output | {args.output_rate_per_m:.2f} | {output_cost:.4f} |")
    print(f"| **Total** |  | **{total_cost:.4f}** |")

    print("\nNote: All figures are estimates. Verify rates with your provider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())