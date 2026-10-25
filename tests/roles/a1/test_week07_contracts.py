"""A1 Week 7 boundary/contract/failure-path tests for configuration and setup."""
import subprocess
import tarfile
import unittest
from unittest import mock

from test_baseline import MAIN, FixtureScriptDirectory, PluginConfig, make_plugin
from test_week06_environment import completed


class A1Week07Contracts(unittest.TestCase):
    def test_config_preserves_explicit_falsey_values(self):
        plugin = make_plugin(PluginConfig({
            "enable_visit_internet": False,
            "quality_threshold": 0,
            "coding_model": "",
            "admin_blacklist": [],
            "requirement_analysis_model": None,
        }))
        for key, expected in [
            ("enable_visit_internet", False),
            ("quality_threshold", 0),
            ("coding_model", ""),
            ("admin_blacklist", []),
            ("requirement_analysis_model", None),
        ]:
            with self.subTest(key=key):
                self.assertEqual(plugin._get_config(key, "fallback"), expected)
        self.assertEqual(plugin._get_config("unlisted_key", "fallback"), "fallback")

    def test_linux_install_failure_does_not_report_success(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed(returncode=1)), \
                mock.patch.object(MAIN.platform, "system", return_value="Linux"), \
                mock.patch.object(plugin, "_install_nodejs_linux", return_value=False) as install:
            self.assertFalse(plugin._ensure_nodejs())
        install.assert_called_once_with()
        self.assertTrue(any("自动安装失败" in msg for level, msg in plugin.logger.messages if level == "warning"))
        self.assertFalse(any("Node.js 已安装" in msg for _, msg in plugin.logger.messages))

    def test_linux_two_package_managers_fail_before_official_fallback(self):
        plugin = make_plugin()
        with mock.patch.object(
            MAIN.shutil, "which",
            side_effect=lambda tool: tool if tool in ("apt", "dnf") else None,
        ), mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=subprocess.CalledProcessError(1, "install"),
        ) as command, mock.patch.object(
            plugin, "_install_nodejs_from_official", return_value=False
        ) as fallback:
            self.assertFalse(plugin._install_nodejs_linux())
        self.assertEqual(command.call_count, 2)
        fallback.assert_called_once_with()

    def test_macos_without_homebrew_uses_official_fallback_only(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.shutil, "which", return_value=None), \
                mock.patch.object(plugin, "_install_nodejs_from_official", return_value=False) as fallback, \
                mock.patch.object(MAIN.subprocess, "run") as command:
            self.assertFalse(plugin._install_nodejs_mac())
        fallback.assert_called_once_with()
        command.assert_not_called()

    def test_official_node_download_failure_returns_false_without_extracting(self):
        plugin = make_plugin()
        with mock.patch.object(
            MAIN.urllib.request, "urlretrieve",
            side_effect=OSError("network unavailable"),
        ) as download, mock.patch.object(MAIN.tarfile, "open") as archive, \
                mock.patch.object(MAIN.subprocess, "run") as command:
            self.assertFalse(plugin._install_nodejs_from_official())
        self.assertEqual(download.call_count, 1)
        self.assertIn("nodejs.org/dist/", download.call_args.args[0])
        archive.assert_not_called()
        command.assert_not_called()
        self.assertTrue(any("官方安装失败" in msg for level, msg in plugin.logger.messages if level == "error"))

    def test_official_node_corrupt_archive_stops_before_copying(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.urllib.request, "urlretrieve"), \
                mock.patch.object(
                    MAIN.tarfile, "open",
                    side_effect=tarfile.ReadError("corrupt fixture"),
                ) as archive, mock.patch.object(MAIN.subprocess, "run") as command, \
                mock.patch.object(MAIN.os, "makedirs") as create_dir:
            self.assertFalse(plugin._install_nodejs_from_official())
        archive.assert_called_once_with("/tmp/nodejs.tar.xz", "r:xz")
        command.assert_not_called()
        create_dir.assert_not_called()

    def test_node_probe_checked_failure_prevents_npm_invocation(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js", "package.json"})
        with mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=subprocess.CalledProcessError(127, ["node", "-v"]),
        ) as command:
            self.assertIsNone(plugin._ensure_js_dependencies())
        command.assert_called_once_with(["node", "-v"], capture_output=True, check=True)
        self.assertFalse(any("依赖安装完成" in msg for _, msg in plugin.logger.messages))

    def test_npm_permission_denied_warns_without_claiming_success(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js", "package.json"})
        with mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=[completed(), PermissionError("npm executable blocked")],
        ) as command:
            self.assertIsNone(plugin._ensure_js_dependencies())
        self.assertEqual(command.call_count, 2)
        self.assertEqual(command.call_args_list[1].args[0], ["npm", "install", "--production=false"])
        self.assertTrue(any("JS 依赖安装异常" in msg for level, msg in plugin.logger.messages if level == "warning"))
        self.assertFalse(any("依赖安装完成" in msg for _, msg in plugin.logger.messages))


if __name__ == "__main__":
    unittest.main(verbosity=2)
