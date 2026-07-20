# Prompt Caching Cheatsheet

## Why
A cached prefix is billed once and reused across turns/requests, often at a
fraction of input-token cost. The savings only materialize if the prefix is
byte-identical between calls.

## Ordering rule
Put content from most-stable to least-stable, top to bottom:
1. System prompt / instructions (rarely changes)
2. Tool/function definitions (changes per feature, not per turn)
3. Static reference docs / examples
4. Retrieved or dynamic context (RAG chunks, file contents)
5. Conversation history
6. The current user turn (always last — never cached)

Any edit above a given point invalidates the cache for everything below it in
that call, so keep volatile content at the bottom.

## Provider notes
- **Claude (Anthropic):** explicit cache breakpoints via `cache_control`; default TTL ~5 min, extendable to 1h. Minimum cacheable prefix size applies — trivially short prompts won't cache.
- **OpenAI / Copilot-style APIs:** automatic prefix caching for prompts over a length threshold; no manual breakpoints, but ordering rule still applies since caching is prefix-based.
- Both: caching is per-exact-prefix match — whitespace/timestamp/nonce differences break it. Never inject `datetime.now()` or random IDs into the cached region.

## Practical checklist
- [ ] System prompt + tool defs are static strings, not rebuilt per request
- [ ] Few-shot examples live above dynamic RAG context, not interleaved with it
- [ ] Dynamic/user-specific content is isolated to the tail of the prompt
- [ ] Long-lived agent loops reuse the same tool schema object (no per-turn regeneration)
- [ ] Cache hit rate is logged and reviewed (target ≥60% steady-state)

## Cost math example
System prompt + tools: 3,000 tokens, reused across 20 turns in a session.
- Without caching: 3,000 × 20 = 60,000 input tokens billed at full rate.
- With caching: ~3,000 tokens billed once (or at cache-write rate), remaining 19 reads billed at cache-read rate (typically 10–25% of full input price).
- Net effect: input-token cost for the stable prefix drops ~75–90% over the session.
