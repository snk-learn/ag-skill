#!/usr/bin/env python3
"""Classify repo context as always-on vs on-demand and estimate tokens."""

from pathlib import Path


ALWAYS_ON_FILES = [
    ".github/copilot-instructions.md",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".claude/CLAUDE.md",
]

ALWAYS_ON_GLOBS = [
    (".github/instructions", "*.instructions.md"),
]

ON_DEMAND_GLOBS = [
    (".github/prompts", "*.prompt.md"),
    (".github/skills", "**/*"),
    (".claude/skills", "**/*"),
    (".agents/skills", "**/*"),
]

TEXT_EXTS = {".md", ".mdx", ".txt", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def read_tokens(path: Path) -> int:
    try:
        return approx_tokens(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return 0


def collect_always_on(root: Path):
    for name in ALWAYS_ON_FILES:
        file = root / name
        if file.is_file():
            yield file

    for directory, pattern in ALWAYS_ON_GLOBS:
        base = root / directory
        if base.is_dir():
            for file in base.rglob(pattern):
                if file.is_file():
                    yield file


def collect_on_demand(root: Path):
    for directory, pattern in ON_DEMAND_GLOBS:
        base = root / directory
        if base.is_dir():
            for file in base.rglob(pattern):
                if file.is_file() and file.suffix.lower() in TEXT_EXTS:
                    yield file


def rating(tokens: int) -> str:
    if tokens < 500:
        return "Excellent"
    if tokens < 1500:
        return "Good"
    if tokens < 3000:
        return "Review"
    if tokens < 6000:
        return "High"
    return "Critical"


def main() -> int:
    root = Path.cwd()

    always_on = sorted(set(collect_always_on(root)))
    on_demand = sorted(set(collect_on_demand(root)))

    always_rows = [(f, read_tokens(f)) for f in always_on]
    demand_rows = [(f, read_tokens(f)) for f in on_demand]

    always_total = sum(t for _, t in always_rows)
    demand_total = sum(t for _, t in demand_rows)

    print("# Context Size Analysis\n")
    print(f"- Estimated always-on tokens: **{always_total}**")
    print(f"- Estimated on-demand tokens: **{demand_total}**")
    print(f"- Overall rating: **{rating(always_total)}**\n")

    print("## Always-on context\n")
    print("| File | Est. tokens | Rating |")
    print("|---|---:|---|")
    for file, tokens in sorted(always_rows, key=lambda item: item[1], reverse=True):
        print(f"| `{file.relative_to(root)}` | {tokens} | {rating(tokens)} |")

    print("\n## On-demand context (top 20 by size)\n")
    print("| File | Est. tokens | Rating |")
    print("|---|---:|---|")
    for file, tokens in sorted(demand_rows, key=lambda item: item[1], reverse=True)[:20]:
        print(f"| `{file.relative_to(root)}` | {tokens} | {rating(tokens)} |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())