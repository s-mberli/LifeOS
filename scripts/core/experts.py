"""
scripts/core/experts.py — Expert profile management for LifeOS.

All logic for reading, writing, and maintaining expert profiles is
centralised here.  The domain→expert mapping is loaded from
``config/domain_map.yaml`` so new domains require no code changes.
"""

from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

import yaml

# Project root — two levels up from this file (scripts/core/experts.py)
ROOT = Path(__file__).resolve().parent.parent.parent


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _load_domain_map() -> dict[str, str]:
    """Load the domain→expert-slug mapping from ``config/domain_map.yaml``.

    Returns an empty dict if the file is missing or unparseable.
    """
    domain_map_path = ROOT / "config" / "domain_map.yaml"
    if not domain_map_path.exists():
        return {}
    try:
        raw = yaml.safe_load(domain_map_path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except Exception:
        return {}


def _read_insight_fm(insight_path: Path) -> dict:
    """Read frontmatter from an insight note.  Returns empty dict on failure."""
    # Local import to avoid circular dependency at module level
    from scripts.core.frontmatter import read_fm  # type: ignore

    try:
        fm, _ = read_fm(insight_path)
        return fm
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def slugify_expert_name(name: str) -> str:
    """Normalise an expert display name to a folder slug.

    Example::

        >>> slugify_expert_name("Santiago Ferreiro")
        'expert--santiago-ferreiro'

    Args:
        name: Human-readable expert name.

    Returns:
        Slug string of the form ``expert--<normalised-name>``.
    """
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return f"expert--{slug}"


def get_existing_experts(root: Path) -> list[dict]:
    """Return metadata for all expert profiles found under ``data/experts/``.

    Args:
        root: Project root directory.

    Returns:
        List of dicts with keys ``slug``, ``display_name``, and ``path``.
    """
    experts_dir = root / "data" / "experts"
    if not experts_dir.is_dir():
        return []

    results: list[dict] = []
    for entry in sorted(experts_dir.iterdir()):
        if not entry.is_dir() or not entry.name.startswith("expert--"):
            continue
        display_name = entry.name.replace("expert--", "").replace("-", " ").title()
        results.append(
            {
                "slug": entry.name,
                "display_name": display_name,
                "path": entry,
            }
        )
    return results


def assign_insight_to_expert(
    insight_path: Path,
    expert_slug: str,
    expert_name: str | None = None,
    reason: str = "user selected",
) -> dict:
    """Attach an existing insight note to an expert profile.

    Creates the expert directory tree if it does not exist, writes a
    source-reference note into ``sources/``, updates the insight's
    frontmatter, appends a row to ``evidence.md``, and creates or
    updates ``profile.md``.

    Args:
        insight_path: Path to the insight note ``.md`` file.
        expert_slug:  Expert folder slug (e.g. ``expert--jane-doe``).
        expert_name:  Human-readable display name.  Derived from slug if omitted.
        reason:       Why the insight is being attached (stored in the ref note).

    Returns:
        Dict with keys ``success`` (bool), ``expert_dir`` (str on success),
        and ``error`` (str on failure).
    """
    from scripts.core.frontmatter import read_fm, write_fm, update_fm  # type: ignore

    try:
        expert_dir = ROOT / "data" / "experts" / expert_slug
        sources_dir = expert_dir / "sources"
        profile_path = expert_dir / "profile.md"

        expert_display_name = (
            expert_name
            if expert_name
            else expert_slug.replace("expert--", "").replace("-", " ").title()
        )

        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        now_str = now.isoformat()
        date_str = now.strftime("%Y-%m-%d")

        # Read insight frontmatter for linking metadata
        insight_fm = _read_insight_fm(insight_path)
        title = insight_fm.get("title", insight_path.stem)
        summary = insight_fm.get("summary", "")
        channel = insight_fm.get("channel", insight_fm.get("channel_name", ""))
        source_url = insight_fm.get("source_url", "")

        # ── 1. Scaffold directories ───────────────────────────────────────────
        expert_dir.mkdir(parents=True, exist_ok=True)
        sources_dir.mkdir(parents=True, exist_ok=True)

        _SCAFFOLDS: dict[str, str] = {
            "playbook.md": (
                "# Playbook\n\n"
                "> What strategies, systems, or frameworks does this expert use?\n\n"
                "## Repeated Frameworks\n- \n\n"
                "## How They Operate\n- \n\n"
                "## What They Avoid\n- \n\n"
                "---\n"
                "*Synthesized from attached insights.*\n"
            ),
            "principles.md": (
                "# Principles\n\n"
                "> What are their core beliefs and the unique angles they bring?\n\n"
                "## Core Beliefs\n- \n\n"
                "## Unique Angle\n- \n\n"
                "---\n"
                "*Synthesized from attached insights.*\n"
            ),
            "evidence.md": (
                "# Evidence Index\n\n"
                "> A running log of all insights attached to this expert.\n\n"
                "| Date | Insight | Summary |\n"
                "|------|---------|---------||\n"
            ),
        }
        for fname, scaffold_content in _SCAFFOLDS.items():
            fpath = expert_dir / fname
            if not fpath.exists():
                fpath.write_text(scaffold_content, encoding="utf-8")
                print(f"  [+] Scaffolded: {fname}")

        # ── 2. Create source-reference note ──────────────────────────────────
        safe_title = re.sub(r"[^a-zA-Z0-9-]", "-", title.lower())
        safe_title = re.sub(r"-+", "-", safe_title).strip("-")
        ref_filename = f"{date_str}-{safe_title[:30]}-ref.md"
        ref_path = sources_dir / ref_filename

        if ref_path.exists():
            return {"success": True, "expert_dir": str(expert_dir), "message": "Already attached."}

        source_rel = ref_path.parent
        rel_insight = insight_path.relative_to(source_rel) if insight_path.is_relative_to(source_rel) else insight_path

        ref_fm: dict = {
            "type": "expert_source_reference",
            "expert_slug": expert_slug,
            "source_path": str(insight_path.relative_to(ROOT)),
            "source_title": title,
            "source_url": source_url,
            "attached_at": now_str,
            "tags": [],
        }
        ref_body = (
            f"\n# Source Reference\n\n"
            f"Original insight note:\n"
            f"[{insight_path.name}]({rel_insight})\n\n"
            f"Reason attached:\n"
            f"- {reason}\n"
        )
        ref_yaml = yaml.dump(ref_fm, default_flow_style=False, allow_unicode=True)
        ref_path.write_text(f"---\n{ref_yaml}---\n{ref_body}", encoding="utf-8")
        print(f"  [+] Source reference created: sources/{ref_filename}")

        # ── 3. Update insight frontmatter ────────────────────────────────────
        insight_fm_current, insight_body = read_fm(insight_path)
        existing_attached: list = insight_fm_current.get("attached_experts", [])
        if isinstance(existing_attached, str):
            existing_attached = [existing_attached]
        if expert_slug not in existing_attached:
            existing_attached.append(expert_slug)

        insight_fm_current.update(
            {
                "expert_status": "attached",
                "attached_experts": existing_attached,
                "review_status": "reviewed",
                "updated_at": now_str,
            }
        )
        write_fm(insight_path, insight_fm_current, insight_body)
        print("  [+] Insight frontmatter updated: expert_status=attached")

        # ── 4. Append row to evidence.md ─────────────────────────────────────
        evidence_path = expert_dir / "evidence.md"
        summary_cell = (summary[:80] + "…") if len(summary) > 80 else (summary or "(manual)")
        try:
            insight_rel = insight_path.relative_to(expert_dir)
        except ValueError:
            insight_rel = insight_path
        evidence_row = f"| {date_str} | [{title}]({insight_rel}) | {summary_cell} |\n"
        with evidence_path.open("a", encoding="utf-8") as f:
            f.write(evidence_row)
        print("  [+] Evidence logged: evidence.md")

        # ── 5. Create or update profile.md ───────────────────────────────────
        if not profile_path.exists():
            profile_fm: dict = {
                "type": "synthesis_expert",
                "expert": expert_display_name,
                "expert_slug": expert_slug,
                "channel": channel or "",
                "created_at": now_str,
                "insight_count": 1,
            }
            profile_body = (
                f"\n# {expert_display_name}\n\n"
                f"**Channel / Handle:** {channel or '(unknown)'}\n\n"
                "## About\n"
                "(Write a brief summary of who this expert is and why you study them.)\n\n"
                "---\n"
                "## Principles\n"
                "![[principles]]\n\n"
                "## Playbook\n"
                "![[playbook]]\n\n"
            )
            profile_yaml = yaml.dump(profile_fm, default_flow_style=False, allow_unicode=True)
            profile_path.write_text(f"---\n{profile_yaml}---\n{profile_body}", encoding="utf-8")
            print(f"  [+] Created: profile.md for {expert_display_name}")
        else:
            # Increment insight_count only
            profile_fm_current, profile_body = read_fm(profile_path)
            profile_fm_current["insight_count"] = int(profile_fm_current.get("insight_count", 0)) + 1
            write_fm(profile_path, profile_fm_current, profile_body)
            print(f"  [+] Updated profile.md for {expert_display_name}")

        # ── 6. Rebuild FTS index ──────────────────────────────────────────────
        try:
            _scripts_dir = ROOT / "scripts"
            if str(_scripts_dir) not in sys.path:
                sys.path.insert(0, str(_scripts_dir))
            from build_fts_index import build_index  # type: ignore

            build_index()
            print("  [+] Rebuilt search index.")
        except Exception as exc:
            print(f"  [-] Failed to rebuild index automatically: {exc}")

        return {"success": True, "expert_dir": str(expert_dir)}

    except Exception as exc:
        return {"success": False, "error": str(exc)}


def scan_unattached_insights(root: Path, limit: int = 50) -> list[dict]:
    """Walk all insight notes and return those not yet attached to an expert.

    Filters out notes where ``expert_status`` is ``'attached'`` or
    ``'ignored'``, or where ``review_status`` is ``'ignored'``.

    Args:
        root:  Project root directory.
        limit: Maximum number of results to return.

    Returns:
        List of dicts with keys ``path``, ``title``, ``domain``, ``tags``,
        ``created_at``, ``review_status``, and ``suggested_experts``.
    """
    from scripts.core.frontmatter import read_fm  # type: ignore

    knowledge_dir = root / "data" / "knowledge"
    results: list[dict] = []

    if not knowledge_dir.is_dir():
        return results

    for fpath in knowledge_dir.rglob("*.md"):
        # Skip raw transcript folders
        if "raw" in fpath.parts:
            continue
        try:
            fm, _ = read_fm(fpath)
        except Exception:
            continue

        if fm.get("type") != "insight_note":
            continue

        status = fm.get("expert_status", "unattached")
        review = fm.get("review_status", "new")
        if status in ("attached", "ignored") or review == "ignored":
            continue

        suggested_raw = fm.get("suggested_experts", [])
        if isinstance(suggested_raw, str):
            suggested = [s.strip() for s in suggested_raw.split(",") if s.strip()]
        else:
            suggested = list(suggested_raw) if suggested_raw else []

        tags_raw = fm.get("tags", [])
        if isinstance(tags_raw, str):
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        else:
            tags = list(tags_raw) if tags_raw else []

        results.append(
            {
                "path": str(fpath),
                "title": fm.get("title", fpath.stem),
                "domain": fm.get("domain", ""),
                "tags": tags,
                "created_at": fm.get("created_at", ""),
                "review_status": review,
                "suggested_experts": suggested,
            }
        )

        if len(results) >= limit:
            break

    return results


def generate_expert_update_suggestion(expert_slug: str, root: Path) -> dict:
    """Generate a suggested update for an expert's profile/principles/playbook.

    Reads all source-reference notes from the expert's ``sources/`` directory,
    follows the ``source_path`` links to load insight body text, then passes
    everything to the LLM.  The result is saved to
    ``outputs/expert-updates/<expert-slug>--YYYY-MM-DD.md``.

    Args:
        expert_slug: Expert folder slug (e.g. ``expert--jane-doe``).
        root:        Project root directory.

    Returns:
        Dict with keys ``success`` (bool), ``output_path`` (str on success),
        and ``error`` (str on failure).
    """
    from scripts.core.frontmatter import read_fm  # type: ignore

    expert_dir = root / "data" / "experts" / expert_slug
    sources_dir = expert_dir / "sources"
    outputs_dir = root / "outputs" / "expert-updates"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    if not sources_dir.is_dir():
        return {"success": False, "error": "No sources directory found."}

    def _read_md(filename: str) -> str:
        p = expert_dir / filename
        return p.read_text(encoding="utf-8") if p.exists() else "(not yet written)"

    profile = _read_md("profile.md")
    principles = _read_md("principles.md")
    playbook = _read_md("playbook.md")

    source_excerpts: list[str] = []
    ref_files = [f for f in sources_dir.iterdir() if f.suffix == ".md" and f.name.endswith("-ref.md")]

    for ref_path in ref_files:
        try:
            ref_fm, _ = read_fm(ref_path)
        except Exception:
            continue

        insight_rel = ref_fm.get("source_path", "")
        if not insight_rel:
            continue

        insight_path = root / insight_rel
        if insight_path.exists():
            try:
                _, insight_body = read_fm(insight_path)
                source_excerpts.append(f"### {ref_path.name}\n{insight_body.strip()[:1200]}")
            except Exception:
                pass

    if not source_excerpts:
        return {"success": False, "error": "No linked insight notes could be loaded."}

    sources_text = "\n\n".join(source_excerpts)
    display_name = expert_slug.replace("expert--", "").replace("-", " ").title()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    prompt = (
        f'You are helping build an Expert Profile for "{display_name}".\n\n'
        f"Existing profile.md:\n{profile[:800]}\n\n"
        f"Existing principles.md:\n{principles[:800]}\n\n"
        f"Existing playbook.md:\n{playbook[:800]}\n\n"
        f"Attached source excerpts:\n{sources_text[:4000]}\n\n"
        "Based on the above, write a structured SUGGESTED UPDATE in Markdown with these sections:\n"
        "## Suggested profile.md update\n"
        "## Suggested principles.md additions\n"
        "## Suggested playbook.md additions\n"
        "## Evidence entries to add\n\n"
        "IMPORTANT: Write ADDITIONS and SUGGESTIONS only. Do not overwrite. Be specific."
    )

    suggestion_text: str
    try:
        _scripts_dir = root / "scripts"
        if str(_scripts_dir) not in sys.path:
            sys.path.insert(0, str(_scripts_dir))
        from llm_client import call_llm  # type: ignore

        suggestion_text = call_llm(prompt) or "LLM returned no content."
    except Exception as exc:
        suggestion_text = f"LLM unavailable. Manual synthesis required.\n\nError: {exc}"

    out_path = outputs_dir / f"{expert_slug}--{date_str}.md"
    header_fm: dict = {
        "type": "expert_update_suggestion",
        "expert_slug": expert_slug,
        "generated_at": date_str,
        "sources_reviewed": len(ref_files),
        "status": "pending_review",
    }
    header_yaml = yaml.dump(header_fm, default_flow_style=False, allow_unicode=True)
    header_body = (
        f"\n# Expert Update Suggestion: {display_name}\n\n"
        "> **Human review required before applying any changes.**\n\n"
        f"{suggestion_text}\n"
    )
    out_path.write_text(f"---\n{header_yaml}---\n{header_body}", encoding="utf-8")

    return {"success": True, "output_path": str(out_path)}


def synthesize_creator_persona(creator_name: str, transcript_text: str) -> dict:
    """Use the LLM to extract a creator's persona from a transcript chunk.

    Calls the LLM asking for a JSON object with ``profile``, ``playbook``,
    and ``principles`` keys describing how to mimic the creator.

    Args:
        creator_name:    The creator's display name.
        transcript_text: A chunk of transcript text (may be truncated).

    Returns:
        Dict with keys ``profile``, ``playbook``, and ``principles``.
        All values are empty strings if the LLM call fails.
    """
    import sys

    _scripts_dir = ROOT / "scripts"
    if str(_scripts_dir) not in sys.path:
        sys.path.insert(0, str(_scripts_dir))

    from llm_client import call_llm  # type: ignore

    prompt = f"""
You are an expert behavioral analyst and copywriter.
Analyze the following transcript excerpt from a YouTube video by creator '{creator_name}'.

Extract their exact persona so that another AI can perfectly mimic them. Focus on:
1. TONE: Are they energetic, calm, academic, sarcastic, bro-ey?
2. VOCABULARY/SLANG: What exact phrases, greetings, or filler words do they use?
3. DELIVERY STYLE: How do they structure their explanations?
4. WORLDVIEW/PRINCIPLES: What core philosophies or themes do they constantly bring up?

Output a strictly valid JSON object with keys:
- "profile": A paragraph written as a system prompt instructing an AI how to act like them.
- "playbook": A paragraph or bullet points detailing their exact delivery style and vocabulary.
- "principles": A short paragraph or bullet points of their core worldview.

TRANSCRIPT EXCERPT:
{transcript_text}
"""
    empty: dict = {"profile": "", "playbook": "", "principles": ""}
    try:
        response_text = call_llm(prompt, model_type="fast", json_mode=True)
        if not response_text:
            return empty
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}")
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx : end_idx + 1]
            return json.loads(json_str)
        return empty
    except Exception as exc:
        print(f"  [!] Error synthesizing creator persona: {exc}")
        return empty


