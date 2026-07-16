#!/usr/bin/env python
"""env_audit.py — READ-ONLY drift check between .env, .env.example and code.

Compares KEY NAMES ONLY. Never reads, stores or prints anything after the
'=' in an env file — values (secrets) are untouchable by design.

Three sets are compared:
  1. keys declared in .env          (names before '=')
  2. keys declared in .env.example  (names before '=')
  3. keys read in code via os.environ.get(...) / os.getenv(...) /
     os.environ[...] with a string literal

Reports: in code but not in .env.example (onboarding gap), in .env but not
in example (undocumented local config), and in example but never read by
code (dead documentation).
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

CODE_DIRS = ["src", "scripts", "tests", "apps"]
CODE_GLOBS = ["*.py"]

ENV_READ_RE = re.compile(
    r"""(?:os\.environ\.get|os\.getenv)\(\s*["']([A-Z][A-Z0-9_]*)["']"""
    r"""|os\.environ\[\s*["']([A-Z][A-Z0-9_]*)["']\s*\]"""
)


def env_keys(path: Path) -> set:
    """Key names only — split each line at the first '=' and discard the rest."""
    if not path.exists():
        return set()
    keys = set()
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip().removeprefix("export ").strip()
        if key:
            keys.add(key)
    return keys


def code_keys() -> dict:
    """{ENV_NAME: [relative files reading it]}"""
    found = {}
    for d in CODE_DIRS:
        root = REPO_ROOT / d
        if not root.exists():
            continue
        for glob in CODE_GLOBS:
            for f in root.rglob(glob):
                try:
                    text = f.read_text(errors="replace")
                except OSError:
                    continue
                for m in ENV_READ_RE.finditer(text):
                    name = m.group(1) or m.group(2)
                    found.setdefault(name, []).append(str(f.relative_to(REPO_ROOT)))
    return found


def show(label, names, readers=None):
    print(f"\n{label}: {len(names)}")
    for n in sorted(names):
        where = ""
        if readers and n in readers:
            where = f"  (read in {readers[n][0]}" + \
                    (f" +{len(readers[n]) - 1} more)" if len(readers[n]) > 1 else ")")
        print(f"    {n}{where}")


def main() -> int:
    dotenv = env_keys(REPO_ROOT / ".env")
    example = env_keys(REPO_ROOT / ".env.example")
    readers = code_keys()
    in_code = set(readers)

    print("=== env drift audit (KEY NAMES ONLY — values never read) ===")
    print(f".env keys: {len(dotenv)}   .env.example keys: {len(example)}   "
          f"distinct keys read in code: {len(in_code)}")

    show("in CODE but NOT in .env.example (onboarding gap)",
         in_code - example, readers)
    show("in .env but NOT in .env.example (undocumented local config)",
         dotenv - example)
    show("in .env.example but NEVER read by code (dead documentation)",
         example - in_code)
    show("in CODE but NOT in .env (may rely on defaults/shell env)",
         in_code - dotenv, readers)
    return 0


if __name__ == "__main__":
    sys.exit(main())
