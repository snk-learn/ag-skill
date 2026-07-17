# Report Format

Every report produced by this skill must include the following sections.

## Required sections

1. Summary
2. Always-on context table
3. On-demand context table
4. Top contributors
5. Reduction opportunities
6. Estimated session cost
7. Notes and caveats

## Style rules

- Use tables for numeric data.
- Sort tables by estimated tokens, descending.
- Bold high-impact recommendations.
- Label every numeric column with "Est." when estimated.
- Include a footer stating the estimation method and character-per-token ratio.

## Report location

Write reports to `.loom/reports/token-observability-<timestamp>.md`
when possible. Fall back to `token-observability-report.md` at repo root.