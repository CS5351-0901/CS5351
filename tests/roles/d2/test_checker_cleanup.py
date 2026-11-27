"""Week 11 cleanup regression tests for D2 external checkers."""

import importlib.util
from pathlib import Path

import pytest


SCRIPT_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills"
    / "CodeAgent"
    / "scripts"
    / "codeagent_security.py"
)


def load_security_module():
    spec = importlib.util.spec_from_file_location("codeagent_security_week11", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_temporary_source_file_is_removed_after_success():
    module = load_security_module()

    with module.temporary_source_file("print('ok')\n", ".py") as temp_path:
        generated = Path(temp_path)
        assert generated.read_text(encoding="utf-8") == "print('ok')\n"

    assert not generated.exists()


def test_temporary_source_file_is_removed_after_checker_failure():
    module = load_security_module()
    generated = None

    with pytest.raises(RuntimeError, match="checker failed"):
        with module.temporary_source_file("echo ok\n", ".sh") as temp_path:
            generated = Path(temp_path)
            assert generated.exists()
            raise RuntimeError("checker failed")

    assert generated is not None
    assert not generated.exists()


def test_ruff_checker_removes_temp_file_when_subprocess_fails(monkeypatch, tmp_path):
    module = load_security_module()
    real_named_tempfile = module.tempfile.NamedTemporaryFile

    def named_tempfile_in_test_dir(**kwargs):
        return real_named_tempfile(dir=tmp_path, **kwargs)

    def fail_to_run(*args, **kwargs):
        raise RuntimeError("runner failed")

    monkeypatch.setattr(module.tempfile, "NamedTemporaryFile", named_tempfile_in_test_dir)
    monkeypatch.setattr(module.subprocess, "run", fail_to_run)
    checker = module.RuffChecker()
    checker._ruff_available = True

    result = checker.check("print('ok')\n", "sample.py")

    assert result["error"] == "runner failed"
    assert list(tmp_path.iterdir()) == []
