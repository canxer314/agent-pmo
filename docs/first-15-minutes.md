# First 15 Minutes

> Goal: from “I just cloned this repo” to “I saw one real card land in my vault and can query it back”.

This walkthrough is written for both **Claude Code** and **Codex**. It assumes:

- you already use Obsidian
- you can open a Claude Code or Codex session
- you want the **fastest first success**, not a perfect setup

The fastest path is: **analyze one short source -> run `/note` or `$note` -> confirm 1-2 cards -> query them back**.

Claude Code examples below use `/skill`. Codex examples use explicit `$skill` invocation.

---

## Minute 0-3: Install into your agent runtime

Clone:

```bash
git clone https://github.com/owenliang60-ship-it/knowledge-mgmt.git
cd knowledge-mgmt
```

Install skills into **one** runtime:

**Claude Code**

```bash
mkdir -p "$HOME/.claude/skills"
cp -r read insights note review query lint "$HOME/.claude/skills/"
```

**Codex**

```bash
mkdir -p "$HOME/.agents/skills"
cp -r read insights note review query lint "$HOME/.agents/skills/"
```

Install the shared vault rules:

```bash
cp SCHEMA.md AGENTS.md /path/to/your/obsidian/vault/
mkdir -p /path/to/your/obsidian/vault/{Cards,Clippings,Journal}
```

If you use **Claude Code**, add a tiny bridge file so the same vault rules are visible there too:

```bash
cat > /path/to/your/obsidian/vault/CLAUDE.md <<'EOF'
Read AGENTS.md before operating this vault.
EOF
```

If you use **Codex**, start the session from your vault root (or a subdirectory inside it) so `AGENTS.md` is visible.

If you want templates on day one:

```bash
cp -r templates /path/to/your/obsidian/vault/
```

---

## Minute 3-5: Verify Obsidian is reachable

Open your vault in Obsidian.

Then verify the CLI works:

```bash
obsidian vault
```

If that command cannot reach the app, fix that first. Knowledge MEMO is usable with MCP fallback, but your first run will be much smoother if the Obsidian CLI is already working.

---

## Minute 5-8: Choose the easiest possible source

Do **not** start with a 40-page PDF.

Pick one of these:

- a 500-1500 word article URL
- a pasted excerpt from an essay, memo, or blog post
- a short markdown note you already care about

Rule of thumb:

- use `/insights` for business, strategy, investing, product, or market content
- use `/read` for papers, theory, research, or dense explanatory writing

Examples:

**Claude Code**

```text
/insights https://example.com/article
```

```text
/read /absolute/path/to/paper.pdf
```

**Codex**

```text
$insights https://example.com/article
```

```text
$read /absolute/path/to/paper.pdf
```

Or just paste a short text block and explicitly invoke the skill:

```text
$insights
```

Success at this step means: the agent gives you a structured analysis that feels worth keeping.

---

## Minute 8-12: Turn the conversation into cards

As soon as the analysis looks useful, say:

**Claude Code**

```text
/note
```

**Codex**

```text
$note
```

`/note` or `$note` will do two things:

1. draft a summary card
2. propose wikilinks and atomic cards for you to confirm

For the first run, keep it simple:

- accept the summary card
- accept **1-2 atomic cards**, not 10
- if there are no existing cards yet, it is fine to skip most wikilinks

Success at this step means: at least one summary card and one atomic card are written into `Cards/`.

---

## Minute 12-15: Verify retrieval and retention

Now immediately test the loop.

### A. Query it back

Ask:

**Claude Code**

```text
/query "what do I know about <your topic>?"
```

**Codex**

```text
$query "what do I know about <your topic>?"
```

Success means the answer cites the card(s) you just wrote.

### B. Register the atomic card into review

Ask:

**Claude Code**

```text
/review --mode=scan
```

**Codex**

```text
$review --mode=scan
```

If you created an atomic card with `type/atomic`, `/review` or `$review` should discover it.

You do **not** need a full spaced-repetition session on day one. The goal is only to confirm that the retain loop is connected.

---

## What success looks like

At the end of 15 minutes, you should have all of this:

- `SCHEMA.md` and `AGENTS.md` in your vault root
- at least 1 new card in `Cards/`
- at least 1 `type/atomic` card if you accepted an atomic proposal
- `/query` able to answer from that card
- `/review --mode=scan` able to see the new atomic card

If you got those five things, the system is live.

---

## Common first-run mistakes

- **Starting with a huge source**: use a short article first
- **Trying to perfect SCHEMA before first use**: keep the author's sample for one run, then fork
- **Skipping `/note` / `$note`**: `/read` and `/insights` are conversational; persistence happens through the note skill
- **Expecting a universal template**: this repo is a sample system, not a finished product
- **Debugging `/review` before you have any `type/atomic` cards**: make one atomic card first

---

## What to do next

After your first success:

1. replace the demo domains with your own
2. edit `SCHEMA.md` section 2 to match your actual card types
3. rewrite the templates you dislike
4. run the loop for a week before making bigger architectural changes

If you are migrating from an older setup, continue with [`upgrade-from-v1.md`](./upgrade-from-v1.md).
