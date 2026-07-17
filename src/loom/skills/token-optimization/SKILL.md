---
name: token-optimization
description: >-
  Applies token-efficiency patterns to prompts, agents, and RAG pipelines
  including prompt caching, progressive disclosure, model routing, tool
  filtering, and context compression. Use when writing prompts, designing
  multi-step agent workflows, or reviewing LLM code for cost.
license: MIT
metadata:
  author: Shariq Khan
  version: "1.1.0"
---

# Token Optimization

## Core rules
1. **Cache stable prefixes.** Move system prompt + tool defs to the top; use provider caching.
2. **Route by complexity.** Cheap model (Haiku, GPT-nano) for classification/titles; premium only when reasoning is required.
3. **Progressive disclosure.** Don't inject a schema, doc, or example until this turn needs it.
4. **Filter tools.** Prune tools list to those relevant to the current turn before sending.
5. **Compress history.** Summarize conversation after N turns; drop redundant tool outputs.
6. **Return structured errors.** Actionable error messages prevent retry loops.
7. **Measure first.** Instrument token counts per node; optimize the top 3 spenders.
8. **Route by task mode.** Classify each request as Investigate / Fast-path / Plan (see reference) before acting — this bounds how much context and output the turn should cost.
9. **Investigate silently.** For "how does X work" / "where is Y" questions, search and answer directly. No plan, no restating the question, no full-file dumps.
10. **Fast-path small edits.** For a typo, one-line fix, or single-value change: locate the exact span, apply a targeted edit, and close with a one-sentence summary — never regenerate the whole file in chat.
11. **Plan before large edits, then log the decision.** For multi-file or architectural changes: trace dependencies first without editing, produce a short plan, and after completion append a one-line note (design pattern used, files touched) to persistent memory/notes so the next session doesn't re-derive it.

## When to load references
- Adding caching → `references/prompt-caching-cheatsheet.md`
- Skill/tool design → `references/skillreducer-heuristics.md`
- Deciding investigate vs. fast-path vs. plan → `references/mode-routing-cheatsheet.md`
- Long-running or multi-turn agent sessions → `references/context-compression-cheatsheet.md`
- Auditing a repo → run `scripts/token_audit.py <path>`

## Definition of done
- Cached-token ratio ≥60% on steady-state traffic
- No unused tool schemas in requests
- Per-turn token usage tracked in observability
- Every turn was handled at the cheapest mode (Investigate/Fast-path/Plan) that fit the request