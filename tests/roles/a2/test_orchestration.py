"""A2 orchestration baseline using real command code and controlled boundaries."""

import importlib.util
import asyncio
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


ROOT = Path(__file__).resolve().parents[3]


def load_plugin():
    """Stub only the host imports; restore sys.modules after loading."""
    stubs = {name: types.ModuleType(name) for name in (
        "astrbot", "astrbot.api", "astrbot.api.event", "astrbot.api.star"
    )}
    api = stubs["astrbot.api"]
    api.logger = Mock()
    api.AstrBotConfig = dict
    event = stubs["astrbot.api.event"]
    event.AstrMessageEvent = object
    event.filter = types.SimpleNamespace(command=lambda name: lambda fn: fn)
    star = stubs["astrbot.api.star"]
    star.Context = object
    star.Star = type("Star", (), {"__init__": lambda self, context: None})
    spec = importlib.util.spec_from_file_location("_a2_main", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, stubs):
        spec.loader.exec_module(module)
    return module


MAIN = load_plugin()


class Event:
    def __init__(self, message="/agent calculator"):
        self.message_str = message

    def get_sender_id(self):
        return "user"

    def get_group_id(self):
        return "group"

    def plain_result(self, text):
        return text

    def chain_result(self, components):
        return components


class A2OrchestrationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.plugin = object.__new__(MAIN.CodeAgentPlugin)
        self.plugin.config = {"max_debug_rounds": 2}
        self.plugin.logger = Mock()
        self.plugin.workspace = self.workspace
        self.plugin.active_sessions = {}
        self.stages = []

        def boundary(name, result):
            def call(*args, **kwargs):
                self.stages.append(name)
                return result
            return Mock(side_effect=call)

        self.plugin._create_process_json = boundary("process", {})
        self.plugin._call_sandbox = boundary("sandbox", {"success": True})
        self.plugin._call_security_scan = boundary(
            "security", {"risk_level": "safe", "quality_score": 90}
        )
        self.plugin._call_js_checker = boundary(
            "checker", {"passed": True, "quality_score": 90}
        )
        self.plugin._save_snapshot = boundary("snapshot", "snapshot.json")
        self.plugin._call_packager = boundary(
            "packager", {"success": False, "error": "fixture packaging failure"}
        )
        # Any unexpected external execution is an error, not an actual process.
        guard = patch.object(MAIN.subprocess, "run", side_effect=AssertionError(
            "External processes must be isolated in the A2 baseline"
        ))
        self.process_guard = guard.start()
        self.addCleanup(guard.stop)

    async def run_command(self, message="/agent calculator"):
        return [reply async for reply in self.plugin.agent_command(Event(message))]

    def assert_no_pipeline(self):
        self.assertEqual(self.stages, [])
        self.process_guard.assert_not_called()

    async def test_empty_message_does_not_start_session(self):
        self.assertEqual(await self.run_command(""), [])
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    async def test_denied_user_does_not_start_pipeline(self):
        self.plugin.config["admin_blacklist"] = ["user"]
        self.assertEqual(await self.run_command(), [])
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    async def test_missing_requirement_returns_prompt_without_session(self):
        self.assertEqual(len(await self.run_command("/agent")), 1)
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    async def test_duplicate_request_preserves_existing_session(self):
        session = {"active": True, "requirement": "original"}
        self.plugin.active_sessions["group_user"] = session
        self.assertEqual(len(await self.run_command()), 1)
        self.assertIs(self.plugin.active_sessions["group_user"], session)
        self.assertEqual(session["requirement"], "original")
        self.assert_no_pipeline()

    async def test_exit_handler_cleans_only_target_session(self):
        for name in ("group_user", "other_user"):
            self.plugin.active_sessions[name] = {"active": True}
            (self.workspace / name).mkdir()
        replies = await self.run_command("/exitconver")
        self.assertEqual(len(replies), 1)
        self.assertNotIn("group_user", self.plugin.active_sessions)
        self.assertFalse((self.workspace / "group_user").exists())
        self.assertTrue((self.workspace / "other_user").exists())
        self.assert_no_pipeline()

    async def test_packaging_failure_follows_checks_and_clears_session(self):
        replies = await self.run_command()
        self.assertEqual(self.stages, [
            "process", "sandbox", "security", "snapshot", "packager"
        ])
        self.assertIn("fixture packaging failure", replies[-1])
        self.assertEqual(self.plugin.active_sessions, {})
        arguments = self.plugin._call_packager.call_args.kwargs
        self.assertEqual(arguments["project_type"], "python")
        self.assertEqual(arguments["name"], "CodeAgent_group_user")
        self.assertEqual(arguments["files"][0]["name"], "main.py")
        self.assertEqual(arguments["test_files"][0]["name"], "test_main.py")

    async def test_sandbox_exhaustion_prevents_checking_and_packaging(self):
        self.plugin._call_sandbox.side_effect = None
        self.plugin._call_sandbox.return_value = {
            "success": False, "error": "fixture execution failure"
        }
        replies = await self.run_command()
        self.assertIn("fixture execution failure", replies[-1])
        self.assertEqual(self.plugin._call_sandbox.call_count, 2)
        self.plugin._call_security_scan.assert_not_called()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_success_yields_archive_before_removing_it(self):
        archive = self.workspace / "project.zip"
        archive.write_bytes(b"fixture archive")
        self.plugin._call_packager.side_effect = None
        self.plugin._call_packager.return_value = {
            "success": True, "zip_path": str(archive), "file_count": 4
        }
        components = types.ModuleType("astrbot.api.message_components")
        components.File = lambda **kwargs: types.SimpleNamespace(**kwargs)
        delivered = []
        with patch.dict(sys.modules, {"astrbot.api.message_components": components}):
            async for reply in self.plugin.agent_command(Event()):
                if isinstance(reply, list):
                    self.assertTrue(archive.exists())
                    delivered.extend(reply)
        self.assertEqual(len(delivered), 1)
        self.assertEqual(delivered[0].file, str(archive))
        self.assertFalse(archive.exists())
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_high_risk_result_prevents_snapshot_and_packaging(self):
        self.plugin._call_security_scan.side_effect = None
        self.plugin._call_security_scan.return_value = {
            "risk_level": "high", "summary": "fixture blocked"
        }
        self.assertIn("fixture blocked", (await self.run_command())[-1])
        self.plugin._save_snapshot.assert_not_called()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_js_critical_result_prevents_packaging(self):
        self.plugin._call_js_checker.side_effect = None
        self.plugin._call_js_checker.return_value = {
            "passed": False, "issues": [{"level": "critical"}]
        }
        await self.run_command("/agent js tool")
        self.plugin._call_js_checker.assert_called_once()
        self.plugin._call_security_scan.assert_not_called()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_dependency_exception_reports_error_and_clears_session(self):
        self.plugin._call_sandbox.side_effect = RuntimeError("fixture crash")
        self.assertIn("fixture crash", (await self.run_command())[-1])
        self.plugin.logger.error.assert_called_once()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_terminate_cleans_all_active_sessions_and_is_repeatable(self):
        sessions = [{"active": True}, {"active": True}]
        for name, session in zip(("one", "two"), sessions):
            self.plugin.active_sessions[name] = session
            (self.workspace / name).mkdir()
            (self.workspace / name / "temporary.txt").write_text("fixture")
        await self.plugin.terminate()
        await self.plugin.terminate()
        self.assertEqual(self.plugin.active_sessions, {})
        self.assertTrue(all(not session["active"] for session in sessions))
        self.assertEqual(list(self.workspace.iterdir()), [])
        self.assert_no_pipeline()

    async def test_closing_command_releases_session_before_retry(self):
        command = self.plugin.agent_command(Event())
        await anext(command)
        self.assertIn("group_user", self.plugin.active_sessions)
        await command.aclose()
        self.assertEqual(self.plugin.active_sessions, {})
        retry = self.plugin.agent_command(Event())
        try:
            await anext(retry)
            self.assertIn("group_user", self.plugin.active_sessions)
        finally:
            await retry.aclose()
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    async def test_cancellation_during_wait_propagates_and_releases_session(self):
        waiting = asyncio.Event()
        blocked = asyncio.Event()

        async def pause(_seconds):
            waiting.set()
            await blocked.wait()

        async def consume():
            async for _reply in self.plugin.agent_command(
                Event("/agent " + "x" * 40)
            ):
                pass

        with patch.object(MAIN.asyncio, "sleep", side_effect=pause):
            task = asyncio.create_task(consume())
            try:
                await asyncio.wait_for(waiting.wait(), timeout=2)
                self.assertIn("group_user", self.plugin.active_sessions)
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
                self.assertEqual(self.plugin.active_sessions, {})
                self.plugin._call_sandbox.assert_not_called()
                self.plugin._call_packager.assert_not_called()
                self.plugin.logger.error.assert_not_called()
            finally:
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

    async def test_closing_error_reply_still_releases_session(self):
        self.plugin._call_sandbox.side_effect = RuntimeError("fixture crash")
        command = self.plugin.agent_command(Event())
        try:
            async for reply in command:
                if "fixture crash" in reply:
                    break
            else:
                self.fail("The command did not yield its error reply")
        finally:
            await command.aclose()
        self.assertEqual(self.plugin.active_sessions, {})
        self.plugin._call_packager.assert_not_called()

    async def test_old_command_close_preserves_replacement_session(self):
        old_command = self.plugin.agent_command(Event())
        await anext(old_command)
        await self.plugin.terminate()
        replacement = self.plugin.agent_command(Event())
        try:
            await anext(replacement)
            current_session = self.plugin.active_sessions["group_user"]
            await old_command.aclose()
            self.assertIs(
                self.plugin.active_sessions["group_user"], current_session
            )
        finally:
            await old_command.aclose()
            await replacement.aclose()
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    def test_constructor_initializes_state_with_environment_helpers_isolated(self):
        context, config = object(), {"quality_threshold": 80}
        with patch.object(MAIN, "Path", return_value=self.workspace), \
                patch.object(MAIN.CodeAgentPlugin, "_ensure_nodejs") as node, \
                patch.object(MAIN.CodeAgentPlugin, "_ensure_js_dependencies") as deps:
            plugin = MAIN.CodeAgentPlugin(context, config)
        self.assertIs(plugin.config, config)
        self.assertEqual(plugin.active_sessions, {})
        self.assertEqual(plugin.workspace, self.workspace)
        node.assert_called_once_with()
        deps.assert_called_once_with()
        self.process_guard.assert_not_called()

    async def test_unstarted_generator_close_does_not_remove_existing_session(self):
        existing = {"active": True, "requirement": "already running"}
        self.plugin.active_sessions["group_user"] = existing
        command = self.plugin.agent_command(Event())
        await command.aclose()
        self.assertIs(self.plugin.active_sessions["group_user"], existing)
        self.assert_no_pipeline()

    async def test_interleaved_users_keep_independent_session_lifetimes(self):
        other_event = Event()
        other_event.get_sender_id = lambda: "other"
        first = self.plugin.agent_command(Event())
        second = self.plugin.agent_command(other_event)
        try:
            await anext(first)
            await anext(second)
            second_session = self.plugin.active_sessions["group_other"]
            await first.aclose()
            self.assertNotIn("group_user", self.plugin.active_sessions)
            self.assertIs(self.plugin.active_sessions["group_other"], second_session)
        finally:
            await first.aclose()
            await second.aclose()
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    async def test_zero_debug_budget_skips_execution_and_packaging(self):
        self.plugin.config["max_debug_rounds"] = 0
        replies = await self.run_command()
        self.assertTrue(replies)
        self.assertEqual(self.stages, ["process"])
        self.plugin._call_sandbox.assert_not_called()
        self.plugin._call_security_scan.assert_not_called()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_last_allowed_retry_success_continues_once(self):
        self.plugin._call_sandbox.side_effect = [
            {"success": False, "error": "fixture retry"},
            {"success": True},
        ]
        await self.run_command()
        self.assertEqual(self.plugin._call_sandbox.call_count, 2)
        self.plugin._call_security_scan.assert_called_once()
        self.plugin._save_snapshot.assert_called_once()
        self.plugin._call_packager.assert_called_once()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_malformed_sandbox_result_stops_downstream_work(self):
        self.plugin._call_sandbox.side_effect = None
        self.plugin._call_sandbox.return_value = None
        replies = await self.run_command()
        self.assertTrue(replies)
        self.plugin.logger.error.assert_called_once()
        self.plugin._call_security_scan.assert_not_called()
        self.plugin._save_snapshot.assert_not_called()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_snapshot_failure_prevents_packaging_and_releases_session(self):
        self.plugin._save_snapshot.side_effect = OSError("fixture disk full")
        replies = await self.run_command()
        self.assertIn("fixture disk full", replies[-1])
        self.plugin._call_security_scan.assert_called_once()
        self.plugin._call_packager.assert_not_called()
        self.assertEqual(self.plugin.active_sessions, {})

    async def test_reply_rendering_failure_propagates_after_cleanup(self):
        event = Event()
        event.plain_result = Mock(side_effect=RuntimeError("fixture reply failure"))
        command = self.plugin.agent_command(event)
        try:
            with self.assertRaisesRegex(RuntimeError, "fixture reply failure"):
                await anext(command)
        finally:
            await command.aclose()
        self.plugin.logger.error.assert_called_once()
        self.assertEqual(self.plugin.active_sessions, {})
        self.assert_no_pipeline()

    def test_factory_forwards_context_and_config(self):
        context = object()
        config = {"quality_threshold": 91, "admin_blacklist": ["blocked"]}
        with patch.object(MAIN, "CodeAgentPlugin") as plugin_type:
            result = MAIN.get_star(context=context, config=config)
        plugin_type.assert_called_once_with(context=context, config=config)
        self.assertIs(result, plugin_type.return_value)

    def test_factory_constructs_plugin_without_replacing_config(self):
        """Exercise the real constructor with populated and empty config."""
        with patch.object(MAIN.CodeAgentPlugin, "_ensure_nodejs"), \
                patch.object(MAIN.CodeAgentPlugin, "_ensure_js_dependencies"), \
                patch.object(MAIN, "Path", return_value=self.workspace):
            for config in ({"quality_threshold": 91}, {}):
                with self.subTest(config=config):
                    plugin = MAIN.get_star(object(), config)
                    self.assertIsInstance(plugin, MAIN.CodeAgentPlugin)
                    self.assertIs(plugin.config, config)
                    self.assertEqual(plugin.active_sessions, {})
                    self.assertEqual(
                        plugin._get_config("quality_threshold", 75),
                        config.get("quality_threshold", 75),
                    )
        self.process_guard.assert_not_called()


if __name__ == "__main__":
    unittest.main()
