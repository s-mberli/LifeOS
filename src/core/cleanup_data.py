import os
from pathlib import Path
import re
from collections import defaultdict

ROOT = Path("/Users/markus/.gemini/antigravity/scratch/lifeos")
knowledge_dir = ROOT / "data" / "knowledge"

def get_frontmatter(path: Path) -> dict:
    try:
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---"): return {}
        fm_end = content.find("---", 3)
        if fm_end < 0: return {}
        
        fields = {}
        for line in content[3:fm_end].split("\n"):
            if ":" in line:
                k, _, v = line.partition(":")
                fields[k.strip()] = v.strip().strip("\"'")
        return fields
    except:
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
