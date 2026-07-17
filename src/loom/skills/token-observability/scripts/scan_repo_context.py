#!/usr/bin/env python3
"""Inventory every AI-relevant context file in the repository."""

from pathlib import Path


TARGETS = [
    ".github/copilot-instructions.md",
    ".github/instructions",
    ".github/prompts",
    ".github/skills",
    ".claude",
    ".agents/skills",
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
]

TEXT_EXTS = {".md", ".mdx", ".txt", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}


def approx_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def collect(root: Path):
    for target in TARGETS:
        path = root / target
        if path.is_file():
            yield path
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and file.suffix.lower() in TEXT_EXTS:
                    yield file


def main() -> int:
    root = Path.cwd()
    rows = []
    for file in collect(root):
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rows.append((file, approx_tokens(text)))

    rows.sort(key=lambda item: item[1], reverse=True)
    total = sum(t for _, t in rows)

    print("# Repository Context Inventory\n")
    print(f"- Files found: **{len(rows)}**")
    print(f"- Total estimated tokens: **{total}**\n")

    print("| File | Est. tokens |")
    print("|---|---:|")
    for file, tokens in rows:
        print(f"| `{file.relative_to(root)}` | {tokens} |")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())