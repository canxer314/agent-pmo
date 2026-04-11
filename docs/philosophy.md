# Philosophy

> The short English landing page for non-Chinese readers who arrive via the Karpathy LLM Wiki discussion. The full long-form essay (《实现人的四个未来化之知识 memo 化》) is in Chinese and linked from the main README once published.

---

## The core thesis

> **Knowledge without a person is not even information — it has no real relationship with a user.**

Personal knowledge management is not a tool problem. It's a discipline problem: how you read, how you think, how you decide what's worth remembering. A better tool cannot do that for you.

Knowledge MEMO is built on two beliefs that follow from this thesis:

1. **Toolkit, not idea file.** A repo should give you something that runs, not a blog post that hand-waves.
2. **Human must stay in the loop.** Not as a fallback, but as the whole point.

Everything else in this repo — the SCHEMA, the 6 skills, the dual-proposal mechanism in `/note`, the Retain step with FSRS-6 — is downstream of those two commitments.

---

## Two myths to abandon before you fork this

### Myth 1: There exists a one-size-fits-all knowledge management solution.

There doesn't. Notion, Roam, Logseq, Heptabase, Obsidian, Reflect, Tana, Mem, Capacities — how many have you tried? Each one you started with hope and slowly abandoned. The issue isn't that the tools are bad. It's that personal knowledge management isn't a "tool problem" at all.

It's a problem about **how you think, how you read, how you talk to yourself**. Tools are scaffolding. They can hold the shape of your thinking, but they can't do the thinking for you.

So when you fork this repo, don't come looking for "the right template". Come looking for a working example you can measure yours against. The templates in `templates/cards/` are labeled with a "fork-me" disclaimer for exactly this reason.

### Myth 2: Imported solutions can satisfy your needs.

They can't. Including this repo.

Knowledge MEMO is the author's personal system. The demo gallery contains real cards from the author's domains: cognitive neuroscience, investing, consciousness studies, molecular biology. **These are not universal examples.** They're the shape of one person's curiosity.

Gary Tan's gbrain will think about how ideas grow (because he runs a startup accelerator). Our system thinks about how concepts cross-pollinate (because the author does interdisciplinary research). Your system will think about something else entirely — and only you know what that is.

> Please do not use this as-is. Fork it. Rewrite it. Grow your own.

---

## The Karpathy coincidence, and the two deliberate differences

Knowledge MEMO's 3-layer architecture (Schema / Flywheel / Governance) turned out to align almost perfectly with Andrej Karpathy's `llm-wiki.md` gist (Raw Sources / Wiki / Schema + Ingest/Query/Lint operations). The author did not set out to implement Karpathy's idea — the overhaul that produced this structure was already mid-flight when the gist was posted, driven by three concrete vault problems that had been growing for weeks (see [`phase-1-6-story.md`](./phase-1-6-story.md) for the timeline). The alignment is convergent, not derivative.

But there are **two deliberate divergences**, both spelled out below. They're not bug-fixes or style disagreements. They're value choices — and if you disagree with either, you should probably fork this repo hard and remove the relevant pieces.

### Philosophy comparison table

| | **Karpathy LLM Wiki** (as proposed) | **Knowledge MEMO** |
|---|---|---|
| Maintenance cost goal | "Trend toward zero" | Knowledge must pass through the brain |
| LLM's role | Tireless knowledge engineer, compiler | A collaborator — but it cannot read *for* you |
| Template strategy | Universal idea file | Personal sample, fork required |
| Closed-loop endpoint | Compiled to wiki | Compiled to wiki **plus retained in your brain** |

---

## The four "intentionally different" points

These are the four places where Knowledge MEMO explicitly diverges from the "maintenance cost trends to zero" direction.

### ① Toolkit, not idea file

Karpathy's gist says: "in the agent era, you share ideas and let other people's agents build them." That's fine for what it is. But this repo exists because the author wanted to *actually hand you something you can install in 30 seconds*, not a prompt you feed to a coding agent and hope it gets right.

**One line of install, complete with SCHEMA.md + 6 skills + card templates + a demo gallery of real cards.** See [`../README.md`](../README.md) for the exact command.

### ② Human must stay in the loop — and this isn't just discipline, it's asset preservation

This is the most important divergence, and it deserves the most space.

Karpathy's framing contains an implicit question he doesn't directly answer: **for whom is the wiki being maintained?**

If the wiki is **context for the agent** — something the agent reads before acting, something the agent treats as its memory — then your accumulation will be wiped out the day the next-generation model ships. Context formats change. Memory mechanisms change. Retrieval patterns change. Today's hard-won wiki is tomorrow's stale data.

If the wiki is **a scaffold for your brain** — a structured path from curiosity to retention — then its value is permanent. The human brain updates its weights *much* more slowly than GPT updates its version number. What you loaded into your head in 2026 is still in your head in 2036.

**This is why Knowledge MEMO enforces "human in the loop"** through three hard disciplines:

- **No automated information flows.** No auto-ingest feeds, no scheduled scraping, no "fill my vault overnight" mode. You must browse, clip, and decide what to read yourself.
- **`/note` is interactive dual-proposal.** It doesn't auto-create cards. It proposes wikilinks and atomic cards, and the user confirms them. This intentionally adds friction.
- **Agents cannot independently rewrite the wiki.** All writes to `Cards/` go through `/note`'s dual-proposal channel. There's no API to bypass it.

None of these are performance optimizations. They're value choices. They exist specifically to prevent the repo from drifting toward "agent context accumulator".

> We're not against automation. We're against *accumulation for disposable consumers*.

### ③ Personal template, not universal product

See "Myth 2" above. The `demo/` gallery contains four cards from the author's life. They're there to show you what the system looks like in motion — not to tell you what your cards should look like.

### ④ The fourth operation: Retain

Karpathy lists three operations: Ingest, Query, Lint. All three are "make the wiki better".

But a beautifully compiled wiki you never remember is wasted effort. You'd need to re-derive the insight every time you want it.

Knowledge MEMO adds the fourth step: **Retain**. `/review` uses the FSRS-6 spaced repetition algorithm (the state-of-the-art open-source SRS, same as Anki's new default) to push knowledge from Obsidian into your brain. That's the only version of "knowledge" that doesn't depreciate when GPT-6 ships.

Karpathy didn't write this step, because it violates the "maintenance cost trends to zero" direction — spaced repetition is, by definition, maintenance cost. Only when you commit to "human must stay in the loop" does `Retain` naturally appear as a necessary operation.

---

## Why this might still be useful to you

You might agree with none of this and still find the repo useful as a reference:

- **As a working example**: see `phase-1-6-story.md` for how a small knowledge system ran for 6 months, hit scale problems, and was rebuilt.
- **As a copy-paste starting point**: fork the SCHEMA, change 80% of it, and you're ahead of "start from blank".
- **As a litmus test**: read this document and notice which of the four points you immediately disagree with. That's where *your* philosophy lives — and that's the first thing worth writing down in *your* version of this repo.

Or you might agree, and want the full argument. In that case the Chinese long-form essay《实现人的四个未来化之知识 memo 化》 is the place — it expands sections ② and ④ with case studies, a decade-scale time-horizon argument, and a reframing of "why do you want to learn something in the first place". See the main README for the link once it's published.

---

## Remember why you started

> Do you still remember why you began seeking knowledge in the first place?
>
> It wasn't so an agent could know things *for* you.
>
> It was because some questions, you wanted to understand yourself.
> It was because some things in the world, you wanted to be the person who knew them.
>
> That impulse is the starting point. Tools are just scaffolding.

Knowledge MEMO is scaffolding. Fork it and build yours.
