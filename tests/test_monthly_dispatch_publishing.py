"""Website publishing requires an explicit request and a current digest."""

import datetime
import hashlib
import json
import sys
import types
from pathlib import Path
from unittest.mock import Mock

import pytest

import scripts.monthly_hermes_run as runner
from scripts.monthly_hermes_run import _is_fresh_digest, push_to_github


def test_monthly_runner_uses_canonical_news_directory():
    assert runner.NEWS_DIR == runner.BASE_DIR / "data" / "knowledge" / "news"


def _digest(tmp_path: Path, date: str) -> Path:
    path = tmp_path / f"tldr-weekly-{date}-w2026W39.md"
    path.write_text("Weekly digest", encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("digest_date", "expected"),
    [("2026-09-23", True), ("2026-09-16", True),
     ("2026-09-15", False), ("2026-09-24", False)],
)
def test_digest_age_controls_publishing(tmp_path, digest_date, expected):
    assert _is_fresh_digest(_digest(tmp_path, digest_date), "2026-09-23") is expected


def test_missing_or_undated_digest_is_not_publishable(tmp_path):
    assert not _is_fresh_digest(None, "2026-09-23")
    assert not _is_fresh_digest(tmp_path / "tldr-weekly-2026-09-23-w2026W39.md", "2026-09-23")
    bad_name = tmp_path / "weekly-digest.md"
    bad_name.write_text("Weekly digest", encoding="utf-8")
    assert not _is_fresh_digest(bad_name, "2026-09-23")


