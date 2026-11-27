"""Real filesystem checks for independent packaging attempts."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import zipfile

import test_baseline as baseline
packager = baseline.packager


class LifecycleFixture(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="c2-lifecycle-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.scratch = self.root / "scratch"
        self.scratch.mkdir()
        self.output = self.root / "archive"
        self.subject = packager.ProjectPackager(str(self.output))
        local_temp = patch.object(tempfile, "tempdir", str(self.scratch))
        local_temp.start()
        self.addCleanup(local_temp.stop)
        clock = patch.object(packager, "datetime")
        self.clock = clock.start()
        self.clock.now.return_value = datetime(2026, 1, 1, 0, 0, 0)
        self.addCleanup(clock.stop)

    def files(self, value):
        return [{"name": "main.py", "content": "VALUE = " + repr(value) + "\n"}]

    def assert_archive(self, result, value):
        self.assertTrue(result["success"], result["error"])
        self.assertIsNone(result["error"])
        path = Path(result["zip_path"])
        self.assertEqual(path.parent, self.output)
        self.assertEqual(result["size"], path.stat().st_size)
        with zipfile.ZipFile(path) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(result["file_count"], len(archive.infolist()))
            content = archive.read("demo/src/main.py").decode().replace("\r\n", "\n")
            self.assertEqual(content, self.files(value)[0]["content"])

    def assert_failure(self, result):
        self.assertFalse(result["success"])
        self.assertTrue(result["error"])
        self.assertEqual(result["zip_path"], "")
        self.assertEqual(result["file_count"], 0)
        self.assertEqual(result["size"], 0)
        self.assertEqual(list(self.scratch.iterdir()), [])


class IndependentAttempts(LifecycleFixture):
    def test_same_second_same_name_preserves_both_archives(self):
        first = self.subject.pack(self.files("first"), name="demo")
        self.assert_archive(first, "first")
        original = Path(first["zip_path"]).read_bytes()
        second = self.subject.pack(self.files("second"), name="demo")
        self.assertNotEqual(first["zip_path"], second["zip_path"])
        self.assertEqual(Path(first["zip_path"]).read_bytes(), original)
        self.assert_archive(first, "first")
        self.assert_archive(second, "second")
        self.assertEqual(len(list(self.output.iterdir())), 2)
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_preexisting_timestamp_archive_is_not_overwritten(self):
        existing = self.output / "demo_20260101_000000.zip"
        existing.write_bytes(b"existing delivery")
        result = self.subject.pack(self.files("new"), name="demo")
        self.assertEqual(existing.read_bytes(), b"existing delivery")
        self.assert_archive(result, "new")
        self.assertNotEqual(Path(result["zip_path"]), existing)

    def test_concurrent_same_name_attempts_keep_separate_contents(self):
        barrier = threading.Barrier(2)
        original = packager.ReadmeGenerator.generate
        def synchronized_readme(project):
            barrier.wait(timeout=10)
            return original(project)
        with patch.object(packager.ReadmeGenerator, "generate", side_effect=synchronized_readme):
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(self.subject.pack, self.files(v), name="demo")
                           for v in ("one", "two")]
                results = [f.result(timeout=20) for f in futures]
        for result, value in zip(results, ("one", "two")):
            self.assert_archive(result, value)
        self.assertNotEqual(results[0]["zip_path"], results[1]["zip_path"])
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_staging_uses_configured_temp_and_unique_directories(self):
        observed = []
        cleanup = self.subject._cleanup_temp_files
        def record(project_dir):
            observed.append(project_dir.parent)
            self.assertEqual(project_dir.parent.parent, self.scratch)
            cleanup(project_dir)
        with patch.object(self.subject, "_cleanup_temp_files", side_effect=record):
            for value in ("one", "two"):
                self.assert_archive(self.subject.pack(self.files(value), name="demo"), value)
        self.assertEqual(len(set(observed)), 2)
        self.assertTrue(all(not path.exists() for path in observed))

    def test_temp_allocation_failure_returns_structured_failure(self):
        with patch.object(tempfile, "mkdtemp", side_effect=OSError("scratch unavailable")):
            result = self.subject.pack(self.files("value"), name="demo")
        self.assert_failure(result)
        self.assertIn("scratch unavailable", result["error"])
        self.assertEqual(list(self.output.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
