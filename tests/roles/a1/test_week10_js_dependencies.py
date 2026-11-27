import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_baseline import MAIN, make_plugin
from test_week06_environment import completed


class A1Week10JsDependencies(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.scripts = Path(temporary.name)
        (self.scripts / "codeagent_js_checker.js").touch()
        self.plugin = make_plugin()
        self.plugin.scripts_dir = self.scripts

    def manifest(self, dependencies=None, dev_dependencies=None):
        data = {
            "dependencies": dependencies if dependencies is not None else {},
            "devDependencies": dev_dependencies if dev_dependencies is not None else {
                "eslint": "^8.57.0", "typescript": "^5.3.0",
            },
        }
        (self.scripts / "package.json").write_text(json.dumps(data), encoding="utf-8")

    def installed(self, *names):
        for name in names:
            (self.scripts / "node_modules" / name).mkdir(parents=True, exist_ok=True)

    def test_empty_existing_modules_directory_triggers_npm(self):
        self.manifest()
        (self.scripts / "node_modules").mkdir()
        with mock.patch.object(MAIN.subprocess, "run", side_effect=[completed(), completed()]) as run:
            self.plugin._ensure_js_dependencies()
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[1].args[0], ["npm", "install", "--production=false"])

    def test_missing_one_manifest_dependency_triggers_npm(self):
        self.manifest()
        self.installed("eslint")
        with mock.patch.object(MAIN.subprocess, "run", side_effect=[completed(), completed()]) as run:
            self.plugin._ensure_js_dependencies()
        self.assertEqual(run.call_count, 2)
        self.assertTrue(any("安装完成" in text for level, text in self.plugin.logger.messages if level == "info"))

    def test_all_manifest_dependencies_installed_skips_npm(self):
        self.manifest()
        self.installed("eslint", "typescript")
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed()) as run:
            self.plugin._ensure_js_dependencies()
        run.assert_called_once_with(["node", "-v"], capture_output=True, check=True)

    def test_dependency_list_comes_from_manifest_not_fixed_names(self):
        self.manifest(dependencies={"left-pad": "1.0.0"}, dev_dependencies={"typescript": "^5.3.0"})
        self.installed("typescript")
        with mock.patch.object(MAIN.subprocess, "run", side_effect=[completed(), completed()]) as run:
            self.plugin._ensure_js_dependencies()
        self.assertEqual(run.call_count, 2)
        self.assertEqual(run.call_args_list[1].args[0], ["npm", "install", "--production=false"])

    def test_invalid_manifest_warns_and_does_not_claim_success(self):
        self.installed("eslint")
        (self.scripts / "package.json").write_text("{invalid", encoding="utf-8")
        with mock.patch.object(MAIN.subprocess, "run", side_effect=[
            completed(), completed(returncode=1, stderr="invalid manifest"),
        ]) as run:
            self.plugin._ensure_js_dependencies()
        self.assertEqual(run.call_count, 2)
        warnings = [text for level, text in self.plugin.logger.messages if level == "warning"]
        self.assertTrue(any("清单检查失败" in text for text in warnings))
        self.assertTrue(any("安装失败" in text for text in warnings))
        self.assertFalse(any("安装完成" in text for _, text in self.plugin.logger.messages))
