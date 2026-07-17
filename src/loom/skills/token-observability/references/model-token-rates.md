# Model Token Rates (Reference)

Use these values as placeholders in cost estimation. Verify against current
provider pricing before quoting numbers to stakeholders.

Put your own dollar estimates in this file. The table below is the canonical
place to set per-model input and output rates used for cost calculation.

| Model family | Input (per 1M) | Output (per 1M) |
|---|---:|---:|
| Frontier reasoning | $$$ | $$$ |
| Balanced | $$ | $$ |
| Cost-efficient | $ | $ |

If you do not know exact provider prices yet, replace `$$$`, `$$`, and `$`
with your best estimates and clearly label outputs as estimates.

The scripts in this skill accept override values via CLI flags or environment
variables:

- `TOKEN_INPUT_RATE_PER_M`
- `TOKEN_OUTPUT_RATE_PER_M`

## Guidance

- Do not present dollar figures without confirming current provider pricing.
- Prefer showing relative reduction (percent) when absolute rates are unknown.
- Use the "cost-efficient" tier for simple edits and the "frontier" tier only
  for complex reasoning or planning tasks.