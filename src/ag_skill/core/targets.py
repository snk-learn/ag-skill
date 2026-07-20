"""Resolve where skills should be installed based on --target flag."""

from pathlib import Path

TARGETS = {
    "copilot": ".github/skills",
    "claude": ".claude/skills",
    "cursor": ".agents/skills",
    "codex": ".agents/skills",
    "generic": ".agents/skills",
}


def resolve_targets(target: str, repo_root: Path) -> list[Path]:
    """Return one or more target directories for the chosen integration."""
    if target == "all":
        return [repo_root / p for p in {".github/skills", ".claude/skills", ".agents/skills"}]
    keys = [t.strip() for t in target.split(",")]
    dirs = []
    for k in keys:
        if k not in TARGETS:
            raise ValueError(f"Unknown target '{k}'. Valid: {', '.join(TARGETS)} or 'all'.")
        dirs.append(repo_root / TARGETS[k])
    return dirs