"""Scaffold a new custom skill into the current repo."""
from pathlib import Path
from rich.console import Console
from ..core.targets import resolve_targets

console = Console()

SKILL_MD_TEMPLATE = """\
---
name: {name}
description: TODO: describe what this skill does (shown to agent, max 1024 chars)
---

# {name}

TODO: fill in the skill instructions here.
"""


def run(name: str, target: str):
    repo_root = Path.cwd()

    try:
        target_dirs = resolve_targets(target, repo_root)
    except ValueError as e:
        console.print(f"[red]✗[/red] {e}")
        raise SystemExit(1)

    created_any = False
    for target_dir in target_dirs:
        skill_dir = target_dir / name
        if skill_dir.exists():
            console.print(f"[yellow]⚠[/yellow]  Skill already exists: {skill_dir}")
            continue

        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            SKILL_MD_TEMPLATE.format(name=name), encoding="utf-8"
        )
        (skill_dir / "references").mkdir()
        (skill_dir / "scripts").mkdir()
        console.print(f"[green]✓[/green] Scaffolded {name} → {skill_dir}")
        created_any = True

    if not created_any:
        raise SystemExit(1)
