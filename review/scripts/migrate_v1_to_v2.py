#!/usr/bin/env python3
"""
Migrate v1 Knowledge MEMO atomic cards to v2 format.

v1: Atomic cards identified by `【】` in H1 title line
v2: Atomic cards identified by `type/atomic` tag in frontmatter

Usage:
    python3 migrate_v1_to_v2.py /path/to/your/obsidian/vault
    python3 migrate_v1_to_v2.py /path/to/vault --dry-run   # preview only

Behavior:
    1. Walk the vault recursively for .md files
    2. For each file:
        a. Parse frontmatter if present
        b. Check first H1 line: if it contains 【 and 】, mark atomic candidate
        c. If file already has type/atomic in tags: skip
        d. If no frontmatter: prepend minimal frontmatter with type/atomic
        e. If frontmatter exists but no tags: add tags field with type/atomic
        f. If frontmatter has block-style tags list: append type/atomic entry
        g. If frontmatter has inline-style tags [a, b]: append type/atomic
    3. Print per-file status and final summary.

Safety:
    - Idempotent: running twice adds nothing
    - Never touches the body (everything after the closing frontmatter fence)
    - stdlib only (no PyYAML dependency — matches fsrs_engine.py)
"""
import argparse
import os
import sys


# --------------------------------------------------------------------------
# Frontmatter helpers
# --------------------------------------------------------------------------

def split_frontmatter(content):
    """Split content into (fm_text, body).

    fm_text is the YAML text between the opening and closing `---` fences,
    NOT including the fences themselves. body is everything after the
    closing fence (including its trailing newline if any).

    Returns (None, content) if no frontmatter fence is found.
    """
    if not content.startswith("---\n") and not content.startswith("---\r\n"):
        return None, content
    # Find the closing fence (must be on its own line)
    lines = content.splitlines(keepends=True)
    if len(lines) < 2:
        return None, content
    # lines[0] is "---\n"
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            close_idx = i
            break
    if close_idx is None:
        return None, content
    fm_text = "".join(lines[1:close_idx])
    body = "".join(lines[close_idx + 1:])
    return fm_text, body


def h1_has_brackets(body):
    """Return True if the first H1 line (starting with '# ') contains 【】."""
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("# "):
            return "【" in stripped and "】" in stripped
        # Ignore blank lines before the H1; but stop at non-blank non-H1
        if stripped and not stripped.startswith("#"):
            return False
    return False


def fm_has_atomic_tag(fm_text):
    """Cheap check: does the frontmatter text already mention type/atomic?"""
    if fm_text is None:
        return False
    return "type/atomic" in fm_text


# --------------------------------------------------------------------------
# Tag insertion
# --------------------------------------------------------------------------

def insert_atomic_into_fm(fm_text):
    """Return a new fm_text with `type/atomic` added to tags.

    Handles three cases:
      (1) No `tags:` field at all → append `tags:\\n  - type/atomic` at end
      (2) Block-style tags:
            tags:
              - a
              - b
          → append `  - type/atomic` after the last tag item
      (3) Inline-style tags: `tags: [a, b]`
          → rewrite as `tags: [a, b, type/atomic]`
    """
    if fm_text is None:
        return "tags:\n  - type/atomic\n"

    lines = fm_text.splitlines(keepends=True)

    # Find a line that starts with "tags:" (allow leading spaces of 0)
    tags_line_idx = None
    for i, line in enumerate(lines):
        # match lines like "tags:" or "tags: [a, b]" at column 0
        stripped = line.lstrip()
        if stripped.startswith("tags:") and line.startswith("tags:"):
            tags_line_idx = i
            break

    if tags_line_idx is None:
        # Case (1): no tags field. Append.
        suffix = "" if fm_text.endswith("\n") else "\n"
        return fm_text + suffix + "tags:\n  - type/atomic\n"

    tags_line = lines[tags_line_idx]
    # Check if it's inline form: "tags: [a, b]" or "tags: []"
    after_colon = tags_line.split(":", 1)[1].strip().rstrip("\n").rstrip("\r")
    if after_colon.startswith("[") and after_colon.endswith("]"):
        # Case (3): inline form
        inner = after_colon[1:-1].strip()
        if inner:
            new_inner = inner + ", type/atomic"
        else:
            new_inner = "type/atomic"
        # Preserve line ending of the original tags_line
        newline = "\n"
        if tags_line.endswith("\r\n"):
            newline = "\r\n"
        lines[tags_line_idx] = f"tags: [{new_inner}]{newline}"
        return "".join(lines)

    # Case (2): block form. Find last contiguous "  - ..." item after tags:
    insert_at = tags_line_idx + 1
    last_item_idx = None
    for j in range(tags_line_idx + 1, len(lines)):
        if lines[j].lstrip().startswith("- "):
            last_item_idx = j
        elif lines[j].strip() == "":
            # Blank line inside frontmatter — keep scanning just in case
            continue
        else:
            break
    if last_item_idx is not None:
        insert_at = last_item_idx + 1

    # Detect indentation used for existing items, default "  "
    indent = "  "
    if last_item_idx is not None:
        leading = lines[last_item_idx]
        indent = leading[: len(leading) - len(leading.lstrip())]
        if not indent:
            indent = "  "

    new_item = f"{indent}- type/atomic\n"
    new_lines = lines[:insert_at] + [new_item] + lines[insert_at:]
    return "".join(new_lines)


# --------------------------------------------------------------------------
# Main migration
# --------------------------------------------------------------------------

def migrate_file(path, dry_run=False):
    """Return one of 'modified', 'skipped', 'nomatch'."""
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()

    fm_text, body = split_frontmatter(content)

    if not h1_has_brackets(body):
        return "nomatch"

    if fm_has_atomic_tag(fm_text):
        return "skipped"

    new_fm_text = insert_atomic_into_fm(fm_text)
    new_content = f"---\n{new_fm_text}"
    if not new_fm_text.endswith("\n"):
        new_content += "\n"
    new_content += "---\n" + body

    if dry_run:
        print(f"[DRY-RUN] Would modify: {path}")
    else:
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(new_content)
        print(f"[MODIFIED] {path}")

    return "modified"


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Migrate v1 Knowledge MEMO atomic cards (【】-in-H1) to v2 "
            "format (type/atomic tag)."
        )
    )
    parser.add_argument(
        "vault_path",
        help="Path to the root of your Obsidian vault",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing any files",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.vault_path):
        print(
            f"Error: vault_path '{args.vault_path}' is not a directory",
            file=sys.stderr,
        )
        sys.exit(2)

    counters = {"modified": 0, "skipped": 0, "nomatch": 0}

    for root, dirs, files in os.walk(args.vault_path):
        # Skip common hidden / non-content dirs
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            try:
                result = migrate_file(path, dry_run=args.dry_run)
            except Exception as e:
                print(f"[ERROR] {path}: {e}", file=sys.stderr)
                continue
            counters[result] += 1

    print()
    print("Summary:")
    print(f"  Modified: {counters['modified']}")
    print(f"  Skipped (already has type/atomic): {counters['skipped']}")
    print(f"  No match (H1 no 【】): {counters['nomatch']}")


if __name__ == "__main__":
    main()
