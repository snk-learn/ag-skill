"""Copy skill folders into target repo locations."""
import shutil
from pathlib import Path
from rich.console import Console

console = Console()


def install_skill(src: Path, target_dirs: list[Path], *, force: bool = False) -> list[Path]:
    """Copy `src` skill folder into each target directory. Returns installed paths."""
    installed = []
    for target in target_dirs:
        target.mkdir(parents=True, exist_ok=True)
        dest = target / src.name
        if dest.exists() and not force:
            console.print(f"[yellow]Skipping[/yellow] {dest} (exists; use --force to overwrite)")
            continue
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        installed.append(dest)
    return installed


def remove_skill(name: str, target_dirs: list[Path]) -> list[Path]:
    """Remove `name` skill folder from each target directory. Returns removed paths."""
    removed = []
    for target in target_dirs:
        dest = target / name
        if dest.exists():
            shutil.rmtree(dest)
            removed.append(dest)
    return removed