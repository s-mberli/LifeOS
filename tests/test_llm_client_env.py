"""Importing the LLM client must not depend on a readable Hermes config."""

import runpy
from pathlib import Path
from unittest.mock import call, patch


def test_unreadable_optional_hermes_env_does_not_block_import(monkeypatch):
    module_path = Path(__file__).resolve().parent.parent / "src" / "core" / "llm_client.py"
    fake_home = module_path.parent / "fake-home"
    hermes_env = fake_home / ".hermes" / ".env"
    original_exists = Path.exists
    checked_hermes_paths = []

    monkeypatch.setattr(Path, "home", classmethod(lambda cls: fake_home))

    def exists_with_denied_hermes_env(path):
        if path.parent.name == ".hermes" and path.name == ".env":
            checked_hermes_paths.append(path)
            raise PermissionError("Hermes home is not readable")
        return original_exists(path)

    monkeypatch.setattr(Path, "exists", exists_with_denied_hermes_env)
    with patch("dotenv.load_dotenv"):
        runpy.run_path(str(module_path))

    assert checked_hermes_paths == [hermes_env]


def test_loads_optional_hermes_env_from_current_users_home(tmp_path, monkeypatch):
    module_path = Path(__file__).resolve().parent.parent / "src" / "core" / "llm_client.py"
    hermes_env = tmp_path / ".hermes" / ".env"
    hermes_env.parent.mkdir()
    hermes_env.write_text("", encoding="utf-8")
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))

    with patch("dotenv.load_dotenv") as load_dotenv:
        runpy.run_path(str(module_path))

    assert call(hermes_env, override=False) in load_dotenv.call_args_list
