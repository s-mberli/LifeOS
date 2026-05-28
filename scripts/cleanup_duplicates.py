import sys
import yaml
from pathlib import Path
from collections import defaultdict
import re

ROOT = Path("/Users/markus/markusos")
DATA_DIR = ROOT / "data"

def parse_frontmatter(path: Path):
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"): return None
    parts = content.split("---", 2)
    if len(parts) < 3: return None
    try:
        return yaml.safe_load(parts[1])
    except Exception:
        return None

def extract_base_name(stem: str) -> str:
    # Matches _1, _2, _1_2_3, etc. at the end of the stem
    return re.sub(r'(_\d+)+$', '', stem)

def main():
    files = list(DATA_DIR.rglob("*.md"))
    
    # We will deduplicate by URL first, then by Title if URL doesn't exist
    by_url = defaultdict(list)
    by_title = defaultdict(list)
    
    valid_files = []
    
    for f in files:
        if "experts" in f.parts or "raw" in f.parts: continue
        fm = parse_frontmatter(f)
        if not fm: continue
        
        if fm.get("type") == "insight_note":
            valid_files.append(f)
            url = fm.get("source_url")
            title = fm.get("title", "")
            if url:
                by_url[url].append(f)
            elif title:
                by_title[title.lower()].append(f)
                
    deleted_count = 0
    
    # Process URL duplicates
    for url, paths in by_url.items():
        if len(paths) > 1:
            # Sort paths. We assume the shortest stem (no _1, _2 suffixes) is the original
            paths.sort(key=lambda p: len(p.stem))
            keep_path = paths[0]
            delete_paths = paths[1:]
            
            for p in delete_paths:
                print(f"Deleting duplicate: {p.relative_to(ROOT)} (keeping {keep_path.relative_to(ROOT)})")
                p.unlink()
                deleted_count += 1
                
    # Process Title duplicates (for those without URLs)
    for title, paths in by_title.items():
        # Re-check existence in case they were already deleted (though they shouldn't be in both)
        paths = [p for p in paths if p.exists()]
        if len(paths) > 1:
            paths.sort(key=lambda p: len(p.stem))
            keep_path = paths[0]
            delete_paths = paths[1:]
            
            for p in delete_paths:
                print(f"Deleting duplicate: {p.relative_to(ROOT)} (keeping {keep_path.relative_to(ROOT)})")
                p.unlink()
                deleted_count += 1
                
    print(f"\nCleanup complete. Deleted {deleted_count} duplicate files.")

if __name__ == "__main__":
    main()
