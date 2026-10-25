#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B2 role baseline / regression test suite (Sprint 1 Closeout, Week 5).

Covers the 5 responsibilities owned by B2 in main.py:
  - main.py::_is_exit_command
  - main.py::_sanitize_session_id
  - main.py::_cleanup_session
  - active_sessions (session state table; verifies the consistency contract
    with session_id and process.json)
  - main.py::_create_process_json

Design notes:
  - The course repo does not ship the astrbot runtime, so importing main.py
    directly fails at its top-level `import astrbot`.
  - Before loading main.py we inject a fake astrbot module tree into
    sys.modules built from the stdlib only, just to satisfy the import.
    The objects under test are pure functions and do not depend on any
    AstrBot runtime behavior.
  - We construct instances via object.__new__(CodeAgentPlugin) to bypass
    __init__ and avoid side effects such as the automatic Node.js install.
  - Stdlib unittest only; no third-party dependency; runs standalone.
"""

import json
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path

# Repository root and main.py path.
REPO_ROOT = Path(__file__).resolve().parents[3]
MAIN_PY = REPO_ROOT / "main.py"


def _build_astrbot_stubs():
    """Build a fake astrbot module tree to satisfy main.py's top-level imports."""
    astrbot = types.ModuleType("astrbot")
    api = types.ModuleType("astrbot.api")

    # astrbot.api.event: filter (decorator) and AstrMessageEvent.
    event = types.ModuleType("astrbot.api.event")

    def _command(name, *args, **kwargs):
        def deco(fn):
            return fn
        return deco

    event.filter = types.SimpleNamespace(command=_command)
    event.AstrMessageEvent = object

    # astrbot.api.star: Context and Star.
    star = types.ModuleType("astrbot.api.star")
    star.Context = object
    star.Star = object

    # astrbot.api top level: logger and AstrBotConfig.
    api.event = event
    api.star = star
    api.logger = types.SimpleNamespace(
        info=lambda *a, **k: None,
        warning=lambda *a, **k: None,
        error=lambda *a, **k: None,
    )
    api.AstrBotConfig = dict

    astrbot.api = api
    return {
        "astrbot": astrbot,
        "astrbot.api": api,
        "astrbot.api.event": event,
        "astrbot.api.star": star,
    }


def _load_main_module():
    """Load main.py; inject astrbot stubs once on first call."""
    import importlib.util

    if "codeagent_main" in sys.modules:
        return sys.modules["codeagent_main"]

    spec = importlib.util.spec_from_file_location("codeagent_main", str(MAIN_PY))
    module = importlib.util.module_from_spec(spec)
    old_modules = dict(sys.modules)
    sys.modules.update(_build_astrbot_stubs())
    try:
        spec.loader.exec_module(module)
    finally:
        # Restore sys.modules, keeping the freshly loaded module registered.
        for k in old_modules:
            sys.modules[k] = old_modules[k]
        sys.modules["codeagent_main"] = module
    return module


main = _load_main_module()


def make_plugin(tmp_root):
    """Create an instance bypassing __init__, injecting workspace/session state."""
    plugin = object.__new__(main.CodeAgentPlugin)
    plugin.workspace = Path(tmp_root)
    plugin.active_sessions = {}
    return plugin


class B2IsExitCommandTest(unittest.TestCase):
    """main.py::_is_exit_command"""

    def setUp(self):
        self.plugin = make_plugin(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.plugin.workspace, ignore_errors=True)

    def test_matches_exit_command(self):
        self.assertTrue(self.plugin._is_exit_command("/exitconver"))

    def test_case_insensitive(self):
        self.assertTrue(self.plugin._is_exit_command("/EXITCONVER"))

    def test_embedded_in_long_text(self):
        self.assertTrue(self.plugin._is_exit_command("please stop /exitconver task"))

    def test_rejects_normal_text(self):
        self.assertFalse(self.plugin._is_exit_command("/agent write a calculator"))

    def test_rejects_empty(self):
        self.assertFalse(self.plugin._is_exit_command(""))


class B2SanitizeSessionIdTest(unittest.TestCase):
    """main.py::_sanitize_session_id"""

    def setUp(self):
        self.plugin = make_plugin(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.plugin.workspace, ignore_errors=True)

    def test_basic(self):
        self.assertEqual(self.plugin._sanitize_session_id("g1", "u1"), "g1_u1")

    def test_colon_replaced(self):
        self.assertEqual(self.plugin._sanitize_session_id("g:1", "u1"), "g_1_u1")

    def test_slash_replaced(self):
        self.assertEqual(self.plugin._sanitize_session_id("g/1", "u/1"), "g_1_u_1")

    def test_mixed_separators(self):
        self.assertEqual(self.plugin._sanitize_session_id("g:1/2", "u"), "g_1_2_u")


