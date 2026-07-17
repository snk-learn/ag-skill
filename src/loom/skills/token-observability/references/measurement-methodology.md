# Measurement Methodology

## Token estimation model

This skill uses a character-based approximation for portability:

```
estimated_tokens = max(1, len(text) // 4)
```

This is the widely used ~4 characters per token heuristic for English. Actual tokenization differs between providers and models. Consider these adjustments if you want tighter estimates:

- Code-heavy content: ~3 characters per token
- Natural language English: ~4 characters per token
- CJK content: ~1–2 characters per token
- Structured JSON/YAML: ~3 characters per token

If a provider offers a local tokenizer (for example, `tiktoken` for OpenAI models), you can plug it into `scripts/estimate_prompt_tokens.py` by replacing the `approx_tokens` function.

## Always-on vs on-demand context

Not all files enter the model context on every request.

### Always-on

Loaded on every request in most agent configurations:

- `.github/copilot-instructions.md`
- `.github/instructions/**/*.instructions.md` (path-matched)
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

### On-demand

Loaded only when the agent decides they are relevant:

- Skill folders
- Prompt files
- Reference documents inside skills
- Scripts inside skills
- Retrieved files from the codebase

Always-on context should be optimized first, since it multiplies with every turn.

## Session cost model

Cost per session is estimated as:

```
session_cost = (input_tokens_per_turn * turns * input_rate) + (output_tokens_per_turn * turns * output_rate)
```

Default assumptions in `session_cost_estimator.py`:

- Turns per session: 20
- Output tokens per turn: 500
- Input tokens per turn: always-on tokens + retrieved context

These are conservative defaults. Adjust to match your workload.

## Confidence levels

Reduction estimates use three confidence levels:

- **High** — measurable and deterministic (for example, moving a 3,000-token reference block out of SKILL.md).
- **Medium** — dependent on agent routing (for example, splitting an instructions file by path).
- **Low** — behavioral guess (for example, reducing verbose explanations).

Always label confidence explicitly.
