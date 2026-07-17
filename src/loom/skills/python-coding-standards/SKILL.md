---
name: python-coding-standards
description: >-
  Enforces modern Python 3.11+ standards including type hints, async patterns,
  ruff/mypy configuration, pytest conventions, and secure error handling. Use
  when generating, reviewing, or refactoring Python code (.py files) or
  configuring a Python project's tooling.
license: MIT
compatibility: Python 3.11+
metadata:
  author: Shariq Khan
  version: "1.0.0"
---

# Python Coding Standards

## Core rules
1. Type hints on every public function. Use `from __future__ import annotations`.
2. Async for all I/O. Never block the event loop.
3. Ruff + mypy strict. Config in `scripts/ruff.toml`.
4. pytest, not unittest. Coverage ≥70% on new code.
5. Specific exceptions. No bare `except:`. Chain with `raise ... from e`.
6. No secrets in code. Use environment variables.

## When to load references
- Editing async code → `references/async-patterns.md`
- Setting up tooling → `references/pep8-cheatsheet.md` + `scripts/ruff.toml`

## Definition of done
- `ruff check` passes, `mypy --strict` passes
- Tests exist for every new public function