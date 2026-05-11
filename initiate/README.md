# /note — Atomic Knowledge Capture

Turn a Claude Code or Codex conversation into durable Obsidian cards.

## What It Does

When you run `/note` in Claude Code, or explicitly invoke `$note` in Codex, the skill:

1. **Scans the conversation** — identifies the research arc, key findings, and reusable knowledge points
2. **Drafts a Research Summary** — a narrative "map" card that preserves the reasoning chain
3. **Proposes wikilinks** — suggests where the new summary should link to existing cards
4. **Proposes Atomic Cards** — suggests standalone "stone" cards for concepts worth retaining
5. **Writes only approved cards** — saves the summary and any accepted atomic cards to Obsidian through the `/note` dual-proposal flow

`/note` is the vault's only write path. Upstream skills like `/read` and `/insights` generate analysis in the conversation; `/note` is where persistence happens.

## Usage

**Claude Code**

```text
/note                    # save everything from this conversation
/note --topic=dopamine   # limit to a specific topic
/note --scope=last       # only the most recent discussion
```

**Codex**

```text
$note                    # save everything from this conversation
$note --topic=dopamine   # limit to a specific topic
$note --scope=last       # only the most recent discussion
```

## Output Format

### Research Summary (Map)

```markdown
# [Topic] — 研究摘要

> 日期：2026-01-15 | 来源：article analysis

## 研究背景
...

## 核心发现
### [Sub-topic]
...

## 关键结论
1. ...

## 延伸问题
...
```

### Atomic Card (Stone)

```markdown
---
tags:
  - type/atomic
  - domain/neuroscience
date: 2026-01-15
---

# 【Dopamine】encodes motivation, not pleasure

Wolfram Schultz's landmark experiments showed that dopamine neurons fire in
anticipation of reward, not at reward delivery...
```

## Why Map + Stones?

- **Map alone**: you can navigate, but you can't build — too dense to review
- **Stones alone**: you have facts, but no context — you don't know why they matter
- **Map + Stones**: the summary explains why each stone is important; the stones become searchable and reviewable

The `/review` skill reads stones, not maps — this is intentional.

## Dual-Proposal Flow

`/note` does not silently dump cards into your vault.

It proposes two things separately:

1. **Wikilinks** — which existing cards should be linked instead of creating duplicates
2. **Atomic cards** — which new concepts are worth promoting into standalone reviewable cards

You confirm what gets written. This is the human-in-the-loop checkpoint that keeps the vault aligned with your own knowledge graph.

## Linking Convention

- `【Key Term】` — marks concepts that may deserve their own atomic cards
- `**bold**` — marks core conclusions within a card
- Combined: `**【extinction learning】is the neuroscientific basis of memory reconsolidation**`

These markers help `/note` surface good card candidates, but `/review` ultimately discovers cards via the `type/atomic` tag.

## Integration with `/review`

Accepted atomic cards are written with the `type/atomic` tag. `/review` scans Obsidian for that tag and registers those cards into FSRS.

As long as the accepted card lands in Obsidian with `type/atomic`, `/review` will find and schedule it.

## Requirements

- Claude Code or Codex
- Obsidian 1.12.4+ (CLI preferred, MCP fallback is fine)
- To use a different knowledge backend, see [CONTRIBUTING.md](../CONTRIBUTING.md)
