"""Executable C1 baseline for the owned debug and snapshot helpers."""

import importlib.util
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def load_main_without_astrbot_runtime():
    """Import production helpers without initializing the AstrBot plugin."""
    astrbot = types.ModuleType("astrbot")
    astrbot.__path__ = []
    api = types.ModuleType("astrbot.api")
    api.__path__ = []
    event = types.ModuleType("astrbot.api.event")
    event.filter = SimpleNamespace(command=lambda *_args, **_kwargs: lambda fn: fn)
    event.AstrMessageEvent = type("AstrMessageEvent", (), {})
    star = types.ModuleType("astrbot.api.star")
    star.Context = type("Context", (), {})
    star.Star = type("Star", (), {"__init__": lambda self, context: None})
    api.logger = SimpleNamespace()
    api.AstrBotConfig = type("AstrBotConfig", (), {})

    stubs = {
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event,
        "astrbot.api.star": star,
    }
    with mock.patch.dict(sys.modules, stubs):
        spec = importlib.util.spec_from_file_location(
            "_c1_week05_main", REPOSITORY_ROOT / "main.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


MAIN = load_main_without_astrbot_runtime()


class C1BaselineTests(unittest.TestCase):
    def setUp(self):
        self.plugin = object.__new__(MAIN.CodeAgentPlugin)

    def test_analyze_error_extracts_type_line_and_message(self):
        stderr = 'Traceback:\n  File "app.py", line 7, in main\nNameError: name \'item\' is not defined'

        result = self.plugin._analyze_error(stderr)

        self.assertEqual(result["error_type"], "NameError")
        self.assertEqual(result["error_line"], 0)
        self.assertEqual(result["error_message"], stderr)

    def test_analyze_error_keeps_unknown_fallback_and_truncates_message(self):
        result = self.plugin._analyze_error("x" * 600)

        self.assertEqual(result["error_type"], "Unknown")
        self.assertEqual(result["error_line"], 0)
        self.assertEqual(len(result["error_message"]), 500)

    def test_generate_debug_fix_for_import_and_name_errors(self):
        cases = [
            ({"error_type": "ModuleNotFoundError", "error_message": "No module named 'widget'"},
             "在 requirements.txt 中添加 widget"),
            ({"error_type": "NameError", "error_message": "name 'item' is not defined"},
             "定义或导入 item"),
        ]
        for error, expected in cases:
            with self.subTest(error=error["error_type"]):
                self.assertEqual(self.plugin._generate_debug_fix(error), expected)

    def test_generate_debug_fix_falls_back_for_unrecognized_error(self):
        self.assertEqual(
            self.plugin._generate_debug_fix({"error_type": "RuntimeError", "error_message": "oops"}),
            "检查运行时错误: RuntimeError",
        )

    def test_snapshot_round_trip_and_latest_selection(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.plugin.workspace = Path(temp_dir)
            with mock.patch.object(MAIN.time, "time", side_effect=[1000, 1001]):
                first = Path(self.plugin._save_snapshot("session", "core_complete", "old", []))
            with mock.patch.object(MAIN.time, "time", side_effect=[2000, 2001]):
                second = Path(self.plugin._save_snapshot(
                    "session", "core_complete", "new", [{"name": "main.py"}]
                ))
            os.utime(first, (1000, 1000))
            os.utime(second, (2000, 2000))

            self.assertEqual(self.plugin._rollback_to_snapshot("session", "core_complete")["code"], "new")
            self.assertEqual(self.plugin._rollback_to_snapshot("session", "other_step"), None)

    def test_rollback_without_snapshot_returns_none(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.plugin.workspace = Path(temp_dir)
            self.assertIsNone(self.plugin._rollback_to_snapshot("missing", "core_complete"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