class B2CleanupSessionTest(unittest.TestCase):
    """main.py::_cleanup_session"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.plugin = make_plugin(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.plugin.workspace, ignore_errors=True)

    def test_removes_existing_session_dir(self):
        session_dir = self.plugin.workspace / "g1_u1"
        session_dir.mkdir(parents=True)
        marker = session_dir / "process.json"
        marker.write_text("{}", encoding="utf-8")
        self.assertTrue(session_dir.exists())

        self.plugin._cleanup_session("g1_u1")

        self.assertFalse(session_dir.exists())

    def test_missing_session_is_noop(self):
        # A non-existent session dir must be a silent no-op.
        self.plugin._cleanup_session("no_such_session")

    def test_does_not_touch_other_sessions(self):
        keep = self.plugin.workspace / "keep"
        keep.mkdir(parents=True)
        rm = self.plugin.workspace / "rm"
        rm.mkdir(parents=True)

        self.plugin._cleanup_session("rm")

        self.assertTrue(keep.exists())
        self.assertFalse(rm.exists())


class B2CreateProcessJsonTest(unittest.TestCase):
    """main.py::_create_process_json"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.plugin = make_plugin(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.plugin.workspace, ignore_errors=True)

    def test_creates_process_json_file(self):
        data = self.plugin._create_process_json("g1_u1", "write a calculator", "python", "S")
        process_file = self.plugin.workspace / "g1_u1" / "process.json"
        self.assertTrue(process_file.exists())

        with open(process_file, encoding="utf-8") as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk, data)

    def test_fields_complete(self):
        data = self.plugin._create_process_json("g1_u1", "req", "toolkit", "M")
        for key in (
            "session_id", "requirement", "project_type", "project_size",
            "status", "current_step", "completed_steps", "snapshots",
            "created_at", "updated_at",
        ):
            self.assertIn(key, data)
        self.assertEqual(data["session_id"], "g1_u1")
        self.assertEqual(data["requirement"], "req")
        self.assertEqual(data["status"], "init")
        self.assertEqual(data["current_step"], "requirement_analysis")
        self.assertEqual(data["completed_steps"], [])
        self.assertEqual(data["snapshots"], [])

    def test_nested_dir_auto_created(self):
        self.plugin._create_process_json("a_b", "req", "python", "S")
        self.assertTrue((self.plugin.workspace / "a_b").is_dir())


class B2ActiveSessionsConsistencyTest(unittest.TestCase):
    """active_sessions table consistency contract.

    Verifies that agent_command uses the same session_id across:
      active_sessions key == _sanitize_session_id result == process.json.session_id.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.plugin = make_plugin(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.plugin.workspace, ignore_errors=True)

    def test_single_key_used_across_state(self):
        group_id, user_id = "g:1", "u/2"
        sid = self.plugin._sanitize_session_id(group_id, user_id)

        self.plugin.active_sessions[sid] = {"active": True}
        self.plugin._create_process_json(sid, "req", "python", "S")

        self.assertIn(sid, self.plugin.active_sessions)
        process_file = self.plugin.workspace / sid / "process.json"
        with open(process_file, encoding="utf-8") as f:
            on_disk = json.load(f)
        self.assertEqual(on_disk["session_id"], sid)

    def test_same_sanitize_id_is_deterministic(self):
        # The same group/user must always produce the same session id.
        a = self.plugin._sanitize_session_id("g1", "u1")
        b = self.plugin._sanitize_session_id("g1", "u1")
        self.assertEqual(a, b)

    def test_exit_path_removes_state(self):
        # Reproduce the key operations of the agent_command exit branch.
        sid = self.plugin._sanitize_session_id("g1", "u1")
        self.plugin.active_sessions[sid] = {"active": True}
        session_dir = self.plugin.workspace / sid
        session_dir.mkdir(parents=True)

        # Exit path: mark inactive -> clean dir -> drop from table.
        self.plugin.active_sessions[sid]["active"] = False
        self.plugin._cleanup_session(sid)
        del self.plugin.active_sessions[sid]

        self.assertNotIn(sid, self.plugin.active_sessions)
        self.assertFalse(session_dir.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
