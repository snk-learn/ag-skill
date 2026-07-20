from pathlib import Path
from rich.console import Console
from ..core.catalog import get_skill
from ..core.installer import install_skill
from ..core.targets import resolve_targets

console = Console()


def run(target: str):
    repo_root = Path.cwd()
    target_dirs = resolve_targets(target, repo_root)
    for target_dir in target_dirs:
        if not target_dir.exists():
            continue
        for skill_dir in target_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            src = get_skill(skill_dir.name)
            if not src:
                console.print(f"[yellow]![/yellow] {skill_dir.name} not in catalog; skipping")
                continue
            install_skill(src, [target_dir], force=True)
            console.print(f"[green]✓[/green] Upgraded {skill_dir.name} in {target_dir}")