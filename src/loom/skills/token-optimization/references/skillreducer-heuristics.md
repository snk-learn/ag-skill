# Skill/Tool-Set Reduction Heuristics

Bloated tool and skill sets cost tokens twice: once for every schema sent on
every turn, and again in reasoning quality — ambiguous overlapping tools make
selection harder for the model.

## Heuristics

1. **One clear job per tool/skill.** If a human engineer can't say definitively
   which tool applies in a given situation, the model can't either. Merge or
   split until each tool has an unambiguous purpose.
2. **Minimal viable tool set.** Only expose tools relevant to the current
   turn/task, not the full catalog. Filter before sending (see core rule 4).
3. **Description does the routing.** A skill's `description` frontmatter field
   is the only thing loaded into context until it's actually invoked
   (progressive disclosure). Front-load it with concrete trigger phrases
   ("WHEN: ...") so the router can decide without reading the whole body.
4. **No overlapping descriptions.** If two skills/tools could plausibly match
   the same request, add explicit "DO NOT USE FOR" exclusions to disambiguate
   (see this repo's sibling skills for the pattern).
5. **Keep SKILL.md bodies short.** Core rules should fit on one screen; push
   depth into `references/*.md`, loaded only when the rule says to.
6. **Descriptive, unambiguous parameters.** Tool input schemas should be
   self-explanatory — avoid parameters requiring out-of-band documentation to
   use correctly.
7. **Prune dead tools regularly.** Remove tools/skills that haven't been
   invoked in practice; every unused schema in the request is pure token
   waste.

## Quick audit questions
- Does every tool/skill description contain concrete trigger phrases, not just
  a category name?
- Could a new tool be confused with an existing one? If yes, add disambiguation.
- Is any tool schema carrying parameters nobody sets? Remove them.
- Is the full tool catalog sent on every turn, or filtered per task?
