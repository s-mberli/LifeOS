"""LLM proposal names must stay within the draft proposals directory."""

import pytest

from scripts.monthly_hermes_run import _proposal_output_path, run_weekly_pipeline


def test_repair_wrapper_stays_on_pipeline():
    assert hasattr(run_weekly_pipeline, "__wrapped__")
    assert not hasattr(_proposal_output_path, "__wrapped__")


@pytest.mark.parametrize(
    "filename",
    ["../outside.md", "..\\outside.md", "/tmp/outside.md", "C:\\outside.md", "C:outside.md"],
)
def test_rejects_path_components_and_absolute_paths(tmp_path, filename):
    assert _proposal_output_path(tmp_path / "proposals", filename) is None


@pytest.mark.parametrize("filename", ["proposal_test", "proposal_test.md"])
def test_normal_filename_stays_in_proposals_dir(tmp_path, filename):
    assert _proposal_output_path(tmp_path / "proposals", filename) == (
        tmp_path / "proposals" / "proposal_test.md"
    )
