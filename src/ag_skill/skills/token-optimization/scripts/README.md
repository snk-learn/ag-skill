# Scripts: token-optimization

- `token_audit.py` — stdlib-only heuristic token counter. Scans a repo for prompt/instruction-like files (SKILL.md, AGENTS.md, *.instructions.md, etc.), estimates token counts, and flags the largest offenders.

  ```sh
  python token_audit.py [path] [--top N] [--threshold TOKENS]
  ```
