"""Load bundled skills from the wheel."""

import importlib.resources as pkg
from pathlib import Path
import yaml


def catalog_root() -> Path:
    """Path to the bundled skills folder inside the installed package."""
    return Path(pkg.files("loom").joinpath("skills"))


def list_skills() -> list:
    """Return a list of {name, description, version} for each bundled skill."""
    root = catalog_root()
    skills = []
    for skill_dir in sorted(root.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        meta = _parse_frontmatter(skill_md)
        skills.append({
            "name": meta.get("name", skill_dir.name),
            "description": meta.get("description", ""),
            "version": (meta.get("metadata") or {}).get("version", "0.0.0"),
            "path": skill_dir,
        })
    return skills


def get_skill(name: str) -> Path | None:
    root = catalog_root()
    candidate = root / name
    return candidate if (candidate / "SKILL.md").exists() else None


def _parse_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, fm, _ = text.split("---", 2)
    return yaml.safe_load(fm) or {}