---
name: token-observability
description: >
  Measure, estimate, and report token usage for AI agent workflows. Use when the user
  asks to see token usage, estimate token cost, measure context size, analyze prompt
  size, compare before/after token savings, estimate session cost, audit Copilot or
  Claude context footprint, or produce a token usage report. Produces evidence-backed
  reports with estimated tokens, cost estimates, and reduction opportunities.
license: MIT
compatibility: Requires python3
metadata:
  author: ag-skill
  version: "1.0"
---

# Token Observability

Use this skill to produce measurable, evidence-backed token usage reports for
AI-assisted engineering workflows across GitHub Copilot, Claude Code, Cursor,
Codex, and other Agent Skills-compatible agents.

This skill is a **measurement tool**, not a behavior modifier. It answers:

- How large is my agent context today?
- Which files contribute the most tokens?
- What is the estimated cost per session?
- How much could I reduce by moving X into a reference file?
- What is the before/after impact of a refactor?

## Important: what this skill can and cannot do

**Can do**
- Estimate tokens for files, folders, prompts, and instructions
- Rank context contributors by estimated token weight
- Estimate cost per session using published model rates
- Produce a before/after comparison for a proposed change
- Detect always-on vs on-demand context and score footprint
- Generate a markdown report artifact

**Cannot do**
- Report the exact live token count from the model provider during a chat
- Read Copilot or Claude session telemetry
- Modify agent behavior at runtime

All numbers reported are **estimates**, based on character-to-token approximations
(default ~4 characters per token for English). Always label estimates clearly.

## When to use

Trigger this skill when the user asks:

- "How many tokens is my CLAUDE.md?"
- "Show me my agent context size"
- "Estimate the cost of this prompt"
- "Which instruction files are the biggest?"
- "Compare tokens before and after my changes"
- "How much would I save if I moved examples to references?"
- "Give me a token observability report"

## Workflow

### Step 1 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Establish scope

Ask the user which scope to measure:

- Whole repo agent context (default)
- A specific file or folder
- A single prompt or draft
- Before/after comparison

If unspecified, default to whole-repo agent context.

### Step 2 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Identify context surfaces

Always-on context surfaces:

- `.github/copilot-instructions.md`
- `.github/instructions/**/*.instructions.md`
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

On-demand context surfaces:

- `.github/prompts/**/*.prompt.md`
- `.github/skills/**/SKILL.md` and their `references/`, `scripts/`, `examples/`
- `.claude/skills/**/SKILL.md` and subfolders
- `.agents/skills/**/SKILL.md` and subfolders

Track these separately. Always-on context is billed on every request.

### Step 3 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Run measurement scripts

Prefer scripts over manual estimation.

Run in this order:

1. `scripts/scan_repo_context.py` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â inventory all context files
2. `scripts/analyze_context_size.py` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â classify always-on vs on-demand
3. `scripts/estimate_prompt_tokens.py <file>` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â per-file estimate
4. `scripts/session_cost_estimator.py` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â cost estimate for typical session
5. `scripts/generate_observability_report.py` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â produce final report artifact

For before/after:

- `scripts/compare_before_after.py <before_path> <after_path>`

### Step 4 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Interpret results

Use these thresholds for always-on files:

| Estimated tokens | Rating |
|---|---|
| < 500 | Excellent |
| 500 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ 1,500 | Good |
| 1,500 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ 3,000 | Review |
| 3,000 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“ 6,000 | High |
| > 6,000 | Critical |

For skills, `SKILL.md` above 2,000 estimated tokens should move content to
`references/` for progressive disclosure.

### Step 5 ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â Recommend actions

Recommend only actions that reduce always-on tokens without removing essential
correctness, security, or compliance guidance. Preferred actions:

- Move examples out of `SKILL.md` into `examples/`
- Move long reference docs out of `SKILL.md` into `references/`
- Split a monolithic instructions file into path-specific instructions
- Move workflow steps out of instructions into skills
- Move one-shot prompts into `.github/prompts/`
- Replace verbatim logs with summarized artifacts

## Output format

Return the report in this format:

```markdown
# Token Observability Report

## Summary
- Estimated always-on tokens: X
- Estimated on-demand tokens: Y
- Estimated cost per typical session: $Z
- Rating: <Excellent | Good | Review | High | Critical>

## Always-on context
| File | Est. tokens | Rating |
|---|---:|---|

## On-demand context
| Skill / Prompt | Est. tokens | Rating |
|---|---:|---|

## Top contributors
1. ...
2. ...
3. ...

## Reduction opportunities
| Change | Est. tokens saved | Confidence |
|---|---:|---|

## Estimated session cost
| Model | Rate (per 1M input) | Est. per session |
|---|---:|---:|

## Notes and caveats
- All numbers are estimates.
- Actual model tokenization may differ.