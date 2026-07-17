# Context Compression Cheatsheet

Context is finite and attention degrades as it fills (context rot). Treat it
like a budget: keep the smallest set of high-signal tokens needed for the
current step, and push everything else out to external storage.

## Techniques, cheapest to most involved

### 1. Tool-result clearing
Once a tool call's raw output has been consumed and acted on, it rarely needs
to stay in context verbatim. Drop or truncate old tool outputs from history
before the next turn, keeping only the derived conclusion.

### 2. Structured note-taking
For any multi-step task, maintain a lightweight external note (e.g. a
`NOTES.md`/todo list/session memory file) recording: goal, decisions made,
files touched, open questions. Read it back in on resume instead of
re-deriving state from full conversation history.

### 3. Compaction
When a conversation nears its context limit, summarize the history into a
compact form that preserves architectural decisions, unresolved issues, and
implementation details, then continue from the summary + the last few
relevant files — not the full transcript.

### 4. Sub-agent delegation
For deep, exploratory work (e.g. "find every place X pattern is used across a
large repo"), delegate to a sub-agent/sub-task that can burn tokens on
exploration and return only a condensed (1–2k token) summary, keeping the
main thread's context clean.

### 5. Just-in-time retrieval over pre-loading
Prefer giving the agent search/read tools over pasting entire files or docs
into the prompt upfront. Load a schema/reference doc only when the current
turn needs it (progressive disclosure — same principle as this skill's
"When to load references" section).

## Triggers to compress
- Conversation has accumulated many large tool outputs (file dumps, logs) no
  longer relevant to the current step.
- Same architectural context is being re-explained across multiple sessions.
- A single sub-task requires extensive exploration but the caller only needs
  the conclusion.

## Anti-patterns
- Aggressive summarization that drops a subtle constraint which matters
  later — bias toward recall first, then trim.
- Keeping every intermediate tool result "just in case" — this is what causes
  context rot.
