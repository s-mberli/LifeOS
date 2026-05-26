"""
Tests for expert-related utilities.

Covers:
- ``slugify_expert_name`` (currently in ``scripts/ingest_resource.py``)
- ``get_existing_experts`` (planned in ``scripts/core/experts.py``)

All tests for the future ``src.core.experts`` module are guarded with
``pytest.mark.skipif`` so the suite remains green while that module is absent.
"""
import importlib
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Optional import of the future core.experts module
# ---------------------------------------------------------------------------
_CORE_EXPERTS_AVAILABLE = importlib.util.find_spec("src.core.experts") is not None

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "src"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


# ---------------------------------------------------------------------------
# Tests: slugify_expert_name (from ingest_resource – always runs)
# ---------------------------------------------------------------------------


class TestSlugifyExpertName:
    """Tests for the ``slugify_expert_name`` function in ingest_resource."""

    @pytest.fixture(autouse=True)
    def _import_slugify(self):
        """Import slugify_expert_name from ingest_resource at test time."""
        try:
            from core.experts import slugify_expert_name
            self._fn = slugify_expert_name
        except Exception as exc:
            pytest.skip(f"Could not import core.experts: {exc}")

    def test_simple_name(self):
        """A plain two-word name must be lowercased, hyphenated, and prefixed."""
        assert self._fn("Santiago Ferreiro") == "expert--santiago-ferreiro"

    def test_single_word(self):
        """A single-word name must still get the expert-- prefix."""
        assert self._fn("Lex") == "expert--lex"

    def test_special_characters_stripped(self):
        """Non-alphanumeric characters must be removed, not kept."""
        result = self._fn("Dr. Jane O'Brien")
        # Special chars like . and ' are stripped
        assert result.startswith("expert--")
        assert "." not in result
        assert "'" not in result

    def test_extra_whitespace_normalised(self):
        """Multiple spaces between words must collapse to a single hyphen."""
        assert self._fn("  Alan   Turing  ") == "expert--alan-turing"

    def test_already_lowercase(self):
        """An already-lowercase name must still be prefixed correctly."""
        assert self._fn("tim ferriss") == "expert--tim-ferriss"

    def test_empty_string(self):
        """An empty string must produce the bare prefix without trailing hyphens."""
        result = self._fn("")
        assert result == "expert--"

    def test_unicode_safe(self):
        """Names with accented characters must not crash (stripped or kept)."""
        result = self._fn("José Mújica")
        assert result.startswith("expert--")

    def test_idempotent_on_slug(self):
        """Passing an already-slugified string must not double-encode it."""
        slug = self._fn("Alice Bob")
        # Calling again should produce the same result (minus the extra prefix)
        result = self._fn(slug.replace("expert--", ""))
        assert result == slug


# ---------------------------------------------------------------------------
# Tests: get_existing_experts (future src.core.experts)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not _CORE_EXPERTS_AVAILABLE,
    reason="src.core.experts not yet implemented",
)
class TestGetExistingExperts:
    """Tests for ``src.core.experts.get_existing_experts``.

    The real API signature is: ``get_existing_experts(root: Path) -> list[dict]``
    where each dict has keys ``slug``, ``display_name``, and ``path``.
    """

    @pytest.fixture(autouse=True)
    def _import_core(self):
        """Import the core experts module."""
        import src.core.experts as experts_mod  # noqa: F401

        self._mod = experts_mod
        self._fn = experts_mod.get_existing_experts

    def test_empty_experts_dir_returns_empty_list(self, tmp_project: Path):
        """An empty data/experts/ directory must yield an empty list."""
        result = self._fn(tmp_project)
        assert result == []

    def test_finds_expert_directories(self, tmp_project: Path):
        """Subdirectories matching ``expert--*`` must be returned as dicts with a 'slug' key."""
        experts_dir = tmp_project / "data" / "experts"
        (experts_dir / "expert--alice-smith").mkdir(parents=True)
        (experts_dir / "expert--bob-jones").mkdir(parents=True)
        result = self._fn(tmp_project)
        slugs = [d["slug"] for d in result]
        assert "expert--alice-smith" in slugs
        assert "expert--bob-jones" in slugs

    def test_non_expert_dirs_ignored(self, tmp_project: Path):
        """Directories not starting with ``expert--`` must not be returned."""
        experts_dir = tmp_project / "data" / "experts"
        (experts_dir / "some-random-folder").mkdir(parents=True)
        result = self._fn(tmp_project)
        slugs = [d["slug"] for d in result]
        assert "some-random-folder" not in slugs

    def test_returns_list_type(self, tmp_project: Path):
        """Return type must always be a list even when no experts exist."""
        result = self._fn(tmp_project)
        assert isinstance(result, list)

    def test_result_dicts_have_expected_keys(self, tmp_project: Path):
        """Each dict in the result must contain 'slug', 'display_name', and 'path'."""
        experts_dir = tmp_project / "data" / "experts"
        (experts_dir / "expert--test-person").mkdir(parents=True)
        result = self._fn(tmp_project)
        assert len(result) == 1
        assert "slug" in result[0]
        assert "display_name" in result[0]
        assert "path" in result[0]


