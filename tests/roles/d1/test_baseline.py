"""D1 baseline: real checker CLI, adapter unit tests, tracked contract defects.

Run: python -B -m unittest discover -s tests/roles/d1 -p 'test_*.py' -v
Expected failures are unresolved defects, not successful business checks.
"""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "skills" / "CodeAgent" / "scripts"
NODE = shutil.which("node")


def load_plugin():
    """Load actual main.py, stubbing only AstrBot registration dependencies."""
    api = types.ModuleType("astrbot.api")
    event = types.ModuleType("astrbot.api.event")
    star = types.ModuleType("astrbot.api.star")
    event.filter = types.SimpleNamespace(command=lambda name: lambda fn: fn)
    event.AstrMessageEvent = type("AstrMessageEvent", (), {})
    star.Context = type("Context", (), {})
    star.Star = type("Star", (), {})
    api.logger = types.SimpleNamespace()
    api.AstrBotConfig = dict
    stubs = {
        "astrbot": types.ModuleType("astrbot"),
        "astrbot.api": api,
        "astrbot.api.event": event,
        "astrbot.api.star": star,
    }
    spec = importlib.util.spec_from_file_location("d1_plugin_under_test", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stubs):
        spec.loader.exec_module(module)
    return module


class AdapterBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_plugin()

    def setUp(self):
        self.plugin = object.__new__(self.module.CodeAgentPlugin)
        self.plugin.scripts_dir = SCRIPTS
        self.plugin.config = {}

    def test_sandbox_preserves_result_payload(self):
        payload = {"success": False, "stdout": "", "stderr": "bad input", "exit_code": 1}
        with patch.object(self.module.subprocess, "run", return_value=
                          subprocess.CompletedProcess([], 0, json.dumps(payload), "")):
            self.assertEqual(self.plugin._call_sandbox("x", "session"), payload)

    def test_sandbox_process_error(self):
        with patch.object(self.module.subprocess, "run", return_value=
                          subprocess.CompletedProcess([], 2, "", "bad configuration")):
            result = self.plugin._call_sandbox("x", "session")
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "bad configuration")

    def test_sandbox_timeout(self):
        with patch.object(self.module.subprocess, "run", side_effect=
                          subprocess.TimeoutExpired("sandbox", 150)):
            self.assertEqual(self.plugin._call_sandbox("x", "session"),
                             {"success": False, "error": "Sandbox timeout"})

    def test_sandbox_invalid_json_is_failure(self):
        with patch.object(self.module.subprocess, "run", return_value=
                          subprocess.CompletedProcess([], 0, "not json", "")):
            result = self.plugin._call_sandbox("x", "session")
        self.assertFalse(result["success"])
        self.assertTrue(result["error"])

    def test_sandbox_session_language_filename_and_outer_timeout(self):
        self.plugin.config = {"code_running_time": 9}
        with patch.object(self.module.subprocess, "run", return_value=
                          subprocess.CompletedProcess([], 0, '{"success": true}', "")) as run:
            self.plugin._call_sandbox("print(1)", "d1_session", "python", "sample.py")
        argv = run.call_args.args[0]
        for flag, value in (("--session-id", "d1_session"), ("--language", "python"),
                            ("--filename", "sample.py")):
            self.assertEqual(argv[argv.index(flag) + 1], value)
        self.assertEqual(run.call_args.kwargs["timeout"], 39)

    def test_missing_sandbox_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            self.plugin.scripts_dir = Path(directory)
            with patch.object(self.module.subprocess, "run") as run:
                result = self.plugin._call_sandbox("x", "session")
            run.assert_not_called()
        self.assertFalse(result["success"])

    def test_checker_nonzero_exit_preserves_json_diagnostics(self):
        payload = {"passed": False, "issues": [{"level": "critical", "line": 2}]}
        with patch.object(self.module.subprocess, "run", side_effect=[
            subprocess.CompletedProcess([], 0, "v22", ""),
            subprocess.CompletedProcess([], 1, json.dumps(payload), ""),
        ]):
            self.assertEqual(self.plugin._call_js_checker("eval('1')"), payload)

    def test_checker_nonzero_exit_without_json_fails(self):
        with patch.object(self.module.subprocess, "run", side_effect=[
            subprocess.CompletedProcess([], 0, "v22", ""),
            subprocess.CompletedProcess([], 1, "", "checker crashed"),
        ]):
            result = self.plugin._call_js_checker("x")
        self.assertEqual(result, {"passed": False, "error": "checker crashed"})

    @unittest.expectedFailure
    def test_known_d1_001_sandbox_receives_raw_code(self):
        code = 'print("你好")\nprint("second line")'
        with patch.object(self.module.subprocess, "run", return_value=
                          subprocess.CompletedProcess([], 0, "{}", "")) as run:
            self.plugin._call_sandbox(code, "session")
        argv = run.call_args.args[0]
        self.assertEqual(argv[argv.index("--code") + 1], code)

    @unittest.expectedFailure
    def test_known_d1_002_sandbox_config_is_readable_file(self):
        self.plugin.config = {"code_running_time": 9, "memory_limit": 128, "max_file_size": 2}
        received = []

        def capture(argv, **kwargs):
            # Read while the child would run: a temporary file may disappear on return.
            try:
                with open(argv[argv.index("--config") + 1], encoding="utf-8") as stream:
                    received.append(json.load(stream))
            except (OSError, ValueError) as error:
                received.append(type(error).__name__)
            return subprocess.CompletedProcess(argv, 0, "{}", "")

        with patch.object(self.module.subprocess, "run", side_effect=capture):
            self.plugin._call_sandbox("print(1)", "session")
        self.assertEqual(received, [{"wall_time_limit": 9, "memory_limit_mb": 128,
                                     "file_size_limit_mb": 2}])

    @unittest.expectedFailure
    def test_known_d1_003_checker_receives_raw_code(self):
        code = 'const greeting = "你好";\nconsole.log(greeting);'
        with patch.object(self.module.subprocess, "run", return_value=
                          subprocess.CompletedProcess([], 0, "{}", "")) as run:
            self.plugin._call_js_checker(code, "typescript")
        argv = run.call_args.args[0]
        self.assertEqual(argv[argv.index("--language") + 1], "typescript")
        self.assertEqual(argv[argv.index("--code") + 1], code)

    @unittest.expectedFailure
    def test_known_d1_004_missing_node_must_not_pass(self):
        with patch.object(self.module.subprocess, "run", side_effect=FileNotFoundError("node")):
            result = self.plugin._call_js_checker("const x = 1;")
        self.assertFalse(result["passed"])

    @unittest.expectedFailure
    def test_known_d1_005_checker_timeout_must_not_pass(self):
        with patch.object(self.module.subprocess, "run", side_effect=[
            subprocess.CompletedProcess([], 0, "v22", ""),
            subprocess.TimeoutExpired("checker", 60),
        ]):
            result = self.plugin._call_js_checker("const x = 1;")
        self.assertFalse(result["passed"])


