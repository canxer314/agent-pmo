#!/usr/bin/env python3
"""
Unit tests for migrate_v1_to_v2.py.

Covers the four frontmatter forms the migrator must handle:
    1. No tags field
    2. Scalar form:  tags: domain/test
    3. Inline form:  tags: [a, b]
    4. Block form:   tags:\n  - a\n  - b

Also covers idempotency via migrate_file on a temp file.

stdlib only to match the migrator itself.
"""
import os
import sys
import tempfile
import textwrap
import unittest

# Make the script importable regardless of cwd.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import migrate_v1_to_v2 as m  # noqa: E402


def _round_trip_frontmatter(fm_text):
    """Rebuild a full file from an fm_text and parse it back.

    Returns the list of non-empty lines between the --- fences so tests can
    assert on structure without depending on a YAML library.
    """
    full = "---\n" + fm_text
    if not fm_text.endswith("\n"):
        full += "\n"
    full += "---\n# 【placeholder】\n"
    fm, _body = m.split_frontmatter(full)
    return [ln for ln in (fm or "").splitlines() if ln.strip()]


class InsertAtomicTests(unittest.TestCase):
    """Unit tests for insert_atomic_into_fm."""

    def test_none_frontmatter(self):
        out = m.insert_atomic_into_fm(None)
        self.assertEqual(out, "tags:\n  - type/atomic\n")

    def test_no_tags_field(self):
        fm_in = "date: 2026-04-11\nauthor: Owen\n"
        out = m.insert_atomic_into_fm(fm_in)
        # Existing fields must be preserved verbatim.
        self.assertIn("date: 2026-04-11\n", out)
        self.assertIn("author: Owen\n", out)
        self.assertIn("tags:\n  - type/atomic\n", out)

    def test_inline_form_with_items(self):
        fm_in = "tags: [domain/neuro, category/card]\n"
        out = m.insert_atomic_into_fm(fm_in)
        self.assertEqual(
            out,
            "tags: [domain/neuro, category/card, type/atomic]\n",
        )

    def test_inline_form_empty(self):
        fm_in = "tags: []\n"
        out = m.insert_atomic_into_fm(fm_in)
        self.assertEqual(out, "tags: [type/atomic]\n")

    def test_block_form_with_items(self):
        fm_in = "tags:\n  - domain/neuro\n  - category/card\n"
        out = m.insert_atomic_into_fm(fm_in)
        self.assertEqual(
            out,
            "tags:\n  - domain/neuro\n  - category/card\n  - type/atomic\n",
        )

    def test_block_form_preserves_trailing_fields(self):
        fm_in = "tags:\n  - domain/neuro\ndate: 2026-04-11\n"
        out = m.insert_atomic_into_fm(fm_in)
        self.assertEqual(
            out,
            "tags:\n  - domain/neuro\n  - type/atomic\ndate: 2026-04-11\n",
        )

    # ------------------------------------------------------------------
    # Scalar form — the P1 regression this test file exists to pin down.
    # ------------------------------------------------------------------
    def test_scalar_form_single_value(self):
        """`tags: domain/test` must become a valid block list, not corrupted YAML."""
        fm_in = "tags: domain/test\n"
        out = m.insert_atomic_into_fm(fm_in)
        # The original scalar value must survive AND type/atomic must be added.
        self.assertIn("domain/test", out)
        self.assertIn("type/atomic", out)
        # The output must NOT be the broken shape:
        #   tags: domain/test
        #     - type/atomic
        # i.e. a scalar followed by an orphan sequence item.
        self.assertNotRegex(
            out,
            r"tags:\s*domain/test\s*\n\s+-\s+type/atomic",
            "scalar form was not converted to a proper list — YAML is invalid",
        )
        # Round-trip: rebuild file, parse frontmatter back, check structure.
        lines = _round_trip_frontmatter(out)
        # Expect exactly: "tags:", "- domain/test", "- type/atomic" (any indent)
        self.assertEqual(lines[0].strip(), "tags:")
        item_lines = [ln.strip() for ln in lines[1:]]
        self.assertIn("- domain/test", item_lines)
        self.assertIn("- type/atomic", item_lines)

    def test_scalar_form_preserves_trailing_fields(self):
        fm_in = "tags: domain/test\ndate: 2026-04-11\n"
        out = m.insert_atomic_into_fm(fm_in)
        self.assertIn("date: 2026-04-11\n", out)
        self.assertIn("domain/test", out)
        self.assertIn("type/atomic", out)
        # date field must still parse as its own line, not get absorbed.
        self.assertRegex(out, r"(?m)^date: 2026-04-11$")


class MigrateFileIntegrationTests(unittest.TestCase):
    """Integration tests through migrate_file + round-trip idempotency."""

    def _write(self, content):
        fd, path = tempfile.mkstemp(suffix=".md")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(content)
        return path

    def _read(self, path):
        with open(path, "r", encoding="utf-8") as fp:
            return fp.read()

    def test_scalar_form_end_to_end_and_idempotent(self):
        src = textwrap.dedent(
            """\
            ---
            tags: domain/test
            date: 2026-04-11
            ---
            # 【测试概念】原子卡片

            Body content.
            """
        )
        path = self._write(src)
        try:
            result1 = m.migrate_file(path)
            self.assertEqual(result1, "modified")

            after = self._read(path)
            # The frontmatter must still have a closing fence on its own line,
            # followed by the unchanged body.
            self.assertIn("---\n# 【测试概念】原子卡片", after)
            self.assertIn("Body content.", after)
            # type/atomic must be present.
            self.assertIn("type/atomic", after)
            # Original scalar value must still be there in some form.
            self.assertIn("domain/test", after)

            # Running again must be a no-op (idempotency guard).
            result2 = m.migrate_file(path)
            self.assertEqual(result2, "skipped")
            after2 = self._read(path)
            self.assertEqual(after, after2)
        finally:
            os.unlink(path)

    def test_no_frontmatter_card_with_brackets(self):
        src = "# 【裸卡】\n\nNo frontmatter at all.\n"
        path = self._write(src)
        try:
            result = m.migrate_file(path)
            self.assertEqual(result, "modified")
            after = self._read(path)
            self.assertTrue(after.startswith("---\n"))
            self.assertIn("type/atomic", after)
            self.assertIn("# 【裸卡】", after)
        finally:
            os.unlink(path)

    def test_non_atomic_card_untouched(self):
        src = "# Normal Heading\n\nJust a regular note.\n"
        path = self._write(src)
        try:
            before = self._read(path)
            result = m.migrate_file(path)
            self.assertEqual(result, "nomatch")
            after = self._read(path)
            self.assertEqual(before, after)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
