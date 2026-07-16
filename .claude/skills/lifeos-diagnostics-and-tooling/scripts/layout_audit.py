#!/usr/bin/env python
"""layout_audit.py — READ-ONLY auditor for the June-21 dual-tree split.

For each (data/<name> vs <name>) pair: file counts, newest mtime per side,
and up to 5 filenames that exist on one side only. Also scans repo-wide for
*sync-conflict* files (Syncthing artifacts), excluding .git.

Primary instrument for the lifeos-data-layout-unification-campaign.
"""
import datetime as dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

# (name, count all files instead of just *.md)
PAIRS = [
    ("knowledge", False),
    ("experts", False),
    ("inbox", False),
    ("private", False),
    ("business", False),
    ("career", False),
    ("tracking", True),
    ("tts_cache", True),
]


def scan(root: Path, all_files: bool):
    """Return {relative_path: mtime} for files under root."""
    if not root.exists():
        return None
    pattern = "*" if all_files else "*.md"
    out = {}
    for p in root.rglob(pattern):
        if p.is_file() and ".git" not in p.parts:
            out[str(p.relative_to(root))] = p.stat().st_mtime
    return out


def fmt_mtime(files):
    if not files:
        return "-"
    return dt.datetime.fromtimestamp(max(files.values())).strftime("%Y-%m-%d %H:%M")


def main() -> int:
    print("=== dual-tree layout audit (READ-ONLY) ===")
    print(f"{'pair':<12} {'data/* files':>12} {'root files':>10}   "
          f"{'newest data/*':<17} {'newest root':<17}")
    details = []
    for name, all_files in PAIRS:
        a = scan(REPO_ROOT / "data" / name, all_files)
        b = scan(REPO_ROOT / name, all_files)
        ca = "-" if a is None else len(a)
        cb = "-" if b is None else len(b)
        print(f"{name:<12} {ca!s:>12} {cb!s:>10}   "
              f"{fmtn(a):<17} {fmtn(b):<17}")
        only_a = sorted(set(a or {}) - set(b or {}))
        only_b = sorted(set(b or {}) - set(a or {}))
        if only_a or only_b:
            details.append((name, only_a, only_b))

    for name, only_a, only_b in details:
        print(f"\n[{name}] only in data/{name}: {len(only_a)}")
        for f in only_a[:5]:
            print(f"    {f}")
        print(f"[{name}] only in root {name}/: {len(only_b)}")
        for f in only_b[:5]:
            print(f"    {f}")

    print("\n=== sync-conflict scan (repo-wide, excluding .git) ===")
    conflicts = [p for p in REPO_ROOT.rglob("*sync-conflict*")
                 if ".git" not in p.parts]
    if conflicts:
        for p in conflicts:
            print(f"    {p.relative_to(REPO_ROOT)}")
    else:
        print("    none found")
    return 0


def fmtn(files):
    return fmt_mtime(files) if files is not None else "(missing)"


if __name__ == "__main__":
    sys.exit(main())
