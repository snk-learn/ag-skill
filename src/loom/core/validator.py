"""Validate SKILL.md files against the agentskills.io spec."""
import re
from pathlib import Path
import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill(skill_dir: Path) -> list[str]:
    """Return a list of validation errors; empty list means valid."""
    errors = []
    md = skill_dir / "SKILL.md"
    if not md.exists():
        return [f"Missing SKILL.md in {skill_dir}"]

    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ["SKILL.md must start with YAML frontmatter (---)"]

    try:
        _, fm, _ = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
    except Exception as e:
        return [f"Invalid YAML frontmatter: {e}"]

    name = meta.get("name")
    if not name:
        errors.append("Missing required field: name")
    elif not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"Invalid name '{name}': lowercase, hyphens, no leading/trailing/consecutive hyphens, ≤64 chars")
    elif name != skill_dir.name:
        errors.append(f"name '{name}' must equal folder name '{skill_dir.name}'")

    desc = meta.get("description")
    if not desc:
        errors.append("Missing required field: description")
    elif len(desc) > 1024:
        errors.append("description exceeds 1024 characters")

    return errors