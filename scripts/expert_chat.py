#!/usr/bin/env python3
"""
expert_chat.py — Load expert profile context for Telegram expert chat mode.

Usage:
    python expert_chat.py load <expert_slug>     # prints system prompt
    python expert_chat.py list                   # list available experts
    python expert_chat.py sources <expert_slug>  # print source excerpts
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPERTS_DIR = ROOT / "data" / "experts"

# Ensure src/ is importable
sys.path.insert(0, str(ROOT / "src"))


def list_experts() -> list[dict]:
    if not EXPERTS_DIR.is_dir():
        return []
    results = []
    for entry in sorted(EXPERTS_DIR.iterdir()):
        if not entry.is_dir() or not entry.name.startswith("expert--"):
            continue
        profile_path = entry / "profile.md"
        fm = {}
        if profile_path.exists():
            try:
                from core.frontmatter import read_fm
                fm, _ = read_fm(profile_path)
            except Exception:
                pass
        results.append({
            "slug": entry.name,
            "name": fm.get("expert", entry.name.replace("expert--", "").replace("-", " ").title()),
            "insight_count": fm.get("insight_count", 0),
        })
    return results


def load_expert_context(slug: str) -> str:
    """Build full system prompt string for an expert."""
    expert_dir = EXPERTS_DIR / slug
    if not expert_dir.is_dir():
        return f"[ERROR: Expert '{slug}' not found]"

    def _read(filename: str) -> str:
        p = expert_dir / filename
        if not p.exists():
            return f"(no {filename})"
        try:
            from core.frontmatter import read_fm
            _, body = read_fm(p)
            return body.strip()
        except Exception:
            return p.read_text(encoding="utf-8").strip()

    profile_body = _read("profile.md")
    principles_body = _read("principles.md")
    playbook_body = _read("playbook.md")

    # Load source excerpts
    sources_dir = expert_dir / "sources"
    source_texts = []
    if sources_dir.is_dir():
        for ref_file in sorted(sources_dir.glob("*-ref.md")):
            try:
                from core.frontmatter import read_fm
                ref_fm, ref_body = read_fm(ref_file)
                source_path = ref_fm.get("source_path", "")
                source_title = ref_fm.get("source_title", ref_file.stem)
                if source_path:
                    insight_p = ROOT / source_path
                    if insight_p.exists():
                        _, insight_body = read_fm(insight_p)
                        source_texts.append(f"### {source_title}\n{insight_body.strip()[:1500]}")
            except Exception:
                pass

    parts = [f"# Expert Profile\n{profile_body}"]
    if principles_body and principles_body != "(no principles.md)":
        parts.append(f"# Principles\n{principles_body}")
    if playbook_body and playbook_body != "(no playbook.md)":
        parts.append(f"# Playbook\n{playbook_body}")
    if source_texts:
        parts.append("# Source Insights\n" + "\n\n".join(source_texts[:5]))

    return "\n\n---\n\n".join(parts)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        experts = list_experts()
        if not experts:
            print("  (no experts found)")
        for e in experts:
            print(f"  {e['slug']}  —  {e['name']}  ({e['insight_count']} insights)")

    elif cmd == "match" and len(sys.argv) >= 3:
        """Fuzzy match an expert by name. Returns slug."""
        query = sys.argv[2].lower()
        experts = list_experts()
        matches = [e for e in experts if query in e['slug'].lower() or query in e['name'].lower()]
        if len(matches) == 1:
            print(matches[0]['slug'])
        elif len(matches) > 1:
            for m in matches:
                print(f"  {m['slug']}  —  {m['name']}")
        else:
            print("[NO MATCH]")

    elif cmd == "load" and len(sys.argv) >= 3:
        slug = sys.argv[2]
        # Auto-prefill expert-- if missing
        if not slug.startswith("expert--"):
            # Try direct match first
            candidate = EXPERTS_DIR / f"expert--{slug}"
            if candidate.is_dir():
                slug = f"expert--{slug}"
            else:
                # Fuzzy: try to find by name
                candidates = []
                for entry in EXPERTS_DIR.iterdir():
                    if entry.is_dir() and slug.lower() in entry.name.lower():
                        candidates.append(entry.name)
                if len(candidates) == 1:
                    slug = candidates[0]
                elif len(candidates) > 1:
                    print(f"[AMBIGUOUS: {', '.join(candidates)}]")
                    sys.exit(1)
        print(load_expert_context(slug))

    elif cmd == "sources" and len(sys.argv) >= 3:
        slug = sys.argv[2]
        expert_dir = EXPERTS_DIR / slug
        sources_dir = expert_dir / "sources"
        if sources_dir.is_dir():
            for f in sorted(sources_dir.glob("*-ref.md")):
                print(f"  {f.name}")
        else:
            print("  (no sources)")

    else:
        print(__doc__)
        sys.exit(1)
