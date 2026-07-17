# ag-skill

`ag-skill` is a command-line tool for installing and managing curated AI agent skills in any repository.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This README covers only how to install and use the CLI.

## What ag-skill Does

With `ag-skill`, you can:

- list available skills
- install one or more skills into the current repository
- remove installed skills
- upgrade installed skills
- scaffold a custom skill
- validate installed skills

## Requirements

- Python 3.11 or later
- [`uv`](https://docs.astral.sh/uv/) installed
- A local repository you want to work in

## Install

Install `ag-skill` directly from the GitHub repository using `uv`:

````powershell
uv tool install ag-skill --from git+https://github.com/snk-learn/ag-skill.git@v0.1.0
````

### Verify installation

````powershell
ag-skill --help
````

If the command is not recognized after installation, restart the terminal and try again.

### Upgrading ag-skill

To upgrade to a newer release tag, reinstall with the new tag and `--force`:

````powershell
uv tool install ag-skill --from git+https://github.com/snk-learn/ag-skill.git@<new-tag> --force
````

## Quick Start

Open a terminal in the repository where you want to use ag-skill.

### 1. List available skills

````powershell
ag-skill list
````

### 2. Install a skill into the current repository

````powershell
ag-skill install <skill-name>
````

Example:

````powershell
ag-skill install testing
````

## Usage

Run all commands from the root of the repository you want to update.

### List skills

Show all skills available in the catalog.

````powershell
ag-skill list
````

Help:

````powershell
ag-skill list --help
````

### Install skills

Install one or more catalog skills into the current repository.

````powershell
ag-skill install <skill-name>
````

Install multiple skills:

````powershell
ag-skill install <skill-one> <skill-two>
````

Install all available skills:

````powershell
ag-skill install --all
````

Install for a specific target:

````powershell
ag-skill install <skill-name> --target copilot
````

Force overwrite existing installed skills:

````powershell
ag-skill install <skill-name> --force
````

Install everything at once (all skills, all targets, overwriting existing ones):

````powershell
ag-skill install --all --target all --force
````

Help:

````powershell
ag-skill install --help
````

Supported install targets:

- `copilot`
- `claude`
- `cursor`
- `all`
- comma-separated target values

### Remove skills

Remove one or more installed skills.

````powershell
ag-skill remove <skill-name>
````

Remove multiple skills:

````powershell
ag-skill remove <skill-one> <skill-two>
````

Remove from a specific target:

````powershell
ag-skill remove <skill-name> --target all
````

Help:

````powershell
ag-skill remove --help
````

### Upgrade installed skills

Upgrade installed skills to the latest catalog version.

````powershell
ag-skill upgrade
````

Upgrade a specific target:

````powershell
ag-skill upgrade --target all
````

Help:

````powershell
ag-skill upgrade --help
````

### Add a custom skill

Scaffold a new custom skill in the repository.

````powershell
ag-skill add <skill-name>
````

Example:

````powershell
ag-skill add my-custom-skill
````

Specify a target:

````powershell
ag-skill add my-custom-skill --target copilot
````

Help:

````powershell
ag-skill add --help
````

### Validate installed skills

Validate installed skills against the supported spec.

````powershell
ag-skill doctor
````

Help:

````powershell
ag-skill doctor --help
````

### Show version

````powershell
ag-skill version
````

Help:

````powershell
ag-skill version --help
````

## CLI Help

### Top-level help

````powershell
ag-skill --help
````

### Command help

````powershell
ag-skill list --help
ag-skill install --help
ag-skill remove --help
ag-skill upgrade --help
ag-skill add --help
ag-skill doctor --help
ag-skill version --help
````

## Common Examples

List skills:

````powershell
ag-skill list
````

Install a skill:

````powershell
ag-skill install testing
````

Install multiple skills:

````powershell
ag-skill install testing docs ci
````

Install all skills:

````powershell
ag-skill install --all
````

Install all skills for all targets, overwriting existing ones:

````powershell
ag-skill install --all --target all --force
````

Remove a skill:

````powershell
ag-skill remove testing
````

Upgrade installed skills:

````powershell
ag-skill upgrade
````

Validate installed skills:

````powershell
ag-skill doctor
````

## Notes

- Run ag-skill inside the repository you want to update.
- Use `ag-skill --help` or `<command> --help` to see the latest supported options.
- The `install` command installs catalog skills into a repository.
- The `add` command scaffolds a new custom skill.

## Docs

- [Token Observability Skill Guide](docs/skills/token-obserabilty.md)

## License

ag-skill is open source, released under the [MIT License](LICENSE). Any use, distribution, or derivative work must credit ag-skill and reference its repository URL: https://github.com/snk-learn/ag-skill
