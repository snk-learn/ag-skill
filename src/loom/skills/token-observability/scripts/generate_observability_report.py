#!/usr/bin/env python3
"""Run all scripts and produce a single markdown report artifact."""

import datetime
import subprocess
from pathlib import Path


SCRIPTS = [
    "scan_repo_context.py",
    "analyze_context_size.py",
    "session_cost_estimator.py",
]


def run(script: Path) -> str:
    if not script.exists():
        return f"## {script.name}\n\nScript not found.\n"

    result = subprocess.run(
        ["python", str(script)],
        capture_output=True,
        text=True,
        check=False,
    )

    body = f"## {script.name}\n\n"
    if result.stdout.strip():
        body += result.stdout.strip() + "\n"
    if result.stderr.strip():
        body += "\n### stderr\n\n```text\n" + result.stderr.strip() + "\n```\n"
    return body


def main() -> int:
    script_dir = Path(__file__).parent
    root = Path.cwd()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_dir = root / ".grimoire" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"token-observability-{timestamp}.md"

    parts = [
        "# Token Observability Report",
        "",
        f"Generated: {timestamp}",
        "",
        "All numbers are estimates based on ~4 characters per token.",
        "Verify provider rates before quoting costs.",
        "",
    ]

    for script_name in SCRIPTS:
        parts.append(run(script_dir / script_name))
        parts.append("")

    output_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())