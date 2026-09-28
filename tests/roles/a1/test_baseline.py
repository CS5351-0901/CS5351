"""A1's stdlib-only regression baseline for configuration and preparation paths."""

import importlib.util
import json
import sys
import types
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def load_main_without_astrbot_runtime():
    """Load main.py with tiny import stubs; plugin initialization is never run."""
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
    previous = {name: sys.modules.get(name) for name in stubs}
    sys.modules.update(stubs)
    try:
        spec = importlib.util.spec_from_file_location(
            "_a1_week05_main", REPOSITORY_ROOT / "main.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, old_module in previous.items():
            if old_module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old_module


MAIN = load_main_without_astrbot_runtime()


class RecordingLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(("info", message))

    def warning(self, message):
        self.messages.append(("warning", message))

    def error(self, message):
        self.messages.append(("error", message))


class PluginConfig(dict):
    """Small mapping-shaped stand-in for the AstrBot config getter."""

    def get(self, key, default=None):
        return super().get(key, default)


class FixturePath:
    def __init__(self, name, present):
        self.name = name
        self.present = present

    def exists(self):
        return self.present

    def __str__(self):
        return f"a1-fixture/{self.name}"


class FixtureScriptDirectory:
    def __init__(self, present_files):
        self.present_files = set(present_files)

    def __truediv__(self, name):
        return FixturePath(name, name in self.present_files)

    def __str__(self):
        return "a1-fixture"


def make_plugin(config=None):
    plugin = object.__new__(MAIN.CodeAgentPlugin)
    plugin.config = config if config is not None else PluginConfig()
    plugin.logger = RecordingLogger()
    return plugin


class A1BaselineTests(unittest.TestCase):
    def test_schema_contains_defaults_for_directly_read_settings(self):
        schema = json.loads((REPOSITORY_ROOT / "_conf_schema.json").read_text(encoding="utf-8"))
        expected = {
            "admin_blacklist": ("list", []),
            "group_blacklist": ("list", []),
            "max_debug_rounds": ("int", 10),
            "code_running_time": ("int", 120),
            "quality_threshold": ("int", 75),
            "memory_limit": ("float", 512.0),
            "max_file_size": ("float", 10.0),
        }

        for key, (setting_type, default) in expected.items():
            with self.subTest(setting=key):
                self.assertIn(key, schema)
                self.assertEqual(schema[key]["type"], setting_type)
                self.assertEqual(schema[key]["default"], default)

    def test_config_getter_preserves_values_and_fallbacks(self):
        plugin = make_plugin(PluginConfig({"quality_threshold": 80}))

        self.assertEqual(plugin._get_config("quality_threshold", 75), 80)
        self.assertEqual(plugin._get_config("missing_setting", 12), 12)

    def test_blacklist_checks_user_and_group_ids_as_strings(self):
        plugin = make_plugin(
            PluginConfig({"admin_blacklist": [123], "group_blacklist": ["blocked-room"]})
        )

        self.assertTrue(plugin._is_in_blacklist("123", "open-room"))
        self.assertTrue(plugin._is_in_blacklist("456", "blocked-room"))
        self.assertFalse(plugin._is_in_blacklist("456", "open-room"))

    def test_sandbox_receives_configured_limits_and_timeout(self):
        plugin = make_plugin(
            PluginConfig(
                {
                    "code_running_time": 4,
                    "memory_limit": 64,
                    "max_file_size": 2.5,
                }
            )
        )
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_sandbox.py"})
        completed = SimpleNamespace(returncode=0, stdout='{"success": true}', stderr="")

        with mock.patch.object(MAIN.subprocess, "run", return_value=completed) as run:
            result = plugin._call_sandbox("print('ok')", "session-1")

        self.assertEqual(result, {"success": True})
        args, kwargs = run.call_args
        config_json = args[0][args[0].index("--config") + 1]
        self.assertEqual(
            json.loads(config_json),
            {
                "wall_time_limit": 4,
                "memory_limit_mb": 64,
                "file_size_limit_mb": 2.5,
            },
        )
        self.assertEqual(kwargs["timeout"], 34)

    def test_windows_node_missing_uses_unsupported_system_path(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.subprocess, "run", side_effect=FileNotFoundError("node")):
            with mock.patch.object(MAIN.platform, "system", return_value="Windows"):
                self.assertFalse(plugin._ensure_nodejs())

        self.assertTrue(
            any("不支持的系统: Windows" in message for level, message in plugin.logger.messages)
        )

    def test_windows_node_present_returns_without_installing(self):
        plugin = make_plugin()
        found_node = SimpleNamespace(returncode=0, stdout="v20.18.0", stderr="")

        with mock.patch.object(MAIN.subprocess, "run", return_value=found_node) as run:
            with mock.patch.object(MAIN.platform, "system", return_value="Windows"):
                self.assertTrue(plugin._ensure_nodejs())

        run.assert_called_once_with(["node", "-v"], capture_output=True, text=True, timeout=5)

    def test_dependency_setup_skips_npm_when_node_modules_exists(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory(
            {"codeagent_js_checker.js", "package.json", "node_modules"}
        )
        found_node = SimpleNamespace(returncode=0, stdout="v20.18.0", stderr="")

        with mock.patch.object(MAIN.subprocess, "run", return_value=found_node) as run:
            plugin._ensure_js_dependencies()

        run.assert_called_once_with(["node", "-v"], capture_output=True, check=True)

    def test_dependency_setup_reports_missing_npm_without_raising(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory(
            {"codeagent_js_checker.js", "package.json"}
        )
        found_node = SimpleNamespace(returncode=0, stdout="v20.18.0", stderr="")

        with mock.patch.object(
            MAIN.subprocess,
            "run",
            side_effect=[found_node, FileNotFoundError("npm")],
        ) as run:
            plugin._ensure_js_dependencies()

        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args.args[0], ["npm", "install", "--production=false"])
        self.assertTrue(
            any(
                level == "warning" and "JS 依赖安装异常" in message
                for level, message in plugin.logger.messages
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
