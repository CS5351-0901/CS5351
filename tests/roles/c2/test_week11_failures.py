"""Week 11: cleanup of reserved/partial archives on packaging failures."""
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest
import zipfile

import test_week10_lifecycle as lifecycle
packager = lifecycle.packager


class ArchiveFailureContracts(lifecycle.LifecycleFixture):
    def assert_only_sentinel(self):
        self.assertEqual({p.name for p in self.output.iterdir()}, {"unrelated.zip"})
        self.assertEqual((self.output / "unrelated.zip").read_bytes(), b"keep me")

    def sentinel(self):
        (self.output / "unrelated.zip").write_bytes(b"keep me")

    def test_second_zip_write_failure_removes_partial_only(self):
        self.sentinel()
        original = zipfile.ZipFile.write
        calls = []
        def fail_second(archive, *args, **kwargs):
            calls.append(archive.filename)
            if len(calls) == 2:
                raise OSError("second archive write failed")
            return original(archive, *args, **kwargs)
        with patch.object(zipfile.ZipFile, "write", new=fail_second):
            result = self.subject.pack(self.files("value"), name="demo")
        self.assertEqual(len(calls), 2)
        self.assert_failure(result)
        self.assertIn("second archive write failed", result["error"])
        self.assert_only_sentinel()

    def test_zip_open_failure_removes_reserved_file(self):
        self.sentinel()
        with patch.object(packager.zipfile, "ZipFile", side_effect=OSError("archive open failed")):
            result = self.subject.pack(self.files("value"), name="demo")
        self.assert_failure(result)
        self.assertIn("archive open failed", result["error"])
        self.assert_only_sentinel()

    def test_size_read_failure_removes_unreported_archive(self):
        self.sentinel()
        original = Path.stat
        def fail_archive_stat(path, *args, **kwargs):
            if path.parent == self.output and path.name != "unrelated.zip":
                raise OSError("archive size unavailable")
            return original(path, *args, **kwargs)
        with patch.object(Path, "stat", new=fail_archive_stat):
            result = self.subject.pack(self.files("value"), name="demo")
        self.assert_failure(result)
        self.assertIn("archive size unavailable", result["error"])
        self.assert_only_sentinel()

    def test_output_reservation_failure_preserves_existing_files(self):
        self.sentinel()
        with patch.object(tempfile, "NamedTemporaryFile", side_effect=OSError("output unavailable")):
            result = self.subject.pack(self.files("value"), name="demo")
        self.assert_failure(result)
        self.assertIn("output unavailable", result["error"])
        self.assert_only_sentinel()

    def test_cleanup_denial_reports_both_errors(self):
        original = Path.unlink
        def deny_archive_unlink(path, *args, **kwargs):
            if path.parent == self.output and path.suffix == ".zip":
                raise PermissionError("cleanup denied")
            return original(path, *args, **kwargs)
        with patch.object(zipfile.ZipFile, "write", side_effect=OSError("archive write failed")):
            with patch.object(Path, "unlink", new=deny_archive_unlink):
                result = self.subject.pack(self.files("value"), name="demo")
        self.assert_failure(result)
        self.assertIn("archive write failed", result["error"])
        self.assertIn("archive cleanup failed", result["error"])
        self.assertIn("cleanup denied", result["error"])
        self.assertEqual(len(list(self.output.iterdir())), 1)

    def test_retry_after_failed_write_keeps_only_successful_delivery(self):
        with patch.object(zipfile.ZipFile, "write", side_effect=OSError("transient write error")):
            failed = self.subject.pack(self.files("bad"), name="demo")
        self.assert_failure(failed)
        self.assertEqual(list(self.output.iterdir()), [])
        recovered = self.subject.pack(self.files("good"), name="demo")
        self.assert_archive(recovered, "good")
        self.assertEqual(len(list(self.output.iterdir())), 1)
        self.assertEqual(list(self.scratch.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
