# Mode-Routing Cheatsheet

Classify every incoming request into one mode before acting. This bounds how
much searching, planning, and output the turn should cost — the single
biggest lever for reducing token spend in agentic coding sessions.

## Mode 1 — Investigate
**Trigger phrases:** "How does X work?", "Where is Y defined?", "What does this
function do?", "Why is Z happening?"
**Action:** Search/read silently, then answer directly.
**Do not:** produce a plan, restate the question, or dump full file contents
into chat — link to the file/line instead.
**Output budget:** a few sentences plus file references.

## Mode 2 — Fast-path
**Trigger phrases:** "Fix this typo", "Rename this variable", "Change this
value", "Center the button" — any single, unambiguous, localized change.
**Action:**
1. Locate the exact span (read only what's needed to get correct context).
2. Apply one targeted edit (search-and-replace style, not full-file rewrite).
3. Close with a one-sentence summary. No upfront planning step.

## Mode 3 — Plan
**Trigger phrases:** "Add a new feature", "Implement auth", "Refactor the
database layer", "Migrate X to Y" — multi-file or architecturally significant
changes.
**Action:**
1. **Silent trace phase:** explore dependencies/impacted files without editing.
2. **Plan artifact:** produce a short plan (todo list or plan doc) naming exact
   files to touch and the intended change per file.
3. **Approval gate:** for high-risk/large-blast-radius changes, pause for user
   confirmation before executing (skip the pause for low-risk internal repos
   when the user has already approved the plan).
4. **Execute + track:** implement against the plan, checking items off as
   completed.
5. **Verify:** run the project's build/lint/test command before declaring done.
6. **Log the decision:** append a one-line note (pattern used, files touched)
   to persistent memory/notes so a future session doesn't need to re-derive
   this context from scratch.

## Decision table
| Signal | Mode |
|---|---|
| Question, no code change requested | Investigate |
| Single file, single well-defined change | Fast-path |
| New feature / multiple files / unclear blast radius | Plan |
| Ambiguous request that could be small or large | Ask a clarifying question before picking a mode — don't guess by writing exploratory code |

## Anti-patterns to avoid
- Writing a full implementation plan for a one-line fix (wastes tokens on
  ceremony).
- Editing files directly during the "silent trace" phase of Plan mode.
- Re-explaining the same architectural decision every session instead of
  reading/writing a persistent notes file.
