# The Phase 1-6 Overhaul Story

> Why this repo is shaped the way it is: a three-day overhaul story that turned 4 loose skills into a 3-layer architecture — and accidentally produced a working implementation of Karpathy's LLM Wiki vision.

---

## Where it started (v1, late 2025)

Knowledge MEMO v1 was four Claude Code skills: `/read`, `/insights`, `/note`, `/review`. No schema file. No MOC. No lint. No query. Just four scripts that composed into a passable flywheel:

```
read → insights → note → review
```

It worked. For about six months.

The author — a Claude Code power user whose domains are cognitive neuroscience, molecular biology, investing, and consciousness studies — ran this loop dozens of times. Hundreds of atomic cards accumulated in Obsidian. `/review` kept surfacing them for FSRS-6 spaced repetition. The cards themselves were (mostly) good.

---

## The three problems that v1 didn't solve

By early 2026, as the vault grew past the thousand-card mark, three silent failure modes became impossible to ignore:

### Problem 1: No shared schema → cards drifted

Each new session wrote cards slightly differently. Sometimes `tags` was a list, sometimes a comma-separated string. Sometimes H1 had `【】` markers, sometimes bold. Sometimes `source` was a URL, sometimes a wikilink, sometimes missing. `/note` didn't enforce a shape — it trusted that the model "would know" the conventions from context. But context windows rotate, and conventions drift.

**Symptom**: cards written three months apart looked like they came from different people.

### Problem 2: No lint → broken links multiplied invisibly

Obsidian happily displayed broken `[[wikilinks]]` in purple as "unresolved". That's a feature — purple means "knowledge gap, you know you don't know". But without a tool to audit them, the author couldn't tell which purples were intentional gaps and which were typos or renamed files. The vault graph view got denser but less reliable.

**Symptom**: clicking a link you thought led somewhere, and landing on an empty "create new file" page.

### Problem 3: No query → couldn't find what had been written

This was the most painful one. The author would remember having read something relevant — "I'm sure I wrote a card about Howard Marks on AI risk" — and waste five minutes grepping through `Cards/`, reading half-cards, eventually finding it or giving up and rewriting a duplicate.

Obsidian has full-text search, but full-text search isn't knowledge retrieval. It doesn't know that `DMN` and `default mode network` are the same thing, or that `BDNF` is discussed under "neuroplasticity" in the MOC.

**Symptom**: the vault accumulated redundant cards on the same topic because the author couldn't find the first one.

---

## The three-day overhaul (2026-04-07 to 2026-04-09)

What started as "I'll just add a `/query` skill this weekend" became a full Phase 1-6 rewrite of the vault's governance layer. Here's the compressed version:

### Phase 1-3 (Day 1): Baseline + Cleanup

- Git-init the vault (it had been living dangerously)
- Full health scan of Cards / Clippings / wikilink integrity — documenting how many broken links and orphan cards had been accumulating invisibly
- Root directory cleanup: moved stray screenshots, drafts, and inbox files into proper directories

### Phase 4 (Day 2 morning): Readwise decompression

The vault had 680 Readwise highlights dumped in as raw imports. None of them were "learned" — they were just imported. The author spent one morning compressing them into 56 "edited cards" — each 200-500 word distillations that preserved the insight and discarded the cruft.

**Why it matters for this repo**: this is what "human in the loop" looks like in practice. A LLM could have summarized those 680 highlights in 20 minutes. But then the knowledge wouldn't live in the author's head — it would live in a summary the author hadn't read. That defeats the point.

### Phase 5 (Day 2 afternoon): MOC rebuild

Seven domain MOCs were created or rebuilt from scratch. Together they index 705 wikilinks across the vault. Each MOC has the same section structure (concepts / readings / insights / research / gaps) — but the *contents* are wildly different per domain, because the domains themselves have different shapes.

This is where the author first noticed: **the MOCs are the schema**. They're not just indexes — they're the assertion "these are the kinds of things worth tracking in this domain".

### Phase 6 (Day 3): SCHEMA.md + /note dual-proposal + /lint + /query

The biggest day. Four things happened in parallel:

