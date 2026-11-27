import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from test_baseline import MAIN, make_plugin
from test_week06_environment import completed


class A1Week11Recovery(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.scripts = Path(temporary.name)
        (self.scripts / "codeagent_js_checker.js").touch()
        self.plugin = make_plugin()
        self.plugin.scripts_dir = self.scripts

    def manifest(self, dev_dependencies):
        (self.scripts / "package.json").write_text(
            json.dumps({"dependencies": {}, "devDependencies": dev_dependencies}),
            encoding="utf-8",
        )

    def test_failed_install_retries_on_next_start_when_modules_still_missing(self):
        self.manifest({"typescript": "^5.3.0"})
        (self.scripts / "node_modules").mkdir()
        with mock.patch.object(
            MAIN.subprocess, "run",
            side_effect=[
                completed(), completed(returncode=1, stderr="network unavailable"),
                completed(), completed(returncode=0),
            ],
        ) as run:
            self.plugin._ensure_js_dependencies()
            self.plugin._ensure_js_dependencies()
        self.assertEqual(run.call_count, 4)
        self.assertEqual(run.call_args_list[1].args[0], ["npm", "install", "--production=false"])
        self.assertEqual(run.call_args_list[3].args[0], ["npm", "install", "--production=false"])
        self.assertTrue(any("安装失败" in text for level, text in self.plugin.logger.messages if level == "warning"))

    def test_failed_node_probe_blocks_npm_with_partial_modules(self):
        self.manifest({"typescript": "^5.3.0"})
        (self.scripts / "node_modules").mkdir()
        with mock.patch.object(
            MAIN.subprocess, "run", side_effect=FileNotFoundError("node unavailable"),
        ) as run:
            self.plugin._ensure_js_dependencies()
        run.assert_called_once_with(["node", "-v"], capture_output=True, check=True)

    def test_empty_manifest_and_existing_modules_directory_need_no_npm(self):
        self.manifest({})
        (self.scripts / "node_modules").mkdir()
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed()) as run:
            self.plugin._ensure_js_dependencies()
        run.assert_called_once_with(["node", "-v"], capture_output=True, check=True)

    def test_scoped_dependency_subdirectory_is_recognized(self):
        self.manifest({"@scope/checker": "1.0.0"})
        (self.scripts / "node_modules" / "@scope" / "checker").mkdir(parents=True)
        with mock.patch.object(MAIN.subprocess, "run", return_value=completed()) as run:
            self.plugin._ensure_js_dependencies()
        run.assert_called_once_with(["node", "-v"], capture_output=True, check=True)

    def test_non_mapping_manifest_is_handled_without_false_install_success(self):
        (self.scripts / "package.json").write_text("[]", encoding="utf-8")
        (self.scripts / "node_modules").mkdir()
        with mock.patch.object(MAIN.subprocess, "run", side_effect=[
            completed(), completed(returncode=1, stderr="invalid package"),
        ]) as run:
            self.plugin._ensure_js_dependencies()
        self.assertEqual(run.call_count, 2)
        self.assertTrue(any("清单检查失败" in value for level, value in self.plugin.logger.messages if level == "warning"))
        self.assertFalse(any("安装完成" in value for _, value in self.plugin.logger.messages))
