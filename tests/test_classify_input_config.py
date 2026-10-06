"""Domain classification reads configuration from the repository root."""

from pathlib import Path

from src.core import classify_input


def test_load_domains_config_from_repo_root(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "domains.yaml").write_text(
        "domains:\n  research:\n    keywords: [strategy]\n"
        "    storage_location: data/knowledge/research/\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        classify_input,
        "__file__",
        str(tmp_path / "src" / "core" / "classify_input.py"),
    )

    assert classify_input.load_domains_config() == {
        "research": {
            "keywords": ["strategy"],
            "storage_location": "data/knowledge/research/",
        }
    }
