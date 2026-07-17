# Token Observability Skill Guide

This guide explains how to use the `token-observability` skill in ag-skill.

## What it does

The `token-observability` skill helps you measure and report estimated token usage for AI agent workflows.

It can help you:

- Estimate token size for prompts, instructions, and skill files
- Split context into always-on and on-demand usage
- Identify the largest token contributors
- Estimate session cost from token usage and model rates
- Compare before and after changes to show token savings
- Generate a markdown token observability report

## What it cannot do

- It cannot read exact live provider token telemetry
- It cannot change runtime behavior of your agent

All values are estimates.

## When to use it

Use this skill when you need answers to questions like:

- How many tokens is this instruction file?
- Which files are driving my context size?
- What is the estimated cost of a typical session?
- Did my refactor reduce token usage?
- How much can I save by moving examples out of always-on context?

## Install the skill with ag-skill

Run from the repository root:

```powershell
ag-skill install token-observability --target copilot
```

You can also install for all supported targets:

```powershell
ag-skill install token-observability --target all
```

## Run the scripts manually

The skill includes helper scripts in `src/loom/skills/token-observability/scripts/`.

Run from the repository root.

### 1. Inventory context files

```powershell
python src/loom/skills/token-observability/scripts/scan_repo_context.py
```

### 2. Analyze always-on vs on-demand context

```powershell
python src/loom/skills/token-observability/scripts/analyze_context_size.py
```

### 3. Estimate one file or prompt

```powershell
python src/loom/skills/token-observability/scripts/estimate_prompt_tokens.py AGENTS.md
```

You can also pipe content through stdin:

```powershell
Get-Content .github/copilot-instructions.md | python src/loom/skills/token-observability/scripts/estimate_prompt_tokens.py
```

### 4. Estimate session cost

```powershell
python src/loom/skills/token-observability/scripts/session_cost_estimator.py
```

Example with custom settings:

```powershell
python src/loom/skills/token-observability/scripts/session_cost_estimator.py --turns 30 --retrieved-tokens-per-turn 1200 --output-tokens-per-turn 600
```

### 5. Compare before and after token impact

```powershell
python src/loom/skills/token-observability/scripts/compare_before_after.py before.md after.md
```

### 6. Generate one combined report

```powershell
python src/loom/skills/token-observability/scripts/generate_observability_report.py
```

Report output location:

- `.grimoire/reports/token-observability-<timestamp>.md`

## Suggested workflow

1. Run `analyze_context_size.py` to evaluate always-on risk.
2. Run `scan_repo_context.py` to find top contributors.
3. Run `session_cost_estimator.py` for rough spend impact.
4. Move non-essential examples or long references out of always-on files.
5. Run `compare_before_after.py` to confirm savings.
6. Generate and share the final report.

## Notes

- Estimates use a character-to-token approximation (default about 4 characters per token).
- Real tokenization varies by model and provider.
- Always validate pricing inputs before sharing cost numbers externally.