def test_credentials_alone_never_publish_and_stale_digest_stays_draft(tmp_path, monkeypatch):
    monkeypatch.setenv("WEBSITE_GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("WEBSITE_GITHUB_REPO", "owner/website")
    monkeypatch.setitem(sys.modules, "github", None)

    fresh = _digest(tmp_path, "2026-09-23")
    stale = _digest(tmp_path, "2026-09-15")
    assert not push_to_github("Dispatch", "2026-09-23", digest_path=fresh)
    assert not push_to_github("Dispatch", "2026-09-23", publish=True, digest_path=stale)
    assert not push_to_github("Dispatch", "2026-09-23", publish=True)


def test_explicit_publish_with_fresh_digest_reaches_website(tmp_path, monkeypatch):
    created = []

    class FakeRepo:
        def get_contents(self, path, ref):
            raise FileNotFoundError(path)

        def create_file(self, **kwargs):
            created.append(kwargs)

    class FakeAuth:
        @staticmethod
        def Token(token):
            return token

    class FakeGithub:
        def __init__(self, auth):
            assert auth == "test-token"

        def get_repo(self, name):
            assert name == "owner/website"
            return FakeRepo()

    monkeypatch.setitem(sys.modules, "github", types.SimpleNamespace(Github=FakeGithub, Auth=FakeAuth))
    monkeypatch.setenv("WEBSITE_GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("WEBSITE_GITHUB_REPO", "owner/website")

    assert push_to_github(
        "# Dispatch\n\nFresh news", "2026-09-23",
        publish=True, digest_path=_digest(tmp_path, "2026-09-23"),
        publication_date="2026-09-24",
    )
    assert len(created) == 1
    assert created[0]["branch"] == "master"
    assert created[0]["path"].endswith("LifeOS-Monthly-Dispatch--2026-09-23.md")
    assert "LifeOS Monthly Dispatch — 2026-09-23" in created[0]["content"]


def test_delayed_publish_checks_freshness_on_publication_day(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "github", None)
    stale_on_publish_day = _digest(tmp_path, "2026-09-16")

    assert not push_to_github(
        "Reviewed", "2026-09-23", publish=True,
        digest_path=stale_on_publish_day, publication_date="2026-09-24",
    )


def test_pipeline_saves_draft_and_source_without_publishing(tmp_path, monkeypatch):
    digest_dir = tmp_path / "knowledge" / "news" / "digest"
    digest_dir.mkdir(parents=True)
    digest = _digest(digest_dir, "2026-09-23")
    draft_dir = tmp_path / "data" / "inbox" / "content_drafts"
    monkeypatch.setattr(runner, "BASE_DIR", tmp_path)
    monkeypatch.setattr(runner, "DRAFT_DIR", draft_dir)
    monkeypatch.setattr(runner, "DIGEST_DIR", digest_dir)
    monkeypatch.setattr(runner, "DB_PATH", tmp_path / "missing.db")
    monkeypatch.setattr(runner, "triage_notes", lambda: None)
    monkeypatch.setattr(runner, "find_latest_digest", lambda: digest)
    monkeypatch.setattr(runner, "collect_articles_from_notes", lambda days: [])
    monkeypatch.setattr(runner, "call_llm", lambda **kwargs: "# Dispatch\n\nFresh news")
    monkeypatch.setattr(runner, "push_to_github", Mock(side_effect=AssertionError("publisher called")))

    runner.run_weekly_pipeline.__wrapped__()

    drafts = list(draft_dir.glob("monthly_dispatch_*.md"))
    assert len(drafts) == 1
    source = json.loads(drafts[0].with_suffix(".source.json").read_text(encoding="utf-8"))
    assert source == {
        "digest": digest.relative_to(tmp_path).as_posix(),
        "sha256": hashlib.sha256(digest.read_bytes()).hexdigest(),
    }


def test_publish_command_reads_existing_edited_draft_only(tmp_path, monkeypatch):
    digest_dir = tmp_path / "knowledge" / "news" / "digest"
    digest_dir.mkdir(parents=True)
    today = datetime.date.today().isoformat()
    draft_date = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    digest = _digest(digest_dir, today)
    draft_dir = tmp_path / "data" / "inbox" / "content_drafts"
    draft_dir.mkdir(parents=True)
    draft = draft_dir / f"monthly_dispatch_{draft_date}.md"
    draft.write_text("# Reviewed and edited dispatch\n", encoding="utf-8")
    draft.with_suffix(".source.json").write_text(json.dumps({
        "digest": digest.relative_to(tmp_path).as_posix(),
        "sha256": hashlib.sha256(digest.read_bytes()).hexdigest(),
    }), encoding="utf-8")
    publish = Mock(return_value=True)
    monkeypatch.setattr(runner, "BASE_DIR", tmp_path)
    monkeypatch.setattr(runner, "DRAFT_DIR", draft_dir)
    monkeypatch.setattr(runner, "DIGEST_DIR", digest_dir)
    monkeypatch.setattr(runner, "push_to_github", publish)
    monkeypatch.setattr(runner, "run_weekly_pipeline", Mock(side_effect=AssertionError("pipeline called")))
    monkeypatch.setattr(runner, "triage_notes", Mock(side_effect=AssertionError("outbox consumed")))
    monkeypatch.setattr(runner, "call_llm", Mock(side_effect=AssertionError("LLM called")))

    assert runner.main(["--publish-draft", str(draft)]) == 0
    publish.assert_called_once_with(
        "# Reviewed and edited dispatch\n", draft_date,
        publish=True, digest_path=digest, publication_date=today,
    )


@pytest.mark.parametrize("existing", ["draft", "sidecar"])
def test_same_day_rerun_preserves_existing_review_files(tmp_path, monkeypatch, existing):
    draft_dir = tmp_path / "data" / "inbox" / "content_drafts"
    draft_dir.mkdir(parents=True)
    today = datetime.date.today().isoformat()
    draft = draft_dir / f"monthly_dispatch_{today}.md"
    source = draft.with_suffix(".source.json")
    guarded = draft if existing == "draft" else source
    guarded.write_text("human review", encoding="utf-8")
    monkeypatch.setattr(runner, "DRAFT_DIR", draft_dir)
    monkeypatch.setattr(runner, "triage_notes", Mock(side_effect=AssertionError("outbox consumed")))
    monkeypatch.setattr(runner, "call_llm", Mock(side_effect=AssertionError("LLM called")))
    monkeypatch.setattr(runner, "_run_fallback_pipeline", Mock(side_effect=AssertionError("generation called")))
    monkeypatch.setattr(runner, "push_to_github", Mock(side_effect=AssertionError("publisher called")))

    runner.run_weekly_pipeline.__wrapped__()

    assert guarded.read_text(encoding="utf-8") == "human review"
    assert not (source if existing == "draft" else draft).exists()


def test_default_command_runs_draft_pipeline_only(monkeypatch):
    pipeline = Mock()
    monkeypatch.setattr(runner, "run_weekly_pipeline", pipeline)
    monkeypatch.setattr(
        runner, "publish_existing_draft", Mock(side_effect=AssertionError("publish called")),
    )

    assert runner.main([]) == 0
    pipeline.assert_called_once_with()


def test_publish_rejects_outside_draft_and_changed_digest(tmp_path, monkeypatch):
    digest_dir = tmp_path / "knowledge" / "news" / "digest"
    digest_dir.mkdir(parents=True)
    today = datetime.date.today().isoformat()
    digest = _digest(digest_dir, today)
    draft_dir = tmp_path / "data" / "inbox" / "content_drafts"
    draft_dir.mkdir(parents=True)
    draft = draft_dir / f"monthly_dispatch_{today}.md"
    draft.write_text("Reviewed", encoding="utf-8")
    draft.with_suffix(".source.json").write_text(json.dumps({
        "digest": digest.relative_to(tmp_path).as_posix(),
        "sha256": hashlib.sha256(digest.read_bytes()).hexdigest(),
    }), encoding="utf-8")
    monkeypatch.setattr(runner, "BASE_DIR", tmp_path)
    monkeypatch.setattr(runner, "DRAFT_DIR", draft_dir)
    monkeypatch.setattr(runner, "DIGEST_DIR", digest_dir)
    monkeypatch.setattr(runner, "push_to_github", Mock(side_effect=AssertionError("publisher called")))

    outside = tmp_path / draft.name
    outside.write_text("Outside", encoding="utf-8")
    assert not runner.publish_existing_draft(outside)
    digest.write_text("Changed digest", encoding="utf-8")
    assert not runner.publish_existing_draft(draft)

    untrusted_digest = tmp_path / digest.name
    untrusted_digest.write_text("Changed digest", encoding="utf-8")
    draft.with_suffix(".source.json").write_text(json.dumps({
        "digest": untrusted_digest.relative_to(tmp_path).as_posix(),
        "sha256": hashlib.sha256(untrusted_digest.read_bytes()).hexdigest(),
    }), encoding="utf-8")
    assert not runner.publish_existing_draft(draft)
    draft.with_suffix(".source.json").unlink()
    assert not runner.publish_existing_draft(draft)


def test_fallback_draft_cannot_publish(tmp_path, monkeypatch):
    draft_dir = tmp_path / "data" / "inbox" / "content_drafts"
    draft_dir.mkdir(parents=True)
    today = datetime.date.today().isoformat()
    draft = draft_dir / f"monthly_dispatch_{today}.md"
    draft.write_text("Fallback", encoding="utf-8")
    draft.with_suffix(".source.json").write_text(
        json.dumps({"digest": None, "sha256": None}), encoding="utf-8",
    )
    monkeypatch.setattr(runner, "BASE_DIR", tmp_path)
    monkeypatch.setattr(runner, "DRAFT_DIR", draft_dir)
    monkeypatch.setattr(runner, "push_to_github", Mock(side_effect=AssertionError("publisher called")))

    assert not runner.publish_existing_draft(draft)
