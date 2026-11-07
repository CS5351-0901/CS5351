"""Week 6 executable regression enhancement for A1 Node/npm preparation.

All install/download/subprocess operations are patched. These tests never
install Node.js or packages or touch a live AstrBot installation.
"""
import subprocess
import unittest
from types import SimpleNamespace
from unittest import mock

from test_baseline import MAIN, FixtureScriptDirectory, make_plugin


def completed(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


class A1Week06EnvironmentTests(unittest.TestCase):
    def test_existing_node_skips_platform_specific_installers(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed(stdout="v22.2.0")) as runner, \
                mock.patch.object(MAIN.platform, "system", return_value="Linux") as platform_probe, \
                mock.patch.object(plugin, "_install_nodejs_linux") as installer:
            self.assertTrue(plugin._ensure_nodejs())
        runner.assert_called_once_with(["node", "-v"], capture_output=True, text=True, timeout=5)
        platform_probe.assert_not_called()
        installer.assert_not_called()

    def test_linux_node_probe_nonzero_routes_to_linux_installer(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed(returncode=1)), \
                mock.patch.object(MAIN.platform, "system", return_value="Linux"), \
                mock.patch.object(plugin, "_install_nodejs_linux", return_value=True) as installer:
            self.assertTrue(plugin._ensure_nodejs())
        installer.assert_called_once_with()

    def test_macos_node_probe_timeout_routes_to_mac_installer(self):
        plugin = make_plugin()
        with mock.patch.object(
            MAIN.subprocess, "run", side_effect=subprocess.TimeoutExpired(["node", "-v"], 5)
        ), mock.patch.object(MAIN.platform, "system", return_value="Darwin"), \
                mock.patch.object(plugin, "_install_nodejs_mac", return_value=True) as installer:
            self.assertTrue(plugin._ensure_nodejs())
        installer.assert_called_once_with()

    def test_linux_without_package_manager_uses_official_fallback(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.shutil, "which", return_value=None), \
                mock.patch.object(plugin, "_install_nodejs_from_official", return_value=True) as fallback, \
                mock.patch.object(MAIN.subprocess, "run") as runner:
            self.assertTrue(plugin._install_nodejs_linux())
        fallback.assert_called_once_with()
        runner.assert_not_called()

    def test_linux_package_manager_error_continues_to_next(self):
        plugin = make_plugin()
        with mock.patch.object(
            MAIN.shutil, "which",
            side_effect=lambda name: name if name in ("apt", "dnf") else None,
        ), mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=[subprocess.CalledProcessError(1, "apt"), completed()],
        ) as runner, mock.patch.object(plugin, "_install_nodejs_from_official") as fallback:
            self.assertTrue(plugin._install_nodejs_linux())
        self.assertEqual(runner.call_count, 2)
        self.assertIn("apt-get update", runner.call_args_list[0].args[0])
        self.assertIn("dnf install", runner.call_args_list[1].args[0])
        fallback.assert_not_called()

    def test_macos_homebrew_failure_uses_official_fallback(self):
        plugin = make_plugin()
        with mock.patch.object(MAIN.shutil, "which", return_value="/opt/homebrew/bin/brew"), \
                mock.patch.object(
                    MAIN.subprocess, "run",
                    side_effect=subprocess.CalledProcessError(1, "brew"),
                ) as runner, mock.patch.object(
                    plugin, "_install_nodejs_from_official", return_value=True
                ) as fallback:
            self.assertTrue(plugin._install_nodejs_mac())
        runner.assert_called_once_with("brew install node", shell=True, check=True, timeout=300)
        fallback.assert_called_once_with()

    def test_absent_js_checker_never_probes_node(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory(set())
        with mock.patch.object(MAIN.subprocess, "run") as runner:
            self.assertIsNone(plugin._ensure_js_dependencies())
        runner.assert_not_called()

    def test_absent_package_json_never_invokes_npm(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js"})
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed()) as runner:
            self.assertIsNone(plugin._ensure_js_dependencies())
        runner.assert_called_once_with(["node", "-v"], capture_output=True, check=True)

    def test_missing_node_aborts_before_npm(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js", "package.json"})
        with mock.patch.object(MAIN.subprocess, "run", side_effect=FileNotFoundError("node")) as runner:
            self.assertIsNone(plugin._ensure_js_dependencies())
        self.assertEqual(runner.call_count, 1)

    def test_npm_nonzero_exit_warns_and_does_not_claim_success(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js", "package.json"})
        with mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=[completed(), completed(returncode=1, stderr="E" * 250)],
        ) as runner:
            self.assertIsNone(plugin._ensure_js_dependencies())
        self.assertEqual(runner.call_count, 2)
        self.assertEqual(runner.call_args_list[1].args[0], ["npm", "install", "--production=false"])
        self.assertEqual(runner.call_args_list[1].kwargs["timeout"], 180)
        warnings = [message for level, message in plugin.logger.messages if level == "warning"]
        self.assertEqual(warnings, ["JS 依赖安装失败: " + "E" * 200])
        self.assertFalse(any("安装完成" in message for _, message in plugin.logger.messages))

    def test_npm_timeout_is_reported_without_crashing(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js", "package.json"})
        with mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=[completed(), subprocess.TimeoutExpired(["npm", "install"], 180)],
        ) as runner:
            self.assertIsNone(plugin._ensure_js_dependencies())
        self.assertEqual(runner.call_count, 2)
        self.assertIn(("warning", "JS 依赖安装超时"), plugin.logger.messages)

    def test_npm_success_reports_completion(self):
        plugin = make_plugin()
        plugin.scripts_dir = FixtureScriptDirectory({"codeagent_js_checker.js", "package.json"})
        with mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=[completed(), completed(returncode=0)],
        ) as runner:
            self.assertIsNone(plugin._ensure_js_dependencies())
        self.assertEqual(runner.call_count, 2)
        self.assertIn(("info", "JS 依赖安装完成"), plugin.logger.messages)


if __name__ == "__main__":
    unittest.main(verbosity=2)
