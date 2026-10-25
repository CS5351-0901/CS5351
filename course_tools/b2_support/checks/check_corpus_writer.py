#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Self-checks for the corpus writer (writes only to temp dirs)."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SUPPORT_DIR = Path(__file__).resolve().parents[1]
if str(SUPPORT_DIR) not in sys.path:
    sys.path.insert(0, str(SUPPORT_DIR))

from corpus_writer import OutputExistsError, write_corpus


class CheckCorpusWriterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_jsonl_write(self):
        recs = [{"a": 1}, {"b": "x"}]
        out = self.dir / "c.jsonl"
        manifest = write_corpus(out, recs, fmt="jsonl")
        self.assertTrue(out.exists())
        lines = out.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        self.assertEqual(manifest["record_count"], 2)
        self.assertEqual(manifest["format"], "jsonl")

    def test_json_write(self):
        recs = [{"a": 1}, {"b": "x"}]
        out = self.dir / "c.json"
        write_corpus(out, recs, fmt="json")
        loaded = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(loaded, recs)

    def test_text_write(self):
        recs = [{"a": 1}, {"b": "x"}]
        out = self.dir / "c.txt"
        write_corpus(out, recs, fmt="text")
        text = out.read_text(encoding="utf-8")
        self.assertIn("'a': 1", text)

    def test_overwrite_disabled_by_default(self):
        recs = [{"a": 1}]
        out = self.dir / "exists.jsonl"
        write_corpus(out, recs, fmt="jsonl")
        with self.assertRaises(OutputExistsError):
            write_corpus(out, [{"z": 9}], fmt="jsonl")

    def test_overwrite_when_enabled(self):
        out = self.dir / "over.jsonl"
        write_corpus(out, [{"a": 1}], fmt="jsonl")
        write_corpus(out, [{"z": 9}], fmt="jsonl", overwrite=True)
        lines = out.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)

    def test_manifest_is_deterministic(self):
        recs = [{"a": 1}, {"b": 2}]
        out = self.dir / "det.jsonl"
        m1 = write_corpus(out, recs, fmt="jsonl")
        out2 = self.dir / "det2.jsonl"
        m2 = write_corpus(out2, recs, fmt="jsonl")
        # sha256 depends only on content/format, not on the output filename.
        self.assertEqual(m1["sha256"], m2["sha256"])
        self.assertEqual(m1["record_count"], m2["record_count"])

    def test_unknown_format_raises(self):
        with self.assertRaises(ValueError):
            write_corpus(self.dir / "x.bin", [{"a": 1}], fmt="bin")

    def test_writes_nothing_outside_output_dir(self):
        # Corpus writes must stay inside the explicitly given output path.
        base = set(os.listdir(self.dir))
        write_corpus(self.dir / "only.jsonl", [{"a": 1}], fmt="jsonl")
        self.assertIn("only.jsonl", os.listdir(self.dir))
        # No extra files beyond the single output.
        self.assertEqual(set(os.listdir(self.dir)), base | {"only.jsonl"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
