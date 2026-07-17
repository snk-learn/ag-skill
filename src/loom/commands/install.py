"""Install one or more skills into the current repo."""
from pathlib import Path
from rich.console import Console
from ..core.catalog import get_skill, list_skills
from ..core.installer import install_skill
from ..core.targets import resolve_targets

console = Console()


def run(names: list[str], target: str, all_skills: bool, force: bool):
    repo_root = Path.cwd()
    target_dirs = resolve_targets(target, repo_root)

    if all_skills:
        names = [s["name"] for s in list_skills()]

    if not names:
        console.print("[red]No skills specified.[/red] Use --all or pass skill names.")
        raise SystemExit(1)

    for name in names:
        src = get_skill(name)
        if not src:
            console.print(f"[red]✗[/red] Unknown skill: {name}")
            continue
        installed = install_skill(src, target_dirs, force=force)
        for path in installed:
            console.print(f"[green]✓[/green] Installed {name} → {path}")