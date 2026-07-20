from typer.testing import CliRunner
from ag_skill.cli import app

runner = CliRunner()


def test_list_runs():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "python-coding-standards" in result.stdout


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "ag-skill" in result.stdout