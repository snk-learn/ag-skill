# Context Surfaces

Use this table to classify each file when measuring.

| Path | Type | Load pattern |
|---|---|---|
| `.github/copilot-instructions.md` | Copilot repo instructions | Always-on |
| `.github/instructions/*.instructions.md` | Path-specific | Always-on when path matches |
| `.github/prompts/*.prompt.md` | Prompt file | On-demand |
| `.github/skills/<name>/SKILL.md` | Skill entry | On-demand (discovery only until activated) |
| `.github/skills/<name>/references/*` | Reference asset | On-demand |
| `.github/skills/<name>/scripts/*` | Script asset | On-demand |
| `.claude/CLAUDE.md` | Claude memory | Always-on |
| `.claude/skills/<name>/SKILL.md` | Skill entry | On-demand |
| `.agents/skills/<name>/SKILL.md` | Skill entry | On-demand |
| `AGENTS.md` | Agent instructions | Always-on |
| `README.md` (when used as prompt context) | Docs | On-demand |

## Guidance

- Keep always-on files small.
- Move workflows and examples into skills.
- Move long reference docs into `references/` inside a skill.
- Only include repo-wide constraints in always-on files.