def _suggest_experts_for_domain(
    domain: str,
    tags: list[str],
    channel: str,
    root: Path,
) -> list[str]:
    """Return up to three expert slugs relevant to the given domain/tags/channel.

    Suggestions are limited to experts that actually exist in
    ``data/experts/``.  The domain→expert mapping is read from
    ``config/domain_map.yaml`` at call time (no caching) so changes take
    effect immediately.

    Args:
        domain:  Primary domain string (e.g. ``'ai-platform'``).
        tags:    List of tag strings from the insight note.
        channel: YouTube channel name / author name.
        root:    Project root directory.

    Returns:
        List of up to three expert slug strings.
    """
    experts_dir = root / "data" / "experts"
    if not experts_dir.is_dir():
        return []

    domain_map = _load_domain_map()
    suggestions: list[str] = []

    # 1. Domain-based hard mapping
    if domain in domain_map:
        candidate = domain_map[domain]
        if (experts_dir / candidate).is_dir():
            suggestions.append(candidate)

    # 2. Channel/author name → creator expert match
    if channel and channel.lower() not in ("", "unknown"):
        channel_slug = re.sub(r"[^a-z0-9]", "-", channel.lower()).strip("-")
        candidate = f"expert--{channel_slug}"
        if (experts_dir / candidate).is_dir() and candidate not in suggestions:
            suggestions.append(candidate)

    # 3. Tag-based scan of expert directory names
    lower_tags = [t.lower() for t in tags]
    for entry in experts_dir.iterdir():
        if not entry.is_dir() or not entry.name.startswith("expert--"):
            continue
        if entry.name in suggestions:
            continue
        friendly = entry.name.replace("expert--", "").replace("-", " ")
        if any(friendly in t or t in friendly for t in lower_tags):
            suggestions.append(entry.name)

    return suggestions[:3]