@unittest.skipUnless(NODE, "Node.js is required for real checker CLI tests")
class CheckerCliBaseline(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="d1-baseline-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.env = os.environ.copy()
        # Isolate the checker's fixed temp directory and deliberately omit lint tools.
        self.env.update(TEMP=self.temp.name, TMP=self.temp.name, TMPDIR=self.temp.name,
                        PATH=self.temp.name)

    def run_checker(self, *args):
        return subprocess.run([NODE, str(SCRIPTS / "codeagent_js_checker.js"), *args],
                              cwd=self.directory, env=self.env, capture_output=True,
                              encoding="utf-8", timeout=30)

    def test_safe_input_json_schema_and_missing_tool_disclosure(self):
        proc = self.run_checker("--code", "const x = 1;", "--language", "javascript")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertTrue({"passed", "issues", "quality_score", "summary", "eslint",
                         "typescript", "security", "quality"} <= result.keys())
        self.assertEqual(result["security"], {"issues": [], "risk_level": "safe"})
        self.assertEqual(result["quality_score"], 100)
        self.assertFalse(result["eslint"]["available"])
        self.assertTrue(result["eslint"]["error"])

    def test_eval_is_rejected_with_line_number_without_executing_input(self):
        proc = self.run_checker("--code", "const x = 1;\neval('1 + 1');")
        self.assertEqual(proc.returncode, 1, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertFalse(result["passed"])
        self.assertEqual(result["security"]["risk_level"], "critical")
        self.assertTrue(any(i["line"] == 2 and i["level"] == "critical"
                            and i["tool"] == "security" for i in result["issues"]))

    def test_whitespace_input_fails_with_json(self):
        proc = self.run_checker("--code", " \n ")
        self.assertEqual(proc.returncode, 1)
        result = json.loads(proc.stdout)
        self.assertFalse(result["passed"])
        self.assertEqual(result["quality_score"], 0)

    def test_missing_code_file_returns_error(self):
        proc = self.run_checker("--code-file", str(self.directory / "missing.js"))
        self.assertEqual(proc.returncode, 1)
        self.assertIn("missing.js", proc.stderr)

    def test_code_file_and_output_file_with_spaces(self):
        source = self.directory / "input with spaces.js"
        output = self.directory / "result with spaces.json"
        source.write_text('const greeting = "你好";\neval(greeting);', encoding="utf-8")
        proc = self.run_checker("--code-file", str(source), "--output", str(output))
        self.assertEqual(proc.returncode, 1, proc.stderr)
        self.assertEqual(proc.stdout, "")
        result = json.loads(output.read_text(encoding="utf-8"))
        self.assertFalse(result["passed"])
        self.assertEqual(result["security"]["issues"][0]["line"], 2)
        self.assertFalse((self.directory / "codeagent_js_check").exists())

    def test_typescript_auto_detection_reports_missing_compiler(self):
        proc = self.run_checker("--code", "const count: number = 1;", "--language", "auto")
        result = json.loads(proc.stdout)
        self.assertFalse(result["typescript"]["available"])
        self.assertTrue(result["typescript"]["error"])
        self.assertEqual(result["typescript"]["issues"], [])

    def test_quality_threshold_rejects_long_uncommented_var_code(self):
        code = "\n".join(f"var item{i} = '{'x' * 130}';" for i in range(31))
        proc = self.run_checker("--code", code)
        self.assertEqual(proc.returncode, 1, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertLess(result["quality_score"], 75)
        self.assertFalse(result["passed"])
        self.assertEqual(result["security"]["issues"], [])


class SandboxPlatformBaseline(unittest.TestCase):
    @unittest.skipUnless(sys.platform == "win32", "Windows-specific import defect")
    @unittest.expectedFailure
    def test_known_d1_006_windows_sandbox_help_starts(self):
        # --help never executes user code or applies resource limits.
        proc = subprocess.run([sys.executable, str(SCRIPTS / "codeagent_sandbox.py"), "--help"],
                              capture_output=True, encoding="utf-8", timeout=10)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--session-id", proc.stdout)


if __name__ == "__main__":
    unittest.main()
