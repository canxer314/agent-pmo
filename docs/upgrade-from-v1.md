# Upgrading from v1 to v2

> **TL;DR**: Run the migration script first, then copy the new skills into your agent runtime.
>
> ```bash
> python3 review/scripts/migrate_v1_to_v2.py /path/to/your/obsidian/vault
>
> # Claude Code
> cp -r read insights note review query lint "$HOME/.claude/skills/"
>
> # Codex
> cp -r read insights note review query lint "$HOME/.agents/skills/"
>
> cp SCHEMA.md AGENTS.md /path/to/your/vault/
> ```

---

## What changed in v2

### Breaking changes

1. **`/review` identification**
   - v1: atomic cards identified by `【】` in H1 title line
   - v2: atomic cards identified by `type/atomic` tag in frontmatter
   - **Impact**: Your v1 cards will silently disappear from `/review` until you migrate. The cards themselves are untouched — only `/review` no longer sees them.

2. **`/note` workflow**
   - v1: auto-creates atomic cards from extracted key points
   - v2: **dual-proposal** — proposes wikilinks and atomic cards for you to confirm interactively
   - **Impact**: `/note` is now more chatty. This is intentional — "human must stay in the loop" is a core v2 principle (see [`docs/philosophy.md`](./philosophy.md)).

### Additions

- **`SCHEMA.md`** + **`AGENTS.md`** — new schema/rules layer (aligned with Karpathy LLM Wiki)
- **`/query`** — new skill to query vault knowledge via MOC + keyword search
- **`/lint`** — new skill for vault health checks (broken links / orphans / gaps)
- **Card templates** (`templates/cards/*.md`) — 8 minimal templates with fork-me disclaimers
- **MOC template** (`templates/moc/domain-moc.md`)
- **Demo gallery** (`demo/`) — author's real vault samples across neuroscience / investing / consciousness / molecular biology

---

## Migration steps

### 1. Run the migration script (MOST IMPORTANT)

This is the only breaking-change fix. **Do it before upgrading the `/review` skill**, otherwise your v1 cards become invisible to `/review`.

```bash
cd knowledge-mgmt

# Preview first — shows what would change without writing anything
python3 review/scripts/migrate_v1_to_v2.py /path/to/your/obsidian/vault --dry-run

# Real run
python3 review/scripts/migrate_v1_to_v2.py /path/to/your/obsidian/vault
```

**What it does**:
- Walks your vault recursively, finds all `.md` files
- For each file whose first H1 line contains `【】`, adds `type/atomic` to its frontmatter tags
- Handles 3 edge cases: no frontmatter, frontmatter without `tags` field, inline-style `tags: [a, b]`
- **Idempotent**: running twice adds nothing
- **Never touches card body** — only the frontmatter region

**Safety notes**:
- Use `--dry-run` first. Read the output before committing.
- If your vault is under git, commit clean state first so you can easily diff or rollback.
- The script is stdlib-only Python (no PyYAML) — the same philosophy as `fsrs_engine.py`.

### 2. Install v2 skills

**Claude Code**

```bash
cp -r read insights note review query lint "$HOME/.claude/skills/"
```

**Codex**

```bash
cp -r read insights note review query lint "$HOME/.agents/skills/"
```

Note: v2 adds two new skill directories (`query`, `lint`). You may want to back up your skill directory first if you have custom modifications.

### 3. Install SCHEMA and AGENTS at your vault root

```bash
cp SCHEMA.md AGENTS.md /path/to/your/obsidian/vault/
```

If you use **Claude Code**, also add a small `CLAUDE.md` bridge so the same vault rules are visible there:

```bash
cat > /path/to/your/obsidian/vault/CLAUDE.md <<'EOF'
Read AGENTS.md before operating this vault.
EOF
```

If you use **Codex**, launch it from your vault root (or a subdirectory inside that vault) so the copied `AGENTS.md` is visible to the runtime.

**Then customize them** for your domain. The author's versions are samples from neuroscience / investing / consciousness / molecular biology. You almost certainly need different Card types, a different tag scheme, or a different permission matrix. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) § "Fork, Don't Consume".

### 4. (Optional) Install templates

```bash
cp -r templates /path/to/your/obsidian/vault/
```

Templates are reference — not authority. Expect to rewrite them to match how you actually think.

### 5. (Optional) Configure state file path

By default, `/review` stores FSRS state next to the installed skill:

- Claude Code: `~/.claude/skills/review/review_state.json`
- Codex: `~/.agents/skills/review/review_state.json`

If you want to put it elsewhere (e.g., in a cloud-synced directory to share across machines), export the env var:

```bash
# Add to your shell profile (.zshrc / .bashrc)
export KM_REVIEW_STATE_PATH="$HOME/Dropbox/km/review_state.json"
```

All `/review` calls will use that path automatically.

### 6. Verify

Run a scan to confirm your old cards are detected:

**Claude Code**

```
/review --mode=scan
```

**Codex**

```
$review --mode=scan
```

You should see your migrated cards being registered into FSRS. If the count is zero or much lower than expected, the migration didn't reach them — rerun with `--dry-run` on your vault to see which files were skipped.

---

## Rollback

If anything breaks, every v1 file is still at the `v1.0.0` git tag:

```bash
# Clone a fresh copy of v1 into a separate directory
git clone --branch v1.0.0 https://github.com/owenliang60-ship-it/knowledge-mgmt.git ~/knowledge-mgmt-v1

# Claude Code
cp -r ~/knowledge-mgmt-v1/{read,insights,note,review} "$HOME/.claude/skills/"

# Codex
cp -r ~/knowledge-mgmt-v1/{read,insights,note,review} "$HOME/.agents/skills/"
```

Note that v2 added `query/` and `lint/` — after rollback you won't have them, but the 4 original skills go back to v1 behavior exactly.

Your vault itself is unchanged by rollback. The migration script only added frontmatter tags; those tags are harmless when `/review` (v1) doesn't look at them.

---

## Support

Open an issue: https://github.com/owenliang60-ship-it/knowledge-mgmt/issues

Please include:
- Which step failed
- The exact command you ran
- Output of `python3 --version` and the dry-run summary
- A fixture file demonstrating the problem (if possible, redact private content)
