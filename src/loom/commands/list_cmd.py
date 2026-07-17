"""List available skills in the bundled catalog."""
from rich.console import Console
from rich.table import Table
from ..core.catalog import list_skills

console = Console()


def run():
    skills = list_skills()
    table = Table(title="ag-skill Skills Catalog", show_lines=True)
    table.add_column("Skill", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Description")
    for s in skills:
        desc = s["description"][:100] + ("…" if len(s["description"]) > 100 else "")
        table.add_row(s["name"], s["version"], desc)
    console.print(table)