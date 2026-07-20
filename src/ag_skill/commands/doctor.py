from pathlib import Path
from rich.console import Console
from ..core.validator import validate_skill

console = Console()


def run():
    repo_root = Path.cwd()
    checked = 0
    failed = 0
    for target in [".github/skills", ".claude/skills", ".agents/skills"]:
        target_dir = repo_root / target
        if not target_dir.exists():
            continue
        for skill_dir in target_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            checked += 1
            errors = validate_skill(skill_dir)
            if errors:
                failed += 1
                console.print(f"[red]✗ {skill_dir}[/red]")
                for e in errors:
                    console.print(f"    - {e}")
            else:
                console.print(f"[green]✓ {skill_dir}[/green]")
    console.print(f"\n[bold]{checked} checked, {failed} failed[/bold]")
    if failed:
        raise SystemExit(1)