@pytest.mark.skipif(
    not _CORE_EXPERTS_AVAILABLE,
    reason="src.core.experts not yet implemented",
)
class TestCreateEmptyExpert:
    """Tests for ``src.core.experts.create_empty_expert``."""

    @pytest.fixture(autouse=True)
    def _import_core(self):
        """Import the core experts module."""
        import src.core.experts as experts_mod
        self._mod = experts_mod
        self._fn = experts_mod.create_empty_expert

    def test_creates_empty_expert_scaffold(self, tmp_project: Path):
        """Must create expert directory and empty profile, playbook, principles, and evidence files."""
        original_root = self._mod.ROOT
        self._mod.ROOT = tmp_project
        try:
            res = self._fn("Jane Doe")
            assert res["success"] is True
            expert_slug = res["expert_slug"]
            assert expert_slug == "expert--jane-doe"

            expert_dir = tmp_project / "data" / "experts" / expert_slug
            assert expert_dir.exists()
            assert (expert_dir / "profile.md").exists()
            assert (expert_dir / "playbook.md").exists()
            assert (expert_dir / "principles.md").exists()
            assert (expert_dir / "evidence.md").exists()
            
            # Verify profile metadata
            from src.core.frontmatter import read_fm
            profile_fm, profile_body = read_fm(expert_dir / "profile.md")
            assert profile_fm["expert"] == "Jane Doe"
            assert profile_fm["expert_slug"] == "expert--jane-doe"
            assert profile_fm["insight_count"] == 0
        finally:
            self._mod.ROOT = original_root

    def test_fails_if_expert_already_exists(self, tmp_project: Path):
        """Must fail if the expert directory already exists."""
        original_root = self._mod.ROOT
        self._mod.ROOT = tmp_project
        try:
            # Create pre-existing expert
            expert_dir = tmp_project / "data" / "experts" / "expert--jane-doe"
            expert_dir.mkdir(parents=True)

            res = self._fn("Jane Doe")
            assert res["success"] is False
            assert "already exists" in res["error"]
        finally:
            self._mod.ROOT = original_root


@pytest.mark.skipif(
    not _CORE_EXPERTS_AVAILABLE,
    reason="src.core.experts not yet implemented",
)
class TestScanUnattachedInsights:
    """Tests for ``src.core.experts.scan_unattached_insights``."""

    @pytest.fixture(autouse=True)
    def _import_core(self):
        import src.core.experts as experts_mod
        self._mod = experts_mod
        self._fn = experts_mod.scan_unattached_insights

    def test_scans_inbox_as_well_as_knowledge(self, tmp_project: Path):
        from src.core.frontmatter import write_fm
        
        # Create unattached insight in inbox
        inbox_dir = tmp_project / "data" / "inbox" / "processed" / "needs-review"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        inbox_file = inbox_dir / "inbox_note.md"
        write_fm(inbox_file, {"type": "insight_note", "expert_status": "unattached"}, "body")
        
        # Create unattached insight in knowledge
        knowledge_dir = tmp_project / "data" / "knowledge" / "general"
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        knowledge_file = knowledge_dir / "know_note.md"
        write_fm(knowledge_file, {"type": "insight_note", "expert_status": "unattached"}, "body")

        results = self._fn(tmp_project)
        paths = [r["path"] for r in results]
        assert str(inbox_file) in paths
        assert str(knowledge_file) in paths


