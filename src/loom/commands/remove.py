from pathlib import Path
from rich.console import Console
from ..core.installer import remove_skill
from ..core.targets import resolve_targets

console = Console()


def run(names: list[str], target: str):
    repo_root = Path.cwd()
    target_dirs = resolve_targets(target, repo_root)
    for name in names:
        removed = remove_skill(name, target_dirs)
        if removed:
            for p in removed:
                console.print(f"[green]✓[/green] Removed {p}")
        else:
            console.print(f"[yellow]![/yellow] {name} not found in any target")