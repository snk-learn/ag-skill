# Token Observability Report

Generated: 2026-07-14_14-05-44
All numbers are estimates based on ~4 characters per token.

## Summary
- Estimated always-on tokens: 8,240
- Estimated on-demand tokens: 22,715
- Overall rating: **High**

## Always-on context

| File | Est. tokens | Rating |
|---|---:|---|
| `CLAUDE.md` | 4,120 | High |
| `.github/copilot-instructions.md` | 2,870 | Review |
| `.github/instructions/backend.instructions.md` | 780 | Good |
| `AGENTS.md` | 470 | Excellent |

## Reduction opportunities

| Change | Est. tokens saved | Confidence |
|---|---:|---|
| Move examples from CLAUDE.md to `.claude/skills/examples/` | 2,600 | High |
| Split copilot-instructions.md into path-specific files | 1,200 | Medium |
| Move onboarding notes out of AGENTS.md | 200 | High |
| **Total potential reduction** | **4,000** | |

## Estimated session cost (20 turns)

| Item | Rate per 1M | Cost |
|---|---:|---:|
| Input | 3.00 | 0.0553 |
| Output | 15.00 | 0.1500 |
| **Total** |  | **0.2053** |

Estimated cost after recommended reductions: **0.1613** per session, a **~21%** decrease.