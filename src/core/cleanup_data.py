import os
from pathlib import Path
import re
from collections import defaultdict

from src.core.frontmatter import read_fm

ROOT = Path(__file__).resolve().parent.parent.parent
knowledge_dir = ROOT / "data" / "knowledge"

def get_frontmatter(path: Path) -> dict:
    try:
        fm, _ = read_fm(path)
        return fm
    except Exception:
        return {}

def clean_data():
    files = list(knowledge_dir.rglob("*.md"))
    
    url_map = defaultdict(list)
    title_map = defaultdict(list)
    
    for f in files:
        fm = get_frontmatter(f)
        url = fm.get("source_url", "")
        title = fm.get("title", f.stem)
        
        if url and url != "None" and url != "Unknown":
            url_map[url].append(f)
        else:
            title_map[title].append(f)
            
    removed = 0
    # Clean by URL
    for url, file_list in url_map.items():
        if len(file_list) > 1:
            # Sort by modified time, keep the newest
            file_list.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            keep = file_list[0]
            for to_remove in file_list[1:]:
                print(f"Removing duplicate by URL: {to_remove.name} (Keep: {keep.name})")
                to_remove.unlink()
                removed += 1
                
    # Clean by Title (only for items without URLs)
    for title, file_list in title_map.items():
        if len(file_list) > 1:
            file_list.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            keep = file_list[0]
            for to_remove in file_list[1:]:
                print(f"Removing duplicate by Title: {to_remove.name} (Keep: {keep.name})")
                to_remove.unlink()
                removed += 1

    print(f"Cleanup complete. Removed {removed} duplicates.")

if __name__ == "__main__":
    clean_data()
