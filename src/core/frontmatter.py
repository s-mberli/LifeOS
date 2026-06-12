"""
scripts/core/frontmatter.py — Canonical YAML frontmatter read/write helpers.

All frontmatter parsing in LifeOS must go through this module.
Uses yaml.safe_load / yaml.dump exclusively — no manual string parsing.
"""

from __future__ import annotations

import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def read_fm(path: Path) -> tuple[dict, str]:
    """Read a Markdown file and return (frontmatter_dict, body_text).

    The frontmatter block is delimited by ``---`` lines at the top of the file.
    If no frontmatter is found an empty dict is returned and the entire file
    content is treated as the body.

    Args:
        path: Absolute or relative path to the Markdown file.

    Returns:
        A tuple of (frontmatter dict, body string).  Both are always present;
        the dict may be empty and the body may be an empty string.

    Raises:
        OSError: If the file cannot be read.
    """
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        return {}, text

    # Find the closing ``---``
    end_marker = text.find("---", 3)
    if end_marker < 0:
        # Malformed frontmatter — return raw text as body
        return {}, text

    raw_yaml = text[3:end_marker]
    body = text[end_marker + 3:]

    fm: dict = yaml.safe_load(raw_yaml) or {}
    return fm, body


def write_fm(path: Path, fm: dict, body: str) -> None:
    """Write a Markdown file with YAML frontmatter.

    Serialises *fm* with ``yaml.dump`` (block style) and prepends it to
    *body*, separated by ``---`` delimiters.

    Args:
        path: Destination file path.  Parent directories must exist.
        fm:   Frontmatter key/value pairs.
        body: Markdown body text (the part after the closing ``---``).
    """
    yaml_text = yaml.dump(fm, default_flow_style=False, allow_unicode=True)
    content = f"---\n{yaml_text}---{body}"
    path.write_text(content, encoding="utf-8")  # codeql[py/clear-text-storage-sensitive-data]


def update_fm(path: Path, **kwargs) -> bool:
    """Read a Markdown file, patch specific frontmatter keys, and rewrite it.

    Only the keys listed in *kwargs* are changed; all other existing keys are
    preserved.  If a key does not yet exist it is added.  Values of ``None``
    in *kwargs* are stored as YAML ``null``.

    Args:
        path:   Path to the Markdown file to update.
        **kwargs: Key/value pairs to patch in the frontmatter.

    Returns:
        ``True`` on success, ``False`` if the file could not be read or the
        frontmatter could not be parsed.
    """
    try:
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---") or text.find("---", 3) < 0:
            return False
    except OSError:
        return False

    try:
        fm, body = read_fm(path)
    except OSError:
        return False

    fm.update(kwargs)

    try:
        write_fm(path, fm, body)
    except OSError:
        return False

    return True
