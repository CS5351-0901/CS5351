"""Baseline checks for B1's requirement and classification helpers."""

import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def load_plugin_type():
    """Import the real plugin module with only its AstrBot imports stubbed."""
    astrbot = types.ModuleType("astrbot")
    api = types.ModuleType("astrbot.api")
    event = types.ModuleType("astrbot.api.event")
    star = types.ModuleType("astrbot.api.star")

    event.filter = types.SimpleNamespace(
        command=lambda _name: (lambda function: function)
    )
    event.AstrMessageEvent = type("AstrMessageEvent", (), {})
    star.Context = type("Context", (), {})
    star.Star = type("Star", (), {})
    api.logger = types.SimpleNamespace()
    api.AstrBotConfig = type("AstrBotConfig", (), {})

    stubs = {
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event,
        "astrbot.api.star": star,
    }
    spec = importlib.util.spec_from_file_location(
        "_b1_main_under_test", REPOSITORY_ROOT / "main.py"
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the course plugin module")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stubs):
        spec.loader.exec_module(module)
    return module.CodeAgentPlugin


class B1BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin_type = load_plugin_type()

    def make_plugin(self, config=None):
        plugin = object.__new__(self.plugin_type)
        plugin.config = config if config is not None else {}
        return plugin

    def test_plain_and_mentioned_requirement(self):
        plugin = self.make_plugin()
        self.assertEqual(plugin._extract_requirement("/agent build a parser"), "build a parser")
        self.assertEqual(
            plugin._extract_requirement("@builder/agent build a parser"),
            "build a parser",
        )

    def test_requirement_preserves_multiline_body(self):
        plugin = self.make_plugin()
        self.assertEqual(
            plugin._extract_requirement("/agent build a parser\nwith tests  "),
            "build a parser\nwith tests",
        )
        self.assertEqual(
            plugin._extract_requirement("/agent build a parser\r\nwith tests"),
            "build a parser\r\nwith tests",
        )

    def test_missing_or_blank_requirement(self):
        plugin = self.make_plugin()
        self.assertIsNone(plugin._extract_requirement("build a parser"))
        self.assertIsNone(plugin._extract_requirement("/agent   "))
        self.assertIsNone(plugin._extract_requirement("/agent \n  "))
        self.assertIsNone(plugin._extract_requirement("@builder/agent   "))

    def test_blacklist_normalizes_ids_and_checks_both_lists(self):
        plugin = self.make_plugin(
            {"admin_blacklist": [42], "group_blacklist": ["blocked-room"]}
        )
        self.assertTrue(plugin._is_in_blacklist("42", "open-room"))
        self.assertTrue(plugin._is_in_blacklist(7, "blocked-room"))
        self.assertFalse(plugin._is_in_blacklist("7", "open-room"))

    def test_empty_blacklists_allow_request(self):
        plugin = self.make_plugin()
        self.assertFalse(plugin._is_in_blacklist("42", "room"))

    def test_project_type_respects_ordered_keywords(self):
        plugin = self.make_plugin()
        self.assertEqual(plugin._assess_project("网页工具")["type"], "web")
        self.assertEqual(plugin._assess_project("Create an API endpoint")["type"], "api")
        self.assertEqual(plugin._assess_project("Write a JavaScript parser")["type"], "js")
        self.assertEqual(plugin._assess_project("Write a Python parser")["type"], "python")

    def test_project_size_boundaries(self):
        plugin = self.make_plugin()
        for length, expected in ((29, "S"), (30, "M"), (99, "M"), (100, "L")):
            with self.subTest(length=length):
                self.assertEqual(plugin._assess_project("x" * length)["size"], expected)


if __name__ == "__main__":
    unittest.main()
