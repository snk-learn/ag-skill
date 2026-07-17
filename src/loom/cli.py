"""ag-skill CLI entry point."""
import typer
from rich.console import Console

from .commands import login as login_cmd
from .commands import list_cmd, install, remove, upgrade, add, doctor
#from .licensing.gate import require_license

console = Console()
app = typer.Typer(
    name="ag-skill",
    help="ag-skill - install curated AI agent skills into any repository.",
    no_args_is_help=True,
)
#app.add_typer(login_cmd.app, name="")  # exposes `ag-skill login` and `ag-skill logout`


@app.command("list")
def list_command():
    """List available skills in the catalog."""
    list_cmd.run()


@app.command("install")
#@require_license(feature="install")
def install_command(
    names: list[str] = typer.Argument(None, help="Skill names to install"),
    target: str = typer.Option("copilot", "--target", "-t", help="copilot | claude | cursor | all | comma-separated"),
    all_skills: bool = typer.Option(False, "--all", help="Install every skill in the catalog"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing skills"),
):
    """Install one or more skills into the current repo."""
    install.run(names or [], target, all_skills, force)


@app.command("remove")
#@require_license()
def remove_command(
    names: list[str] = typer.Argument(..., help="Skill names to remove"),
    target: str = typer.Option("all", "--target", "-t"),
):
    """Remove installed skills."""
    remove.run(names, target)


@app.command("upgrade")
#@require_license(feature="upgrade")
def upgrade_command(
    target: str = typer.Option("all", "--target", "-t"),
):
    """Upgrade all installed skills to the latest catalog version."""
    upgrade.run(target)


@app.command("add")
#@require_license(feature="add")
def add_command(
    name: str = typer.Argument(..., help="Custom skill name (kebab-case)"),
    target: str = typer.Option("copilot", "--target", "-t"),
):
    """Scaffold a new custom skill."""
    add.run(name, target)


@app.command("doctor")
def doctor_command():
    """Validate installed skills against the agentskills.io spec."""
    doctor.run()


@app.command("version")
def version_command():
    """Show ag-skill version."""
    from . import __version__
    console.print(f"ag-skill {__version__}")


if __name__ == "__main__":
    app()