1. **`SCHEMA.md`** was written as the first draft of a constitution — 11 sections covering three-layer architecture, 8 Card types, a 4-dimensional tag scheme, ingestion rules, MOC rules, lint checklist, query rules, and a permission matrix.

2. **`/note`** got its dual-proposal mechanism: instead of auto-creating atomic cards, it proposes them and waits for the user to pick. This added friction. It was *meant* to add friction.

3. **`/lint`** was written as the governance counterpart. Its semantics are deliberate: **lint generates reports, lint never auto-fixes**. The user reads the report and decides.

4. **`/query`** was written to finally solve Problem 3. Its algorithm is: read the domain MOC first (get the map), then keyword-search (narrow down), then read the hit cards (assemble an answer). This mimics how the author had been manually querying the vault.

Crucially: `type/atomic` became the *sole* identification standard for atomic cards, replacing the v1 `【】-in-H1` convention. The old convention was clever (no frontmatter edits required) but tied atomic-card identity to a markdown quirk. The new convention is boring (add a tag) but robust.

---

## The Karpathy coincidence

The overhaul and Karpathy's `llm-wiki.md` gist happened in the same week. The gist appeared on Twitter in early April 2026; the author's overhaul was already mid-flight, driven by the three vault problems above, and finished a few days later. The author read the gist while the overhaul was still in progress, paused, and compared it against the `SCHEMA.md` draft already taking shape. The two documents described nearly the same architecture, in different words:

- Three layers: **Raw Sources / The Wiki / The Schema**
- Three operations: **Ingest / Query / Lint**
- A schema/rules layer the LLM reads before acting

This repo is the result of noticing that convergence and shipping fast. The vault itself isn't in the repo (it's full of personal content). But the *shape* of the vault — the SCHEMA, the 6 skills, the permission matrix, the fork-me templates, the demo gallery of four real cards — all of that is here.

**The author didn't set out to implement Karpathy's idea.** The overhaul was internal, driven by three concrete problems (drift, broken links, couldn't-find-things) that had been growing for weeks. The alignment with Karpathy's LLM Wiki vision is a side-effect of both efforts trying to solve the same underlying problem: *how do you maintain a growing knowledge base with a LLM as your collaborator?* The gist helped the author name things (Ingest / Query / Lint is a cleaner vocabulary than what the author had been using). The gist did not cause the overhaul.

---

## What's *different* from Karpathy's proposal

Two deliberate divergences. Both are spelled out in detail in [`philosophy.md`](./philosophy.md), but the short version:

1. **Knowledge MEMO adds a fourth operation: Retain.** Karpathy's vision is Ingest/Query/Lint. It assumes the wiki is the end-state. We disagree — the end-state is **knowledge in your head**, not knowledge in a markdown file. So `/review` + FSRS-6 is a first-class citizen, not an add-on.

2. **Knowledge MEMO insists on human-in-the-loop.** Karpathy writes that maintenance cost should "trend toward zero". We think that's the wrong goal for personal knowledge. A wiki maintained entirely by an agent is a wiki whose structure serves the agent — which means it will be obsolete the moment the next-generation agent ships. A wiki maintained by a human (with agent assistance) serves the human brain — which has a much longer version cycle.

These aren't technical choices, they're value choices. You might disagree, and that's fine — fork the repo, rip out `/review`, remove the dual-proposal flow from `/note`, and you'll have something closer to Karpathy's vision. The MIT license says you can. The `CONTRIBUTING.md` says we specifically won't merge that back, but you're welcome to run it on your fork.

---

## Why you're reading this

If you found this repo via Twitter — probably during the Karpathy LLM Wiki discussion — welcome. This document exists so you can decide whether this repo is worth your time.

If you want a **turn-key SaaS product for personal knowledge**: this isn't it. Go try Mem, Logseq, or Heptabase.

If you want a **reference implementation** of "what it looks like when one person actually runs a knowledge wiki for 6 months, then rebuilds the governance layer when it starts to drift": keep reading. Start with [`../SCHEMA.md`](../SCHEMA.md) and the `demo/` gallery.

If you want the philosophical essay underneath: that's in [`philosophy.md`](./philosophy.md) (short English version) and the upcoming Chinese long-form piece《实现人的四个未来化之知识 memo 化》 (link will appear in the main README once published).
